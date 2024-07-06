import customtkinter
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import json
import os
from tkinter import messagebox

# Set appearance mode and default color theme
customtkinter.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Create main window
root = customtkinter.CTk()
root.geometry("600x500")

# Key file for encryption
key_file = 'secret.key'

# Function to generate AES key
def generate_aes_key(password):
    backend = default_backend()
    salt = b'salt_123'  # Replace with a secure salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 32 bytes = 256 bits
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = kdf.derive(password.encode())
    return key

# Load or generate encryption key
def load_key():
    if os.path.exists(key_file):
        with open(key_file, 'rb') as keyfile:
            return keyfile.read()
    else:
        password = input("Enter a password to generate the encryption key: ")  # Replace with your key generation logic
        key = generate_aes_key(password)
        with open(key_file, 'wb') as keyfile:
            keyfile.write(key)
        return key

key = load_key()
fernet = Fernet(key)

# Encrypt data
def encrypt_data(data):
    return fernet.encrypt(data.encode()).decode()  # Decode bytes to string

# Decrypt data
def decrypt_data(data):
    return fernet.decrypt(data.encode()).decode()

# Store credentials
def store_credentials(account_name, username, password, notes=""):
    credentials = {
        "account_name": account_name,
        "username": username,
        "password": encrypt_data(password),
        "notes": encrypt_data(notes)
    }
    all_credentials = load_credentials()
    all_credentials.append(credentials)
    save_credentials(all_credentials)

