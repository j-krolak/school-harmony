import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Harmony")
        self.geometry("1200x800")
        self.resizable(True, True)


if __name__ == "__main__":
    app = App()
    app.mainloop()