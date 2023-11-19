import math
import tkinter as tk
from tkinter import messagebox

class QuadraticCalculatorPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Quadratic Calculator")
        self.geometry("400x400")
        self.configure(bg="#E6F5F5")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.label_a = tk.Label(self, text="Coefficient of x^2 (a):", bg="#E6F5F5")
        self.entry_a = tk.Entry(self)

        self.label_b = tk.Label(self, text="Coefficient of x (b):", bg="#E6F5F5")
        self.entry_b = tk.Entry(self)

        self.label_c = tk.Label(self, text="Constant term (c):", bg="#E6F5F5")
        self.entry_c = tk.Entry(self)

        self.entry_fields = [self.entry_a, self.entry_b, self.entry_c]

        self.solve_button = tk.Button(self, text="Solve", command=self.solve_quadratic, bg="#00A0A0", fg="white")
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_input, bg="#FFA500", fg="white")
        self.back_button = tk.Button(self, text="Back to Menu", command=self.on_back, bg="#FF6060", fg="white")

        self.result_label = tk.Label(self, text="", font=("Helvetica", 14), bg="#E6F5F5")

        self.label_a.grid(row=0, column=0, padx=10, sticky="e")
        self.entry_a.grid(row=0, column=1, padx=10)

        self.label_b.grid(row=1, column=0, padx=10, sticky="e")
        self.entry_b.grid(row=1, column=1, padx=10)

        self.label_c.grid(row=2, column=0, padx=10, sticky="e")
        self.entry_c.grid(row=2, column=1, padx=10)

        self.solve_button.grid(row=3, column=0, pady=15, padx=5, sticky="e")
        self.clear_button.grid(row=3, column=1, pady=15, padx=5, sticky="w")
        self.back_button.grid(row=3, column=1, pady=15, padx=5, sticky="e")

        self.result_label.grid(row=4, columnspan=3, pady=10)

        self.keypad_frame = tk.Frame(self, bg="#E6F5F5")
        self.keypad_frame.grid(row=5, columnspan=2, pady=10)

        keypad_symbols = [
            "7", "8", "9",
            "4", "5", "6",
            "1", "2", "3",
            "0", ".", "-"
        ]

        row, col = 0, 0
        for symbol in keypad_symbols:
            button = tk.Button(self.keypad_frame, text=symbol, command=lambda s=symbol: self.on_keypad_button_click(s))
            button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.delete_button = tk.Button(self.keypad_frame, text="del", command=self.delete_last_character)
        self.delete_button.grid(row=4, column=1, padx=5, pady=5)

    def solve_quadratic(self):
        try:
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            c = float(self.entry_c.get())

            solutions = self.quadratic_solver(a, b, c)

            if isinstance(solutions, tuple):
                solution_text = f"Root 1: {solutions[0]:.4f}, Root 2: {solutions[1]:.4f}"
            else:
                solution_text = f"Root: {solutions:.4f}"

            self.result_label.config(text=solution_text, fg="#007F7F")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numerical coefficients.")

    def clear_input(self):
        for entry in self.entry_fields:
            entry.delete(0, tk.END)
        self.result_label.config(text="", fg="#000000")

    def quadratic_solver(self, a, b, c):
        discriminant = b**2 - 4*a*c

        if discriminant > 0:
            root1 = (-b + math.sqrt(discriminant)) / (2*a)
            root2 = (-b - math.sqrt(discriminant)) / (2*a)
            return root1, root2
        elif discriminant == 0:
            root = -b / (2*a)
            return root
        else:
            real_part = -b / (2*a)
            imaginary_part = math.sqrt(abs(discriminant)) / (2*a)
            root1 = complex(real_part, imaginary_part)
            root2 = complex(real_part, -imaginary_part)
            return root1, root2

    def on_keypad_button_click(self, symbol):
        current_entry = self.focus_get()
        if current_entry in self.entry_fields:
            current_text = current_entry.get()
            if symbol == "del":
                current_entry.delete(len(current_text) - 1, tk.END)
            else:
                current_entry.delete(0, tk.END)
                current_entry.insert(tk.END, current_text + symbol)

    def delete_last_character(self):
        current_entry = self.focus_get()
        if current_entry in self.entry_fields:
            current_text = current_entry.get()
            current_entry.delete(len(current_text) - 1, tk.END)

    def on_back(self):
        self.destroy()

    def on_close(self):
        self.master.show_menu()
        self.destroy()


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Menu")
        self.geometry("400x400")
        self.configure(bg="#E6F5F5")

        self.calculator_button = tk.Button(self, text="Calculator", command=self.show_calculator, bg="#00A0A0", fg="white")
        self.learn_button = tk.Button(self, text="Learn Quadratic Formula", command=self.show_education, bg="#00A0A0", fg="white")

        self.calculator_button.pack(pady=20)
        self.learn_button.pack()

        self.current_page = None

    def show_calculator(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = QuadraticCalculatorPage(self)

    def show_education(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = QuadraticFormulaPage(self)

    def show_menu(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = None

class QuadraticFormulaPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Quadratic Formula")
        self.geometry("400x400")
        self.configure(bg="#E6F5F5")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.text = tk.Text(self, bg="#E6F5F5", height=15, width=48)
        self.text.insert(tk.END, "The quadratic formula is used to solve quadratic equations of the form:\n\n")
        self.text.insert(tk.END, "ax^2 + bx + c = 0\n\n")
        self.text.insert(tk.END, "The solutions for x are given by:\n\n")
        self.text.insert(tk.END, "x = (-b ± √(b² - 4ac)) / 2a\n\n")
        self.text.insert(tk.END, "Where 'a', 'b', and 'c' are coefficients of the quadratic equation.")
        self.text.config(state=tk.DISABLED)

        self.back_button = tk.Button(self, text="Back to Menu", command=self.on_back, bg="#FF6060", fg="white")

        self.text.pack(padx=10, pady=10)
        self.back_button.pack(pady=15)

    def on_back(self):
        self.destroy()

    def on_close(self):
        self.master.show_menu()
        self.destroy()

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
