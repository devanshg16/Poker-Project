import pydealer
from pydealer.card import card_abbrev
from treys import Card, Evaluator


evaluator = Evaluator()
count = 0



#is needed to convert card format (called in line 40)
def to_treys_format(card):
    rank = card[:-1]
    suit = card[-1].lower()
    if rank == "10":
        rank = "T"
    else:
        rank = rank.upper()  # Keep face ranks uppercase
    return rank + suit

hands = []
#hands is a 2D array, with each row being a different person's hand, and row 0 being the user's hand.
#cards will be in the format "Jack of Diamonds" / "10 of Clubs"



numofplayers = int(input("Enter Number of Players (Incl. Yourself): "))
hands.append(input("Enter the cards in your hand separated by a comma: ").split(","))
hands[0] = [card.strip() for card in hands[0]]





for i in range(10000):
    hands = hands[:1]  


    #creates and shuffles a deck
    deck = pydealer.Deck()
    deck.shuffle()
    [deck.get(card) for card in hands[0]] #  deletes the user's cards from the deck


    #creates the river (5 cards on table)
    table = [card_abbrev(c.value, c.suit) for c in deck.deal(5)]


    #deals cards to other players
    [hands.append([card_abbrev(c.value, c.suit) for c in deck.deal(2)]) for player in range(numofplayers-1)]
    score = []


    #calculates a hand score for each player (lower being better)
    for player in range(numofplayers):
        currhand = table.copy()
        currhand.extend(hands[player])
        treys_hand = [Card.new(to_treys_format(card)) for card in currhand] # converts each card in hand to treys format
        score.append(evaluator.evaluate([],treys_hand))


    if score.index(min(score)) == 0:
        count += 1
    

    print(f"\r{count/100}%", end='', flush=True)


print(f"\rCalculation Complete! There is a {count/100}% chance of you winning.")