# import required modules
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # randomly choose quantity and characters for password
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    # password list with all chosen characters
    password_list = password_letters + password_numbers + password_symbols
    # shuffle order of characters in password
    shuffle(password_list)

    # add all shuffled password characters to string to change from list format
    shuffled_password = "".join(password_list)

    pass_entry.delete(0, END) # clear entry if anything written
    pass_entry.insert(0, shuffled_password) # write in generated password

    # copy generated password to clipboard
    pyperclip.copy(shuffled_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    # get hold of inputs
    website = web_entry.get()
    username = user_entry.get()
    password = pass_entry.get()

    # add inputs to dictionary
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    # check if user left any entries blank
    left_blanks = False
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        left_blanks = True

    if left_blanks:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

    else:
        # confirm user is satisfied with inputs
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nUsername: {username}\nPassword: {password}\nIs it okay to save?")

        if is_ok:
            # write inputs to file
            try:
                with open("data.json", mode="r") as data_file:
                    # reading old data
                    data = json.load(data_file)

            # if file does not exist, create file
            except FileNotFoundError:
                with open("data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            # if file already exists, add new data to old data and save to file
            else:
                data.update(new_data)
                with open("data.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)  # data to add, file to add to, # spaces to indent data

            finally:
                # clear current inputs from window
                web_entry.delete(0, END) # start from 0th position until end of entry
                user_entry.delete(0, END)
                pass_entry.delete(0, END)

# ---------------------- SEARCH FOR PASSWORD ------------------------- #
def search():
    website = web_entry.get()

    try:
        with open("data.json") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message=f"No data file found. Try saving some data first.")

    else:
        if website in data:
            username = data[website]["username"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Username: {username}\nPassword: {password}")

        else:
            messagebox.showinfo(title="Error", message=f"There is no username/password saved for {website}")


# ---------------------------- UI SETUP ------------------------------- #
# create screen window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# canvas to add background image
canvas = Canvas(width=200, height=200, highlightthickness=0) # size, background colour, remove canvas outline
# read in tomato image to create photo Image object to input into create_image method
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo) # place in center of canvas
canvas.grid(row=0, column=1)

# labels
website_label = Label(text="Website: ")
website_label.grid(row=1, column=0)

email_username_label = Label(text="Email/Username: ")
email_username_label.grid(row=2, column=0)

password_label = Label(text="Password: ")
password_label.grid(row=3, column=0)

# entries
web_entry = Entry(width=32)
web_entry.grid(row=1, column=1)
web_entry.focus() # start cursor in this entry

user_entry = Entry(width=51)
user_entry.grid(row=2, column=1, columnspan=2)

pass_entry = Entry(width=32)
pass_entry.grid(row=3, column=1)

# buttons
search_button = Button(text="Search", command=search, width=15)
search_button.grid(row=1, column=2)

generate_pass_button = Button(text="Generate password", command=generate_password)
generate_pass_button.grid(row=3, column=2)

add_button = Button(text="Add", command=save_password, width=44)
add_button.grid(row=4, column=1, columnspan=2)

# keep screen window open
window.mainloop()
