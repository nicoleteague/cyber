import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def generate_password_gui():
    # Create the main window
    root = tk.Tk()
    root.title("Password Generator")
    root.geometry("400x250")
    root.configure(bg="#F0F0F0")

    # Function to generate password and display in a messagebox
    def generate_and_display():
        password_length = length_scale.get()
        generated_password = generate_password(password_length)
        messagebox.showinfo("Generated Password", f"Your generated password:\n\n{generated_password}")

    # Frame for the GUI
    frame = tk.Frame(root, bg="#F0F0F0")
    frame.pack(pady=20)

    # Label and Scale for password length
    length_label = tk.Label(frame, text="Password Length:", bg="#F0F0F0", font=("Helvetica", 12))
    length_label.grid(row=0, column=0, padx=10, pady=10)

    length_scale = tk.Scale(frame, from_=4, to=32, orient=tk.HORIZONTAL, length=200, bg="#F0F0F0", troughcolor="#4CAF50")
    length_scale.set(12)  # default length
    length_scale.grid(row=0, column=1, padx=10, pady=10)

    # Generate button
    generate_button = tk.Button(frame, text="Generate Password", command=generate_and_display, bg="#4CAF50", fg="white", font=("Helvetica", 12), relief="flat")
    generate_button.grid(row=1, columnspan=2, padx=10, pady=20)

    # Run the Tkinter main loop
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    generate_password_gui()
