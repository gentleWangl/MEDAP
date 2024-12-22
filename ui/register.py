import tkinter as tk
from tkinter import messagebox
from db.db_connection import create_db_connection, execute_query

class RegisterWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Register")
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        self.register_button = tk.Button(self, text="Register", command=self.register)
        self.register_button.grid(row=3, columnspan=2, pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        # Here you should hash the password before storing it
        connection = create_db_connection("localhost", "root", "password", "exercise_db")
        query = f"INSERT INTO User (Username, PasswordHash, Email) VALUES ('{username}', '{password}', '{email}')"
        execute_query(connection, query)

        messagebox.showinfo("Success", "Registration successful!")
        self.master.destroy()
        from ui.login import LoginWindow
        root = tk.Tk()
        app = LoginWindow(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterWindow(root)
    root.mainloop()



