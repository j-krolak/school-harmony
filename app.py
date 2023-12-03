from tkinter import ttk
import tkinter as tk
from utils import *
import json
from tkinter import filedialog

DAYS = ["Pn", "Wt", "Śr", "Czw", "Pi"]
HOURS  = ["8:45-8:55", "9:40-9:50", "10:35-10:55", "11:40-11:50", "12:35-12:45", "13:30-13:35", "14:20-14:25", "15:10-15:15"]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Harmony")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.create_menu()

        self.home_page = HomePage(self)

    def save_file_as(self):
        self.home_page.save_file_as()

    def save_file(self):
        self.home_page.save_file()

    def open_file(self):
        self.home_page.open_file()

    def create_menu(self):
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Otwórz", command=self.open_file)
        self.filemenu.add_command(label="Zapisz", command=self.save_file)
        self.filemenu.add_command(label="Zapisz jako...", command=self.save_file_as)

        self.menubar.add_cascade(label="Plik", menu=self.filemenu)
        self.config(menu=self.menubar)

class HomePage(tk.Frame):
    def __init__(self, master):
        self.teachers = {}
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH)
        self.create_widgets()
        self.win_add_teacher = ''
        self.file_name = None
        self.popup_window = None
    def show_add_teacher_window(self):
        if self.popup_window is not None:
            self.popup_window.destroy()
        
        self.popup_window = tk.Toplevel(self)
        self.popup_window.title("Nowy nauczyciel")
        self.popup_window.geometry("200x100")
        self.popup_window.resizable(False, False)
        
        self.popup_label = tk.Label(self.popup_window, text="Imię i nazwisko")
        self.popup_label.pack(pady=5, expand=True)

        self.popup_entry = tk.Entry(self.popup_window)
        self.popup_entry.pack(pady=5, expand=True)

        self.popup_btn = tk.Button(self.popup_window, text="Dodaj", command=self.add_teacher)
        self.popup_btn.pack(pady=5, expand=True)

        self.popup_window.grab_set()

    def add_teacher(self):
        self.teachers[self.popup_entry.get()] =  []
        self.popup_entry.delete(0, tk.END)
        self.combo["values"] = [teacher for teacher in self.teachers]
        self.combo.current(len(self.teachers)-1)
        self.update_schedule()
    
    def show_popup_window(self, text):
        if self.popup_window is not None:
            self.popup_window.destroy()
        
        self.popup_window = tk.Toplevel(self)
        self.popup_window.title("Informacja")
        self.popup_window.geometry("200x100")
        self.popup_window.resizable(False, False)
        self.popup_label = tk.Label(self.popup_window, text=text)
        self.popup_label.pack(fill=tk.BOTH, expand=True)
        self.popup_window.grab_set()



    def save_file(self):
        if self.file_name is None:
            self.save_file_as()
            return
        with open(self.file_name, "w") as f:
            json.dump(self.teachers, f)
        self.show_popup_window("Zapisano plik")
        
    def save_file_as(self):
        self.file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        with open(self.file_name, "w") as f:
            json.dump(self.teachers, f)
        self.show_popup_window("Zapisano plik")
        

    def open_file(self):
        self.file_name = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if self.file_name is None:
            return
        with open(self.file_name, "r") as f:
            self.teachers = json.load(f)
        self.combo["values"] = [teacher for teacher in self.teachers]
        self.combo.current(len(self.teachers)-1)
        self.update_schedule()

    def create_bar(self):
        self.bar = tk.Frame(self)
        self.bar.columnconfigure([0, 1, 2, 3], weight=1)
        self.bar.columnconfigure([0,1], minsize=400)
        self.bar.columnconfigure([2, 3], minsize=200)

        self.bar.rowconfigure([0, 1], weight=1, pad=20)
        self.bar.pack(expand=True, fill=tk.X)

        self.lbl_teacher = tk.Label(self.bar, text="Nauczyciel")
        self.lbl_teacher.grid(row=0, column=0, sticky=tk.S)
        self.combo = ttk.Combobox(master=self.bar, state="readonly")
        self.combo.bind("<<ComboboxSelected>>", self.update_schedule)
        self.combo["values"] = [teacher[0] for teacher in self.teachers]
        self.combo.grid(row=1, column=0)

        # self.ent_add_teacher = tk.Entry(self.bar)
        # self.ent_add_teacher.grid(row=1, column=2, sticky=tk.E)

        self.btn_delete_teacher = ttk.Button(master=self.bar, text="Usuń nauczyciela")
        self.btn_delete_teacher.grid(row=1, column=2, sticky=tk.E)

        self.btn_add_teacher = ttk.Button(master=self.bar, text="Dodaj nauczyciela", command=self.show_add_teacher_window)
        self.btn_add_teacher.grid(row=1, column=3, sticky=tk.W)

    def handle_checkbox_change(self):
        if self.combo.get() == "":
            for day in range(5):
                for hour in range(8):
                    self.check_btns_state[day][hour].set(0)
            return
        self.teachers[self.combo.get()] = []
        for day in range(5):
            for hour in range(8):
                if self.check_btns_state[day][hour].get() == 1:
                    self.check_btns[day][hour].config(bg="green")
                    self.teachers[self.combo.get()].append(day * 8 + hour)
                else:
                    self.check_btns[day][hour].config(bg="red")
        
    def update_schedule(self, event=None):
        for day in range(5):
            for hour in range(8):
                if day * 8 + hour in self.teachers[self.combo.get()]:
                    self.check_btns_state[day][hour].set(1)
                    self.check_btns[day][hour].config(bg="green")
                else:
                    self.check_btns_state[day][hour].set(0)
                    self.check_btns[day][hour].config(bg="red")


    def create_schedule(self):
        self.frm_schedule = tk.Frame(self)
        self.frm_schedule.columnconfigure([i for i in range(9)], minsize=100, weight=1)
        self.frm_schedule.rowconfigure([i for i in range(6)], minsize=60, weight=1)
        self.frm_schedule.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    
        tk.Frame(master=self.frm_schedule, highlightbackground="black", highlightthickness=1).grid(row=0, column=0, sticky=tk.NSEW)

        # Create labels for days
        for i in range(5):
            tk.Label(text=f"{DAYS[i]}", master=self.frm_schedule, highlightbackground="black", highlightthickness=1).grid(row=i+1, column=0, sticky=tk.NSEW)


        # Create labels for hours
        for i in range(0,8):
            tk.Label(text=f"{i+1}\n{HOURS[i]}", master=self.frm_schedule, highlightbackground="black", highlightthickness=1).grid(row=0, column=i+1, sticky=tk.NSEW)

        # For each cell, create checkbox and frame

        self.check_btns = [[[] for _ in range(8)] for _ in range(5)]
        self.check_btns_state  = [[tk.IntVar() for _ in range(8)] for _ in range(5)]

        self.frm_check_btns = [[[] for _ in range(8)] for _ in range(5)]
        
        for day in range(5):
            for hour in range(8):
                self.frm_check_btns[day][hour] = tk.Frame(master=self.frm_schedule, highlightbackground="black", highlightthickness=1)
                self.check_btns[day][hour] = tk.Checkbutton(master=self.frm_check_btns[day][hour], variable=self.check_btns_state[day][hour], onvalue=1, offvalue=0, bg="red", command=self.handle_checkbox_change)

                self.check_btns[day][hour].pack(fill=tk.BOTH, expand=True)
                self.frm_check_btns[day][hour].grid(row=day+1, column=hour+1, sticky=tk.NSEW)
    
    def convert_teachers_to_teacher_data(self):
        return [TeacherData(teacher,self.teachers[teacher]) for teacher in self.teachers]
    
    def calculate_optimal_solution(self):
        if self.combo.get() == "":
            return
        teachers_data = self.convert_teachers_to_teacher_data()
        self.optimal_values = find_optimal_solution(teachers_data)
        display_solution(teachers_data, self.optimal_values)

    def create_calculate_btn(self):
        self.btn_calculate = ttk.Button(master=self, text="Oblicz", command=self.calculate_optimal_solution)
        self.btn_calculate.pack(pady=20)

    def create_widgets(self):
        self.create_bar()
        self.create_schedule()
        self.create_calculate_btn()


if __name__ == "__main__":
    app = App()
    app.mainloop()