from tkinter import *
import pandas
import random

# ------------------- Global variables --------------------- #
BACKGROUND_COLOR = "#B1DDC6"
PRIMARY_LANGUAGE = "Nepali"
SECONDARY_LANGUAGE = "English"
current_card = {}
to_learn = {}

# --------------------- Language Converter ---------------- #


def radio_english():
    global PRIMARY_LANGUAGE, SECONDARY_LANGUAGE
    PRIMARY_LANGUAGE = "English"
    SECONDARY_LANGUAGE = "Nepali"


def radio_nepali():
    global PRIMARY_LANGUAGE, SECONDARY_LANGUAGE
    PRIMARY_LANGUAGE = "Nepali"
    SECONDARY_LANGUAGE = "English"
# -------------------- Flash card -------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    original_data = pandas.read_csv("data/nepali_natti.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def generate_card():
    global current_card, flip_timer

    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)

    canvas.itemconfig(canvas_img, image=front_img)
    canvas.itemconfig(card_title, text=PRIMARY_LANGUAGE, fill="black")
    canvas.itemconfig(card_word, text=current_card[PRIMARY_LANGUAGE], fill="black")

    flip_timer = window.after(3000, func=show_card)



def show_card():
    canvas.itemconfig(canvas_img, image=back_img)
    canvas.itemconfig(card_title, text=SECONDARY_LANGUAGE, fill="white")
    canvas.itemconfig(card_word, text=current_card[SECONDARY_LANGUAGE], fill="white")


def known_card():
    to_learn.remove(current_card)
    study_data = pandas.DataFrame(to_learn)
    study_data.to_csv("data/words_to_learn.csv", index=False)
    generate_card()

# -------------------- UI set-up --------------------------- #
window = Tk()
window.title("Natti Preparation(Nepali)")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=show_card)

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
# canvas image
back_img = PhotoImage(file="images/card_back.png")
front_img = PhotoImage(file="images/card_front.png")
canvas_img = canvas.create_image(400, 263, image=front_img)

# canvas text
card_title = canvas.create_text(400, 150, font=("Arial", 35, "italic"), text="Title")
card_word = canvas.create_text(400, 263, font=("Arial", 55, "bold"), text="word")
canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Button
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=generate_card)
wrong_button.grid(row=2, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=known_card)
right_button.grid(row=2, column=1)


# Radio button
radio_state = IntVar()
english_to_nepali = Radiobutton(text="English to Nepali", value=1, bg=BACKGROUND_COLOR, variable=radio_state, command=radio_english)
nepali_to_english = Radiobutton(text="Nepali to English", value=2, bg=BACKGROUND_COLOR, variable=radio_state, command=radio_nepali)
english_to_nepali.grid(row=0, column=0)
nepali_to_english.grid(row=0, column=1)

generate_card()
nepali_to_english.select()


window.mainloop()