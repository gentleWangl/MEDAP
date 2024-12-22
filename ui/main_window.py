import tkinter as tk
from tkinter import ttk
from db.db_connection import create_db_connection, read_query, execute_query

class MainWindow(tk.Frame):
    def __init__(self, master=None, is_admin=False):
        super().__init__(master)
        self.master = master
        self.is_admin = is_admin
        self.master.title("Exercise Management System")
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        if self.is_admin:
            self.admin_menu()
        else:
            self.user_menu()

    def admin_menu(self):
        self.exercise_listbox = tk.Listbox(self, height=15, width=80)
        self.exercise_listbox.pack(pady=10)

        self.load_exercises()

        self.add_button = tk.Button(self, text="Add Exercise", command=self.add_exercise)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(self, text="Edit Exercise", command=self.edit_exercise)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self, text="Delete Exercise", command=self.delete_exercise)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.statistics_button = tk.Button(self, text="Statistics", command=self.statistics)
        self.statistics_button.pack(side=tk.LEFT, padx=5)

    def user_menu(self):
        self.exercise_listbox = tk.Listbox(self, height=15, width=80)
        self.exercise_listbox.pack(pady=10)

        self.load_exercises()

        self.details_button = tk.Button(self, text="View Details", command=self.view_details)
        self.details_button.pack(pady=10)

    def load_exercises(self):
        connection = create_db_connection("localhost", "root", "password", "exercise_db")
        query = "SELECT ExerciseName FROM Exercise"
        exercises = read_query(connection, query)
        for exercise in exercises:
            self.exercise_listbox.insert(tk.END, exercise[0])

    def add_exercise(self):
        # Placeholder for adding an exercise
        pass

    def edit_exercise(self):
        # Placeholder for editing an exercise
        pass

    def delete_exercise(self):
        # Placeholder for deleting an exercise
        pass

    def statistics(self):
        # Placeholder for showing statistics
        pass

    def view_details(self):
        selected_index = self.exercise_listbox.curselection()
        if not selected_index:
            return

        selected_exercise = self.exercise_listbox.get(selected_index)
        connection = create_db_connection("localhost", "root", "password", "exercise_db")
        query = f"SELECT * FROM Exercise WHERE ExerciseName='{selected_exercise}'"
        details = read_query(connection, query)[0]

        detail_window = tk.Toplevel(self.master)
        detail_window.title("Exercise Details")

        labels = [
            "ExerciseID", "Country", "ExerciseName", "ForeignName", "Organization",
            "StartTime", "EndTime", "ExerciseIntro", "ExerciseProcess", "MainPurpose"
        ]

        for i, label_text in enumerate(labels):
            label = tk.Label(detail_window, text=f"{label_text}: {details[i]}")
            label.pack(anchor='w', padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root, is_admin=True)
    root.mainloop()



