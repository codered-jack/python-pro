from flask import Flask
import random

MIN_GUESS = 0
MAX_GUESS = 9
NUMBER_TO_GUESS = random.randint(MIN_GUESS, MAX_GUESS)
COLORS = [
    "72A0C1",
    "0048BA",
    "3B7A57",
    "007FFF",
    "2E5894",
    "54626F",
    "318CE7",
    "333399",
    "126180",
    "6699CC",
]

LOW_GIF = "https://media.giphy.com/media/XKvNduSwo0nEXsjZAg/giphy.gif"
HIGH_GIF = "https://media.giphy.com/media/oZ7zyrQwFaRyM/giphy.gif"
WIN_GIF = "https://media.giphy.com/media/pHZdGyFNp5sUXq4jp5/giphy-downsized-large.gif"
START_GIF = "https://media.giphy.com/media/Rs2QPsshsFI9zeT4Kn/giphy.gif"

app = Flask(__name__)


def random_color():
    """Return one random HEX color (without #), e.g. '007FFF'."""
    return random.choice(COLORS)


def render_message(message, gif_url):
    """Return formatted HTML response used by all routes."""
    return (
        f"<h1 style='color:#{random_color()}'>{message}</h1>"
        f"<img src='{gif_url}' width='300'>"
    )


@app.route("/")
def high_low_game():
    # Example: visit /5 to submit guess "5".
    return (
        f"<h1>Guess a number between {MIN_GUESS} and {MAX_GUESS}</h1>"
        f"<img src='{START_GIF}' width='300'>"
    )


@app.route("/<int:number>")
def check_number(number):
    if number < NUMBER_TO_GUESS:
        return render_message(f"{number} is too low!", LOW_GIF)
    if number > NUMBER_TO_GUESS:
        return render_message(f"{number} is too high!", HIGH_GIF)
    return render_message(f"{number} is woofderful!", WIN_GIF)


if __name__ == "__main__":
    app.run(debug=True)
