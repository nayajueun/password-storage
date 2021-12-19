from json import JSONDecodeError
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

YELLOW = "#FFEBA1"
VIOLET = "#6F69AC"
FONT_NAME = "Garamond"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

lower_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']
upper_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def password_generator():
    password = [random.choice(lower_case) for _ in range(8)] + [random.choice(upper_case) for _ in range(2)] \
               + [random.choice(numbers) for _ in range(3)] + [random.choice(symbols) for _ in range(2)]
    random.shuffle(password)

    password = "".join(password)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    global cur_data
    website = website_entry.get().upper()
    email = email_entry.get()
    password = password_entry.get()
    email_used = {
        "email": email
    }
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(message="Please make sure to fill out all the fields!")

    else:
        is_ok = messagebox.askokcancel(message=f"Would you like to store these details for {website}?\n"
                                               f"Email: {email}\nPassword:{password}")

        if is_ok:
            pyperclip.copy(password)
            messagebox.showinfo(message="Password has been copied to clipboard.")
            try:
                with open("password-saved.json", "r") as data:
                    cur_data = json.load(data)
                    cur_data.update(new_data)
                    cur_data.update(email_used)

            except (JSONDecodeError, FileNotFoundError) as e:
                cur_data = new_data
                cur_data.update(email_used)

            finally:
                with open("password-saved.json", "w") as data:
                    json.dump(cur_data, data, indent=3)

        website_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def search():
    website = website_entry.get().upper()
    if len(website) == 0:
        messagebox.showinfo(message="Please make sure to fill out the Website field!")
    else:
        try:
            with open("password-saved.json", "r") as data:
                cur_data = json.load(data)
                email = cur_data[website]["email"]
                password = cur_data[website]["password"]
                messagebox.showinfo(message=f"Website: {website.capitalize()}\nEmail: {email}\nPassword: {password}\n"
                                                f"Password has been copied to clipboard.")
                pyperclip.copy(password)

        except (KeyError, FileNotFoundError, JSONDecodeError) as e:
            messagebox.showinfo(message=f"You have not stored password for {website.capitalize()}.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("password manager")
window.config(padx=30, pady=30, bg=YELLOW)

unlock_pic = PhotoImage(file="unlock-icon.png").subsample(2, 2)

canvas = Canvas(width=128, height=128, bg=YELLOW, highlightthickness=0)  # size of the png file
canvas.create_image(64, 64, image=unlock_pic)
# # two first arguments representing the position of the image in the canvas.
# # image argument takes PhotoImage object
canvas.grid(column=1, row=0)

space = Label(bg=YELLOW)
space.grid(column=0, row=1)

website_label = Label(text="Website:", font=(FONT_NAME, 12, "bold"), bg=YELLOW)
website_label.grid(row=2, column=0)
website_entry = Entry(width=23)
website_entry.grid(column=1, row=2)
website_entry.focus()

email_label = Label(text="Email / Username:", font=(FONT_NAME, 12, "bold"), bg=YELLOW)
email_label.grid(column=0, row=3)
email_entry = Entry(width=41)
email_entry.grid(column=1, row=3, columnspan=2)
try:
    with open("password-saved.json", "r") as data:
        cur_data = json.load(data)
        email = cur_data["email"]

except (TypeError, JSONDecodeError, FileNotFoundError) as e:
    pass
else:
    email_entry.insert(0, email)


password_label = Label(text="Password:", font=(FONT_NAME, 12, "bold"), bg=YELLOW)
password_label.grid(column=0, row=4)
password_entry = Entry(width=23)
password_entry.grid(column=1, row=4)

generator = Button(width=14, text="Generate Password", command=password_generator)
generator.grid(column=2, row=4)

search = Button(width=14, text="Search", command=search)
search.grid(column=2, row=2)

add_button = Button(width=35, text="Add", command=save_password)
add_button.grid(column=1, row=5, columnspan=2)

window.mainloop()
