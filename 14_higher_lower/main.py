from game_data import data
import random


def get_random_account(exclude=None):
    """Pick a random account, ensuring it's not the same as the excluded one."""
    account = random.choice(data)
    while account == exclude:
        account = random.choice(data)
    return account


def format_account(label, account):
    """Format account info for display."""
    return f"Compare {label}: {account['name']}, a {account['description']}, from {account['country']}."


def get_winner(a, b):
    """Return 'a' or 'b' based on who has more followers. Ties go to A."""
    if a['follower_count'] >= b['follower_count']:
        return 'a'
    return 'b'


def get_guess():
    """Get valid input from the user."""
    while True:
        guess = input("Who has more followers? Type 'A' or 'B': ").lower()
        if guess in ('a', 'b'):
            return guess
        print("Invalid input. Please type 'A' or 'B'.")


def play():
    score = 0
    current = get_random_account()

    while True:
        challenger = get_random_account(exclude=current)

        if score > 0:
            print(f"You're right! Current score: {score}")

        print(format_account("A", current))
        print('vs')
        print(format_account("B", challenger))

        guess = get_guess()
        winner = get_winner(current, challenger)

        if guess == winner:
            score += 1
            current = current if winner == 'a' else challenger
        else:
            print(f"Sorry, that's wrong. Final score: {score}")
            break

play()