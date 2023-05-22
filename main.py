from tkinter import filedialog
from tkinter import messagebox
import customtkinter as tk
import time
import pandas as pd
import matplotlib.pyplot as plt

tk.set_appearance_mode("dark")

root = tk.CTk(fg_color=('#F1E4E8', '#002029'))
root.title('Расчет кинетической кривой')
root.iconbitmap('logo.ico')
root.geometry('700x700+200+50')
root.minsize(500, 500)


def close_root():
    time.sleep(0.1)
    root.destroy()


def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx .xls")])
    if filepath != '':
        file_label.configure(text=f'Выбранный файл: {filepath}')


def calculate():
    try:
        df = pd.read_excel(file_label.cget('text').split('файл: ')[1])
        print(df)
        plt.plot(df.x, df.y)
        plt.show()
    except IndexError:
        messagebox.showerror('Ошибка', 'Файл не выбран!')
    except ValueError:
        messagebox.showerror('Ошибка', 'Выбран файл неверного формата!')


container = tk.CTkFrame(root, width=400, height=800, fg_color=('#E2DCDE', '#00303D'), corner_radius=14)

calculate_button = tk.CTkButton(container, text='Провести расчет', width=300, height=50, corner_radius=10,
                                border_width=2, font=('Merriweather Regular', 20), command=calculate,
                                fg_color=('#CEB1BE', '#004052'), hover_color=('#B97375', '#005066'),
                                border_color=('#2D2D34', '#00607A'), text_color=('#2D2D34', '#a9d6e5'))
load_data_button = tk.CTkButton(container, text='Загрузить данные', width=300, height=50, corner_radius=10,
                                border_width=2, font=('Merriweather Regular', 20), command=open_file,
                                fg_color=('#CEB1BE', '#004052'), hover_color=('#B97375', '#005066'),
                                border_color=('#2D2D34', '#00607A'), text_color=('#2D2D34', '#a9d6e5'))
exit_button = tk.CTkButton(container, text='Выход', width=300, height=50, corner_radius=10, border_width=2,
                           font=('Merriweather Regular', 20), command=close_root, fg_color=('#CEB1BE', '#004052'),
                           hover_color=('#B97375', '#005066'), border_color=('#2D2D34', '#00607A'),
                           text_color=('#2D2D34', '#a9d6e5'))
file_label = tk.CTkLabel(container, text='Файл не выбран', width=300, height=16, font=('Merriweather Regular', 14),
                         text_color=('#2D2D34', '#a9d6e5'))

root.columnconfigure(index=0, weight=1)
root.rowconfigure(index=0, weight=1)

calculate_button.grid(row=0, column=0, padx=10, pady=10)
load_data_button.grid(row=1, column=0, padx=10, pady=10)
file_label.grid(row=2, column=0, padx=10, pady=10)
exit_button.grid(row=3, column=0, padx=10, pady=10)

container.grid(row=0, column=0)

root.mainloop()