# Function to load stored credentials
def load_credentials():
    if os.path.exists('credentials.json'):
        with open('credentials.json', 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Function to save updated credentials to file
def save_credentials(credentials):
    with open('credentials.json', 'w') as file:
        json.dump(credentials, file)

# Login function
def login():
    username = entry1.get()
    password = entry2.get()
    credentials = load_credentials()
    for credential in credentials:
        if credential["username"] == username and decrypt_data(credential["password"]) == password:
            show_passwords(credentials)
            return
    messagebox.showerror("Login Failed", "Invalid username or password")

# Function to display passwords after login
def show_passwords(credentials):
    root.withdraw()  # Hide the main login window
    passwords_window = customtkinter.CTk()
    passwords_window.geometry("800x600")
    passwords_window.title("Password Manager")

    frame = customtkinter.CTkFrame(master=passwords_window)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    def add_password_window():
        passwords_window.withdraw()
        add_password_window = customtkinter.CTk()
        add_password_window.geometry("600x400")
        add_password_window.title("Add Password")

        add_frame = customtkinter.CTkFrame(master=add_password_window)
        add_frame.pack(pady=20, padx=60, fill="both", expand=True)

        def add_password():
            store_credentials(entry_account.get(), entry_username.get(), entry_password.get(), entry_notes.get())
            add_password_window.destroy()
            show_passwords(load_credentials())

        def back_to_main():
            add_password_window.destroy()
            passwords_window.deiconify()

        customtkinter.CTkLabel(master=add_frame, text="Account Name").pack(pady=6, padx=10)
        entry_account = customtkinter.CTkEntry(master=add_frame)
        entry_account.pack(pady=6, padx=10)

        customtkinter.CTkLabel(master=add_frame, text="Username").pack(pady=6, padx=10)
        entry_username = customtkinter.CTkEntry(master=add_frame)
        entry_username.pack(pady=6, padx=10)

        customtkinter.CTkLabel(master=add_frame, text="Password").pack(pady=6, padx=10)
        entry_password = customtkinter.CTkEntry(master=add_frame, show="*")
        entry_password.pack(pady=6, padx=10)

        customtkinter.CTkLabel(master=add_frame, text="Notes").pack(pady=6, padx=10)
        entry_notes = customtkinter.CTkEntry(master=add_frame)
        entry_notes.pack(pady=6, padx=10)

        customtkinter.CTkButton(master=add_frame, text="Submit", command=add_password).pack(pady=12, padx=10)
        customtkinter.CTkButton(master=add_frame, text="Back", command=back_to_main).pack(pady=12, padx=10)

        add_password_window.mainloop()

    # Function to delete password
    def delete_password(index):
        credentials = load_credentials()
        if index >= 0 and index < len(credentials):
            del credentials[index]
            save_credentials(credentials)
            refresh_password_list()
        else:
            messagebox.showerror("Delete Failed", "Invalid index for deletion")

    # Refresh password list function
    def refresh_password_list():
        # Clear existing widgets in the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Label for displaying stored passwords
        customtkinter.CTkLabel(master=frame, text="Stored Passwords", font=("Roboto", 24)).pack(pady=12, padx=10)

        # Button to add new password
        customtkinter.CTkButton(master=frame, text="Add Password", command=add_password_window).pack(pady=12, padx=10)

        # Display existing passwords
        credentials = load_credentials()
        for idx, credential in enumerate(credentials, start=1):
            account_name = credential["account_name"]
            username = credential["username"]
            password = decrypt_data(credential["password"])
            notes = decrypt_data(credential["notes"])

            credential_info = f"Account: {account_name}\nUsername: {username}\nPassword: {password}\nNotes: {notes}\n"
            customtkinter.CTkLabel(master=frame, text=credential_info).pack(pady=6, padx=10)

            # Button to delete password (lambda function to capture current index)
            customtkinter.CTkButton(master=frame, text=f"Delete {idx}",
                                    command=lambda idx=idx - 1: delete_password(idx - 1)).pack(pady=6, padx=10)

        # Button to logout
        customtkinter.CTkButton(master=frame, text="Logout", command=lambda: logout(passwords_window)).pack(pady=12,
                                                                                                            padx=10)
    # Initial refresh of password list
    refresh_password_list()

    passwords_window.mainloop()

# Logout function
def logout(window):
    window.destroy()
    root.deiconify()  # Show the main login window

# Registration function
def register():
    try:
        account_name = entry_account.get()
        username = entry_username.get()
        password = entry_password.get()
        notes = entry_notes.get()

        if not account_name or not username or not password:
            messagebox.showerror("Registration Failed", "All fields are required")
            return
        if len(password) < 8:
            messagebox.showerror("Registration Failed", "Password must be at least 8 characters long")
            return

        store_credentials(account_name, username, password, notes)
        messagebox.showinfo("Registration Successful", "You have successfully registered!")

        # Clear entry fields after successful registration
        entry_account.delete(0, 'end')
        entry_username.delete(0, 'end')
        entry_password.delete(0, 'end')
        entry_notes.delete(0, 'end')

    except Exception as e:
        messagebox.showerror("Registration Failed", f"An error occurred during registration: {e}")

# Frame for login system
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
checkbox.pack(pady=12, padx=10)

# Frame for registration
frame_register = customtkinter.CTkFrame(master=root)
frame_register.pack(pady=20, padx=60, fill="both", expand=True)

label_register = customtkinter.CTkLabel(master=frame_register, text="Register", font=("Roboto", 24))
label_register.pack(pady=12, padx=10)

entry_account = customtkinter.CTkEntry(master=frame_register, placeholder_text="Account Name")
entry_account.pack(pady=12, padx=10)

entry_username = customtkinter.CTkEntry(master=frame_register, placeholder_text="Username")
entry_username.pack(pady=12, padx=10)

entry_password = customtkinter.CTkEntry(master=frame_register, placeholder_text="Password", show="*")
entry_password.pack(pady=12, padx=10)

entry_notes = customtkinter.CTkEntry(master=frame_register, placeholder_text="Notes (Optional)")
entry_notes.pack(pady=12, padx=10)

button_register = customtkinter.CTkButton(master=frame_register, text="Register", command=register)
button_register.pack(pady=12, padx=10)

root.mainloop()
