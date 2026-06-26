import csv
import pathlib


def evaluate_score(hand):
    """Evaluate a 7-card hand (river + hole cards) and return its score.

    This function is robust to several card string formats such as
    'ac', 'ca', 'Ad', '10d', 'td', ' A C ' (with spaces), etc. It
    opens the CSV lookup files relative to this script's directory.
    """
    isflush = False
    value_score = 1
    suit_score = 1

    rank_values = {
        '2': 2, '3': 3, '4': 5, '5': 7, '6': 11,
        '7': 13, '8': 17, '9': 19, 't': 23,
        'j': 29, 'q': 31, 'k': 37, 'a': 41
    }
    rank_suits = {
        'c': 2, 's': 3, 'h': 5, 'd': 7
    }

    def parse_card(card_str):
        s = str(card_str).strip().lower()
        # Normalize 10 to 't'
        s = s.replace('10', 't')
        # Remove non-alphanumeric characters
        s = ''.join(ch for ch in s if ch.isalnum())
        if len(s) < 2:
            raise ValueError(f"Invalid card: {card_str!r}")
        # If first char is a rank, assume rank+suit (e.g. 'ac')
        if s[0] in rank_values and s[1] in rank_suits:
            return s[0], s[1]
        # If last char is a suit and first is rank (e.g. 'ad')
        if s[-1] in rank_suits and s[0] in rank_values:
            return s[0], s[-1]
        # If format is suit+rank (e.g. 'ca'), swap
        if s[0] in rank_suits and s[1] in rank_values:
            return s[1], s[0]
        # If format is rank at end (e.g. 'dA' normalized to 'da' already handled), try last two
        if s[-2] in rank_values and s[-1] in rank_suits:
            return s[-2], s[-1]
        raise ValueError(f"Unrecognized card format: {card_str!r}")

    for card in hand:
        try:
            rank, suit = parse_card(card)
        except Exception:
            # If a bad card is present, propagate a helpful error
            raise ValueError(f"Bad card in hand: {card!r}")
        value_score *= rank_values[rank]
        suit_score *= rank_suits[suit]

    # Check for flush: suit_score divisible by same suit prime**5
    if suit_score % (2**5) == 0 or suit_score % (3**5) == 0 or suit_score % (5**5) == 0 or suit_score % (7**5) == 0:
        isflush = True

    # Open CSV files relative to this script's directory
    csv_dir = pathlib.Path(__file__).resolve().parent
    if isflush:
        filename = csv_dir / "Flush_Hands.csv"
    else:
        filename = csv_dir / "NoFlush_Hands.csv"

    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        # look for a row where PrimeProduct matches value_score
        for row in reader:
            if int(row['PrimeProduct']) == value_score:
                return int(row['Score'])