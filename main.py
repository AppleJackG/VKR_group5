from tkinter import filedialog
from tkinter import messagebox
import customtkinter as tk
import time
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

tk.set_appearance_mode("dark")

root = tk.CTk(fg_color=('#F1E4E8', '#002029'))
root.title('Расчет кинетической кривой')
root.iconbitmap('logo.ico')
root.geometry('1400x800+200+50')
root.minsize(1400, 700)

matplotlib.use('TkAgg')
plt.style.use('seaborn-v0_8-deep')


def close_root():
    time.sleep(0.1)
    root.destroy()


def get_filepath():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx .xls")])
    if filepath != '':
        file_label.configure(text=f'Выбранный файл: {filepath}')


def open_file():
    return pd.read_excel(file_label.cget('text').split('файл: ')[1])


def calculate():
    try:
        df = open_file()
        figure = Figure(figsize=(8, 5), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, solution_frame)
        toolbar = NavigationToolbar2Tk(figure_canvas, solution_frame, pack_toolbar=False)
        axes = figure.add_subplot()
        axes.plot(df.x, df.y)
        axes.set_title('Тестовый график')
        axes.set_ylabel('Тестовые значения')
        axes.set_facecolor('xkcd:light blue grey')
        figure.patch.set_facecolor('xkcd:light blue grey')
        figure_canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=(10, 0))
        toolbar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='w')
        table_label.configure(text=df.transpose().to_string())
    except IndexError:
        messagebox.showerror('Ошибка', 'Файл не выбран!')
    except ValueError:
        messagebox.showerror('Ошибка', 'Выбран файл неверного формата или введены некорректные данные!')


menu_frame = tk.CTkFrame(root, width=400, height=800, fg_color=('#E2DCDE', '#00303D'), corner_radius=14)
solution_frame = tk.CTkFrame(root, width=400, height=800, fg_color=('#E2DCDE', '#00303D'), corner_radius=14)

calculate_button = tk.CTkButton(menu_frame, text='Провести расчет', width=300, height=50, corner_radius=10,
                                border_width=2, font=('Merriweather Regular', 20), command=calculate,
                                fg_color=('#CEB1BE', '#004052'), hover_color=('#B97375', '#005066'),
                                border_color=('#2D2D34', '#00607A'), text_color=('#2D2D34', '#a9d6e5'))
load_data_button = tk.CTkButton(menu_frame, text='Загрузить данные', width=300, height=50, corner_radius=10,
                                border_width=2, font=('Merriweather Regular', 20), command=get_filepath,
                                fg_color=('#CEB1BE', '#004052'), hover_color=('#B97375', '#005066'),
                                border_color=('#2D2D34', '#00607A'), text_color=('#2D2D34', '#a9d6e5'))
exit_button = tk.CTkButton(menu_frame, text='Выход', width=300, height=50, corner_radius=10, border_width=2,
                           font=('Merriweather Regular', 20), command=close_root, fg_color=('#CEB1BE', '#004052'),
                           hover_color=('#B97375', '#005066'), border_color=('#2D2D34', '#00607A'),
                           text_color=('#2D2D34', '#a9d6e5'))
file_label = tk.CTkLabel(menu_frame, text='Файл не выбран', width=300, height=16, font=('Merriweather Regular', 14),
                         text_color=('#2D2D34', '#a9d6e5'))
graph_label = tk.CTkLabel(solution_frame, text='График', width=300, height=16, font=('Merriweather Regular', 14),
                          text_color=('#2D2D34', '#a9d6e5'))
table_label = tk.CTkLabel(solution_frame, text='Таблица', width=300, height=16, font=('Merriweather Regular', 14),
                          text_color=('#2D2D34', '#a9d6e5'))
table_scroll = tk.CTkScrollbar(table_label, hover=True)

root.columnconfigure(index=1, weight=1)
root.rowconfigure(index=0, weight=1)

calculate_button.grid(row=0, column=0, padx=10, pady=10)
load_data_button.grid(row=1, column=0, padx=10, pady=10)
file_label.grid(row=2, column=0, padx=10, pady=10)
exit_button.grid(row=3, column=0, padx=10, pady=10)
graph_label.grid(row=0, column=0, padx=10, pady=10)
table_label.grid(row=2, column=0, padx=10, pady=10)

menu_frame.grid(sticky='w', padx=40)
solution_frame.grid(row=0, column=1)

root.mainloop()
