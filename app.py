from tkinter import ttk
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Harmony")
        self.geometry("1200x800")
        self.resizable(True, True)

        HomePage(self)

class HomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.teachers = {}
        self.pack(fill=tk.BOTH)
        self.create_widgets()
        self.win_add_teacher = ''

    def add_teacher(self):
        self.teachers[self.ent_add_teacher.get()] =  []
        self.ent_add_teacher.delete(0, tk.END)
        self.combo["values"] = [teacher for teacher in self.teachers]
        self.combo.current(len(self.teachers)-1)

    def create_bar(self):
        self.bar = tk.Frame(self)
        self.bar.columnconfigure([0, 1, 2, 3], weight=1)
        self.bar.columnconfigure([0,1], minsize=400)
        self.bar.columnconfigure([2, 3], minsize=200)

        self.bar.rowconfigure([0, 1], weight=1, pad=20)
        self.bar.pack(expand=True, fill=tk.X)

        self.lbl_teacher = tk.Label(self.bar, text="Teacher")
        self.lbl_teacher.grid(row=0, column=0, sticky=tk.S)
        self.combo = ttk.Combobox(master=self.bar, state="readonly")
        self.combo["values"] = [teacher[0] for teacher in self.teachers]
        self.combo.grid(row=1, column=0)

        self.ent_add_teacher = tk.Entry(self.bar)
        self.ent_add_teacher.grid(row=1, column=2, sticky=tk.E)

        self.btn_add_teacher = ttk.Button(master=self.bar, text="Add teacher", command=self.add_teacher)
        self.btn_add_teacher.grid(row=1, column=3, sticky=tk.W)

    def create_widgets(self):
        self.create_bar()


if __name__ == "__main__":
    app = App()
    app.mainloop()