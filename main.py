from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_TITLE = ("Ariel", 40, "italic")
FONT_WORD = ("Ariel", 60, "bold")

# Program functions
try:
    words_to_learn = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    words_to_learn = pandas.read_csv("./data/french_words.csv")
finally:
    to_learn = words_to_learn.to_dict(orient="records")

current_card = {}


def random_next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def card_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.csv", index=False)
    random_next_card()


# UI Setup
window = Tk()
window.title("French-English Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=900, height=550, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_image = canvas.create_image(460, 270, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=3)

card_title = canvas.create_text(450, 150, text="French", font=FONT_TITLE, anchor="center")
card_word = canvas.create_text(450, 260, text="word", font=FONT_WORD, anchor="center")

# Buttons
right_img = PhotoImage(file="./images/right.png")
button_right = Button(image=right_img, highlightthickness=0, command=card_known)
button_right.grid(row=1, column=2)

wrong_img = PhotoImage(file="./images/wrong.png")
button_wrong = Button(image=wrong_img, highlightthickness=0, command=random_next_card)
button_wrong.grid(row=1, column=0)

random_next_card()
window.mainloop()
