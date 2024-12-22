import tkinter as tk
from tkinter import messagebox
from db.db_connection import create_db_connection, read_query

class LoginWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Login")
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

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Here you should hash the password and compare it with the stored hash
        connection = create_db_connection("localhost", "root", "password", "exercise_db")
        query = f"SELECT is_admin FROM User WHERE Username='{username}' AND PasswordHash='{password}'"
        result = read_query(connection, query)

        if result:
            is_admin = result[0][0]
            self.master.destroy()
            from ui.main_window import MainWindow
            root = tk.Tk()
            app = MainWindow(root, is_admin=is_admin)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()



