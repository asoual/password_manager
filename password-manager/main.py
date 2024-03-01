from tkinter import *
import json
from tkinter import messagebox
import random
from letter_numbers_symbols import *
import pyperclip

FONT_NAME = "Times New Roman"
FONT_SIZE = 12

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = password_letters + password_symbols + password_numbers
    
    random.shuffle(password_list)
    password = ""
    for char in password_list:
        password += char
        
    if len(password_entry.get())==0:
        password_entry.insert(0, password)
        pyperclip.copy(password)
    else:
        password_entry.delete(0,END)
        password_entry.insert(0, password)
        pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email_username = email_username_entry.get()
    password = password_entry.get()
    data_dict = {website:{"Email or Username":email_username, "Password":password,}}
    
    if not website or not email_username or not password:
        messagebox.showerror(title="Empty fields",message="Please fill all the fields.")
        return
    else:
        try:
            with open("password.json","r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("password.json", "w") as file:
                json.dump(data_dict, file, indent=4)
        else:
            data.update(data_dict)
            with open("password.json","w") as file:
                json.dump(data, file, indent=4)
                
        finally:
            messagebox.showinfo("Success", "Password saved successfully")
            website_entry.delete(0,END)
            email_username_entry.delete(0,END)
            password_entry.delete(0,END)
# ---------------------------- SEARCH ------------------------------- #
def search():
    website = website_entry.get()
    try:
        with open("password.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message=" No Data File Found")
    else:
        if website in data:
            email_username = data[website]["Email or Username"]
            password = data[website]["Password"]
            messagebox.showinfo(title=website, message=f"Email or Username: {email_username} \n Password: {password}")
        else:
            messagebox.showerror(title="Error", message=f"No details for {website} exists.")
# ---------------------------- DELETE ROW ------------------------------- #
def delete(key):
    with open("password.json", "r") as file:
        data = json.load(file)
    if key in data:
        del data[key]
        with open("password.json", "w") as file:
            json.dump(data, file, indent=4)
        messagebox.showinfo(title="Row Deleted!", message="Row Deleted!")
        
# ---------------------------- VIEW SAVED PASSWORD ------------------------------- #
def format_data(new_window):
    pass_buttons = []
    passwords = []
    emails = []
    websites = []
    web_y = 30
    em_y = 30
    pas_y = 30
    pass_btn_width = 0
    try:
        with open("password.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        if_no = Label(new_window, text="No Saved Data or Passwords found\nAdd Passwords to view them.", bg="white")
        if_no.place(x=110, y=90)
    else:
        for website in data:
            websites.append(website)
            emails.append(data[website]["Email or Username"])
            passwords.append(data[website]["Password"])
        for passw in passwords:
            if len(passw) > pass_btn_width:
                pass_btn_width = len(passw)
        for website in websites:
            websites_label = Label(new_window, text=website, bg="white")
            websites_label.place(x=10, y=web_y)
            key_to_delete = website
            delete_button = Button(new_window, text="Delete", height=1, bg="red", fg="white",command=lambda: delete(key_to_delete))
            delete_button.place(x=450, y=web_y)
            web_y += 30
        for email in emails:
            emails_label = Label(new_window, text=email, bg="white")
            emails_label.place(x=150, y=em_y)
            em_y += 30

        def copy_pass(password_to_copy):
            pyperclip.copy(password_to_copy)

        for password in passwords:
            pas_button = Button(new_window, text=password, height=1, width=pass_btn_width, bg="white")
            pas_button.config(command=lambda password_arg=pas_button: copy_pass(password_arg.cget('text')))
            pas_button.place(x=300, y=pas_y)
            pas_y += 30
            pass_buttons.append(pas_button)

def view_saved():
    new_window = Tk()
    new_window.geometry("550x200")
    new_window.config(bg="white")
    new_window.title("Saved Passwords")
    web_label = Label(new_window, text="Website", fg="red", font=("aerial", 10, "bold"), bg="white")
    web_label.place(x=10, y=10)
    email_user_label = Label(new_window, text="Email/Username", fg="red", font=("aerial", 10, "bold"), bg="white")
    email_user_label.place(x=150, y=10)
    pas_label = Label(new_window, text="Password", fg="red", font=("aerial", 10, "bold"), bg="white")
    pas_label.place(x=300, y=10)
    format_data(new_window)
    
    new_window.mainloop()
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx = 50, pady=50, bg="white", highlightthickness=0)

canvas = Canvas(width = 200, height =189, bg="white",highlightthickness=0)
password_img = PhotoImage(file="logo.png")
canvas.create_image(100,100,image = password_img)
canvas.grid(column=1,row=0)

website_label = Label(text="Website:",bg="white",highlightthickness=0, font=(FONT_NAME, FONT_SIZE, "normal"))
website_label.grid(column=0, row=1)

website_entry = Entry(width=50)
website_entry.grid(column=1, row=1,sticky="EW")
website_entry.focus()

search_button = Button(text="Search", font=(FONT_NAME, 10),command=search)
search_button.grid(column=2,row=1, sticky="EW")

email_username_label =Label(text="Email/Username:",bg="white",highlightthickness=0,font=(FONT_NAME, FONT_SIZE))
email_username_label.grid(column=0, row=2)

email_username_entry = Entry(width=50)
email_username_entry.grid(column=1,row=2,columnspan=2, sticky="EW")

password_label = Label(text="Password:",bg="white",highlightthickness=0,font=(FONT_NAME, FONT_SIZE))
password_label.grid(column=0, row=3)

password_entry = Entry(width=31)
password_entry.grid(column=1,row=3, sticky="EW")

generate_password_button= Button(text="Generate Password",font=(FONT_NAME, 10),command=password_generator)
generate_password_button.grid(column=2,row=3, sticky="EW")

add_button = Button(text="Add",width=42,font=(FONT_NAME,10),command=save_password)
add_button.grid(column=1,row=4,columnspan=2, sticky="EW")

view_saved_password = Button(text="View Saved Password",width=42,font=(FONT_NAME,10),command=view_saved)
view_saved_password.grid(column=1,row=5,columnspan=2, sticky="EW")

window.mainloop()