from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flash Card App")
window.config(padx=50,  pady=50, bg=BACKGROUND_COLOR)


current_card = {}
to_learn = []

try:
    words = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = words.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    if not to_learn:
        canvas.itemconfig(card_title, text="Done!", fill="black")
        canvas.itemconfig(card_word, text="No cards left", fill="black")
        canvas.itemconfig(current_image, image=front_img)
        return
    current_card = random.choice(to_learn)
    french_word = current_card['French']
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=french_word, fill="black")
    canvas.itemconfig(current_image, image=front_img)
    flip_timer = window.after(3000, flip_card)


def is_known():
    if current_card in to_learn:
        to_learn.remove(current_card)
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def flip_card():
    global current_card
    english_word = current_card['English']
    canvas.itemconfig(card_title, text="English", fill="#fff")
    canvas.itemconfig(card_word, text=english_word, fill="#fff")
    canvas.itemconfig(current_image, image=back_img)


flip_timer = window.after(3000, flip_card)


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
back_img = PhotoImage(file="images/card_back.png")
front_img = PhotoImage(file="./images/card_front.png")
current_image = canvas.create_image(400, 263, image=front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))


canvas.grid(column=0, row=0, columnspan=2)

#BUTTONS

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=0, row=1)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

next_card()

window.mainloop()
