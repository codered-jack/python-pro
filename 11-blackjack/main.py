import random

def deal_card(cards):
    """Deal a random card from the deck."""
    return random.choice(cards)

def adjust_aces(hand):
    """Convert aces from 11 to 1 if hand is over 21."""
    while 11 in hand and sum(hand) > 21:
        hand.remove(11)
        hand.append(1)

def is_blackjack(hand):
    """Natural blackjack = exactly 2 cards totaling 21."""
    return len(hand) == 2 and sum(hand) == 21

def blackjack():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    player_cards = [deal_card(cards) for _ in range(2)]
    computer_cards = [deal_card(cards) for _ in range(2)]

    adjust_aces(player_cards)
    adjust_aces(computer_cards)

    print(f"Your cards: {player_cards}, score: {sum(player_cards)}")
    print(f"Computer's first card: {computer_cards[0]}")

    # Check for natural blackjack
    if is_blackjack(player_cards) and is_blackjack(computer_cards):
        print(f"Computer's hand: {computer_cards}")
        print("Both have Blackjack! It's a draw!")
        return
    elif is_blackjack(player_cards):
        print("Blackjack! You win!")
        return
    elif is_blackjack(computer_cards):
        print(f"Computer's hand: {computer_cards}. Computer has Blackjack! You lose.")
        return

    # Player's turn
    game_over = False
    while not game_over:
        choice = input("Type 'y' to get another card, type 'n' to pass: ")
        if choice == "y":
            player_cards.append(deal_card(cards))
            adjust_aces(player_cards)
            print(f"Your cards: {player_cards}, score: {sum(player_cards)}")
            if sum(player_cards) > 21:
                print("You went bust! Computer wins.")
                return
        else:
            game_over = True

    # Computer's turn (must draw on 16 or below)
    while sum(computer_cards) < 17:
        computer_cards.append(deal_card(cards))
        adjust_aces(computer_cards)

    player_score = sum(player_cards)
    computer_score = sum(computer_cards)

    print(f"Your final hand: {player_cards}, score: {player_score}")
    print(f"Computer's final hand: {computer_cards}, score: {computer_score}")

    if computer_score > 21:
        print("Computer went bust! You win!")
    elif computer_score > player_score:
        print("Computer wins!")
    elif player_score > computer_score:
        print("You win!")
    else:
        print("It's a draw!")

# Game loop
while True:
    play = input("Do you want to play Blackjack? Type 'y' or 'n': ")
    if play != "y":
        print("Goodbye!")
        break
    blackjack()