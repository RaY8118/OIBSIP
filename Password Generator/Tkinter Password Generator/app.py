import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

BG_COLOR = "#f0f0f0"
FG_COLOR = "#333333"
ACCENT_COLOR = "#007bff"


def generate_password():
    length = length_var.get()
    include_upper = upper_var.get()
    include_lower = lower_var.get()
    include_numbers = number_var.get()
    include_special = special_var.get()
    exclude_chars = exclude_var.get()

    if length < 8:
        messagebox.showwarning(
            "Warning", "Password length should be at least 8 characters")
        return

    if not (include_upper or include_lower or include_numbers or include_special):
        messagebox.showwarning("Warning", "Select at least one character type")
        return

    characters = ""
    if include_upper:
        characters += string.ascii_uppercase
    if include_lower:
        characters += string.ascii_lowercase
    if include_numbers:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    characters = ''.join([c for c in characters if c not in exclude_chars])

    if not characters:
        messagebox.showwarning(
            "Warning", "Character pool is empty after excluding characters.")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    while True:
        if (include_upper and not any(c in string.ascii_uppercase for c in password)):
            password = ''.join(random.choice(characters)
                               for _ in range(length))
            continue
        if (include_lower and not any(c in string.ascii_lowercase for c in password)):
            password = ''.join(random.choice(characters)
                               for _ in range(length))
            continue
        if (include_numbers and not any(c in string.digits for c in password)):
            password = ''.join(random.choice(characters)
                               for _ in range(length))
            continue
        if (include_special and not any(c in string.punctuation for c in password)):
            password = ''.join(random.choice(characters)
                               for _ in range(length))
            continue
        break

    password_var.set(password)


def copy_to_clipboard():
    pyperclip.copy(password_var.get())
    messagebox.showinfo("Copied", "Password copied to clipboard")


root = tk.Tk()
root.title("Advanced Password Generator")
root.configure(bg=BG_COLOR)

length_var = tk.IntVar(value=12)
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
number_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)
exclude_var = tk.StringVar(value="")
password_var = tk.StringVar()

tk.Label(root, text="Password Length:", bg=BG_COLOR,
         fg=FG_COLOR).grid(row=0, column=0, padx=10, pady=10)
length_entry = tk.Entry(root, textvariable=length_var,
                        bg=BG_COLOR, fg=FG_COLOR, width=10)
length_entry.grid(row=0, column=1, padx=10, pady=10)

font_large = ('Helvetica', 12)
upper_checkbutton = tk.Checkbutton(
    root, text="Include Uppercase Letters", variable=upper_var, bg=BG_COLOR, fg=FG_COLOR, font=font_large)
upper_checkbutton.grid(row=1, column=0, padx=10, pady=5)
lower_checkbutton = tk.Checkbutton(
    root, text="Include Lowercase Letters", variable=lower_var, bg=BG_COLOR, fg=FG_COLOR, font=font_large)
lower_checkbutton.grid(row=1, column=1, padx=10, pady=5)
number_checkbutton = tk.Checkbutton(
    root, text="Include Numbers", variable=number_var, bg=BG_COLOR, fg=FG_COLOR, font=font_large)
number_checkbutton.grid(row=2, column=0, padx=10, pady=5)
special_checkbutton = tk.Checkbutton(
    root, text="Include Special Characters", variable=special_var, bg=BG_COLOR, fg=FG_COLOR, font=font_large)
special_checkbutton.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Exclude Characters:", bg=BG_COLOR,
         fg=FG_COLOR).grid(row=3, column=0, padx=10, pady=5)
exclude_entry = tk.Entry(root, textvariable=exclude_var,
                         bg=BG_COLOR, fg=FG_COLOR, width=30)
exclude_entry.grid(row=3, column=1, padx=10, pady=5)

generate_button = tk.Button(root, text="Generate Password",
                            command=generate_password, bg=ACCENT_COLOR, fg="white", width=20, height=2)
generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

password_entry = tk.Entry(root, textvariable=password_var,
                          width=50, state='readonly', bg=BG_COLOR, fg=FG_COLOR)
password_entry.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard,
                        bg=ACCENT_COLOR, fg="white", width=20, height=2)
copy_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
