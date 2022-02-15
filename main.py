from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
data = {}

try:
    initial_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    org_data = pandas.read_csv("data/french_words.csv")
    data = org_data.to_dict(orient='records')
else:
    data = initial_data.to_dict(orient='records')


def read_csv_file():
    global current_card, flip_timer, data
    window.after_cancel(flip_timer)
    current_card = random.choice(data)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=current_card['French'], fill="black")
    canvas.itemconfig(first_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=current_card['English'], fill="white")
    canvas.itemconfig(first_image, image=card_back)


def is_known():
    data.remove(current_card)
    data_to_save = pandas.DataFrame(data)
    data_to_save.to_csv("data/words_to_learn.csv", index=False)
    read_csv_file()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)
# Canvas
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
first_image = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
# Text
language = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 253, text="", font=("Arial", 60, "bold"))
# Buttons
inc_image = PhotoImage(file="images/wrong.png")
incorrect_button = Button(image=inc_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=read_csv_file)
incorrect_button.grid(column=0, row=1)
cor_image = PhotoImage(file="images/right.png")
correct_button = Button(image=cor_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known)
correct_button.grid(column=1, row=1)

read_csv_file()
window.mainloop()
