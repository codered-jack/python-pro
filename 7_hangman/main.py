import random
from hangman_words import word_list
from hangman_art import stages, logo

game_over = False
lives = 6
display = []

print(logo)
chosen_word = random.choice(word_list)
word_length = len(chosen_word)

print(chosen_word)

for i in range(word_length):
    display.append("_")

while not game_over:
    guess = input("Guess a letter: ").lower()
    if guess in display:
        print(f"You already guessed {guess} letter")

    for index in range(word_length):
        if guess == chosen_word[index]:
            display[index] = guess

    if guess not in chosen_word:
        lives -= 1
        if 3 <= lives <= 5:
            print(
                f"Eep, you guessed: {guess}, that's not in the word. 😱 You have {lives} chances left before the hangman makes his final judgment.")
        elif 1 <= lives < 3:
            print(
                f"You guessed: {guess}, that's not in the word. You have {lives} chances left 😢...the hangman is coming!!!")
        elif lives == 0:
            print(f"Oh no. The hangman got you! The answer was: {chosen_word}.😭😭")
            game_over = True

    print(f"{' '.join(display)}")

    #Check if user has got all letters.
    if "_" not in display:
        game_over = True
        print("You Win")


    print(stages[lives])