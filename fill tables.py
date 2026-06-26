import itertools
import csv
from functools import reduce
import operator

# ---------- Setup ----------
RANKS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
RANK_TO_VALUE = {rank:index for index,rank in enumerate(RANKS)}

# Prime numbers for hand evaluation
RANK_PRIMES = {'2':2,'3':3,'4':5,'5':7,'6':11,'7':13,'8':17,'9':19,
               'T':23,'J':29,'Q':31,'K':37,'A':41}

def prime_product(cards):
    """Multiply primes corresponding to the cards (repeats included)."""
    return reduce(operator.mul, [RANK_PRIMES[c] for c in cards], 1)

def is_consecutive(values):
    """Check if sorted values form a straight (including wheel)."""
    if all(values[i]+1 == values[i+1] for i in range(4)):
        return True
    return values == [0,1,2,3,12]  # Wheel: A-2-3-4-5

def generate_all_straights():
    """Return list of (list_of_ranks, high_card) for all straights."""
    straights = []
    # Wheel
    straights.append((['A','2','3','4','5'],'5'))
    # All other straights
    for start in range(0,9):
        seq = RANKS[start:start+5]
        high = seq[-1]
        straights.append((seq, high))
    return straights

STRAIGHTS = generate_all_straights()
all_5_ranks = list(itertools.combinations(RANKS,5))

flush_list = []
noflush_list = []
score_counter = 1

def add_hand(pattern, components, flush_possible, card_list):
    global score_counter
    score = score_counter
    score_counter += 1
    pp = prime_product(card_list)
    row = (pattern, components, score, pp)
    if flush_possible:
        flush_list.append(row)
    else:
        noflush_list.append(row)

# ---------- 1) Royal Flush ----------
add_hand("Royal Flush", "ranks=A,K,Q,J,T", True, ['A','K','Q','J','T'])
# ---------- 2) Straight Flush ----------
for seq, high in sorted(STRAIGHTS[1:], key=lambda x:RANK_TO_VALUE[x[1]], reverse=True):
    if seq == ['T','J','Q','K','A'] or seq == ['A','2','3','4','5']:
        continue
    add_hand(f"Straight Flush to {high}", f"ranks={','.join(seq)}", True, seq)
# Wheel straight flush
add_hand("Straight Flush to 5", "ranks=A,2,3,4,5", True, ['A','2','3','4','5'])

# ---------- 3) Four of a Kind ----------
for quad in RANKS[::-1]:
    for kicker in RANKS[::-1]:
        if kicker == quad: continue
        add_hand(f"4{quad} + {kicker}", f"quad={quad};kicker={kicker}", False,
                 [quad]*4 + [kicker])

# ---------- 4) Full House ----------
for trips in RANKS[::-1]:
    for pair in RANKS[::-1]:
        if pair == trips: continue
        add_hand(f"{trips}x3 + {pair}x2", f"trips={trips};pair={pair}", False,
                 [trips]*3 + [pair]*2)

# ---------- 5) Flush (non-straight) ----------
for comb in sorted(all_5_ranks, key=lambda c: sorted([RANK_TO_VALUE[r] for r in c], reverse=True), reverse=True):
    values = sorted([RANK_TO_VALUE[r] for r in comb])
    if is_consecutive(values): continue
    sorted_desc = sorted(comb, key=lambda r:RANK_TO_VALUE[r], reverse=True)
    add_hand(f"Flush: {''.join(sorted_desc)}", f"ranks={','.join(sorted_desc)}", True, sorted_desc)

# ---------- 6) Straight (non-flush) ----------
for seq, high in sorted(STRAIGHTS, key=lambda x:RANK_TO_VALUE[x[1]], reverse=True):
    add_hand(f"Straight to {high}", f"ranks={','.join(seq)}", False, seq)

# ---------- 7) Three of a Kind ----------
three_of_kind_hands = []
for trips in RANKS[::-1]:
    kicker_pool = [r for r in RANKS if r != trips]
    for k1,k2 in itertools.combinations(kicker_pool,2):
        ks = sorted([k1,k2], key=lambda r:RANK_TO_VALUE[r], reverse=True)
        three_of_kind_hands.append((trips, ks[0], ks[1], f"{trips}x3 + {ks[0]} + {ks[1]}", [trips]*3 + ks))

three_of_kind_hands.sort(key=lambda x:(RANK_TO_VALUE[x[0]],RANK_TO_VALUE[x[1]],RANK_TO_VALUE[x[2]]), reverse=True)
for trips, k1, k2, pat, card_list in three_of_kind_hands:
    add_hand(pat, f"trips={trips};kickers={k1},{k2}", False, card_list)

# ---------- 8) Two Pair ----------
two_pair_hands = []
for p1,p2 in itertools.combinations(RANKS,2):
    kicker_pool = [r for r in RANKS if r != p1 and r != p2]
    for kicker in kicker_pool:
        hi,lo = (p1,p2) if RANK_TO_VALUE[p1]>RANK_TO_VALUE[p2] else (p2,p1)
        two_pair_hands.append((hi, lo, kicker, f"{hi}x2 + {lo}x2 + {kicker}", [hi]*2 + [lo]*2 + [kicker]))

two_pair_hands.sort(key=lambda x:(RANK_TO_VALUE[x[0]],RANK_TO_VALUE[x[1]],RANK_TO_VALUE[x[2]]), reverse=True)
for hi, lo, kicker, pat, card_list in two_pair_hands:
    add_hand(pat, f"pair_high={hi};pair_low={lo};kicker={kicker}", False, card_list)

# ---------- 9) One Pair ----------
one_pair_hands = []
for pair in RANKS[::-1]:
    kicker_pool = [r for r in RANKS if r != pair]
    for k1,k2,k3 in itertools.combinations(kicker_pool,3):
        ks = sorted([k1,k2,k3], key=lambda r:RANK_TO_VALUE[r], reverse=True)
        one_pair_hands.append((pair, ks[0], ks[1], ks[2], f"{pair}x2 + {ks[0]} + {ks[1]} + {ks[2]}", [pair]*2 + ks))

one_pair_hands.sort(key=lambda x:(RANK_TO_VALUE[x[0]],RANK_TO_VALUE[x[1]],RANK_TO_VALUE[x[2]],RANK_TO_VALUE[x[3]]), reverse=True)
for pair, k1, k2, k3, pat, card_list in one_pair_hands:
    add_hand(pat, f"pair={pair};kickers={k1},{k2},{k3}", False, card_list)

# ---------- 10) High Card ----------
for comb in sorted(all_5_ranks, key=lambda c: sorted([RANK_TO_VALUE[r] for r in c], reverse=True), reverse=True):
    values = sorted([RANK_TO_VALUE[r] for r in comb])
    if is_consecutive(values): continue
    sorted_desc = sorted(comb, key=lambda r:RANK_TO_VALUE[r], reverse=True)
    add_hand(f"High card: {''.join(sorted_desc)}", f"ranks={','.join(sorted_desc)}", False, sorted_desc)

# ---------- Write CSVs ----------
def write_csv(filename,data):
    with open(filename,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Pattern','Components','Score','PrimeProduct'])
        for row in data:
            writer.writerow(row)
    print(f"Wrote {len(data)} rows to {filename}")

write_csv("Flush_Hands.csv", flush_list)
write_csv("NoFlush_Hands.csv", noflush_list)

print(f"Flush list: {len(flush_list)}")
print(f"No-flush list: {len(noflush_list)}")
print(f"Total unique scores: {score_counter-1}")
