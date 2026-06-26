import pydealer
from Other.Poker_Project.evaluate_scores import evaluate_score

numofplayers = int(input("Enter Number of Players (Incl. Yourself): "))
userhand = (input("Enter the cards in your hand separated by a comma: ").split(","))
userhand = [card.strip() for card in userhand]
win_count = 0
total_count = 100000

for i in range(total_count):
    hands = []
    hands.append(userhand)
    # hands becomes a 2d array, with each row being a different person's hand, and row 0 being the user's hand.

    deck = pydealer.Deck()
    deck.shuffle()
    [deck.get(card) for card in userhand] #  deletes the user's cards from the deck

    river = [(pydealer.card.card_abbrev(card.value, card.suit)).lower() for card in deck.deal(5)]
    #  creates the river (5 cards on table)
    # "pydealer.card.card_abbrev(card.value, card.suit)" gives the card in format "10d" rather than "10 of Diamonds"

    [hands.append([(pydealer.card.card_abbrev(card.value, card.suit)).lower() for card in deck.deal(2)]) for player in range(numofplayers-1)]
    # deals 2 cards to each of the other players

    score = []

    for player in range(numofplayers):
        currhand = river.copy()
        currhand.extend(hands[player])
        score.append(evaluate_score(currhand))
    
    if score[0] == min(score):
        win_count += 1
    
    print(f"\r{win_count/total_count*100:.2f}%", end='', flush=True)

print(f"\rEstimated Winning Probability: {win_count/total_count*100:.2f}%")
