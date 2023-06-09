from tkinter import filedialog, messagebox, ttk
import customtkinter as tk
import time
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

tk.set_appearance_mode("system")

root = tk.CTk(fg_color=('#F1E4E8', '#002029'))
root.title('Расчет кинетической кривой')
root.iconbitmap('media/logo.ico')
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.minsize(1400, 700)

matplotlib.use('TkAgg')
plt.style.use('seaborn-v0_8-deep')


def close_root() -> None:
    """Выход из программы"""
    time.sleep(0.1)
    root.destroy()


def get_calibfilepath() -> None:
    """Получить путь к калибровочному файлу и изменить текст"""
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx .xls")])
    if filepath != '':
        calib_file_label.configure(text=f'Выбранный файл для градуировки: {filepath}')


def get_userfilepath() -> None:
    """Получить путь к файлу и изменить текст"""
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx .xls")])
    if filepath != '':
        user_file_label.configure(text=f'Выбранный файл для расчета: {filepath}')


def calculate() -> pd.DataFrame:
    """Функция проводит расчет и должна вернуть данные, для построения графика"""
    calib_arr = np.transpose(
        pd.DataFrame.to_numpy(
            pd.read_excel(calib_file_label.cget('text').split('градуировки: ')[1])
        )
    )

    calib_line = np.polyfit(calib_arr[0], calib_arr[1], 1)

    user_arr = np.transpose(
        pd.DataFrame.to_numpy(
            pd.read_excel(user_file_label.cget('text').split('расчета: ')[1])
        )
    )

    user_conc = np.polyval(calib_line, user_arr[1])

    df = pd.DataFrame()
    df['time'] = user_arr[0].round(1)
    df['concentration'] = user_conc.round(3)
    return df


def make_plot() -> None:
    """Построение графика"""
    try:
        df = calculate()
        figure = Figure(figsize=(8, 5), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, solution_frame)
        toolbar = NavigationToolbar2Tk(figure_canvas, solution_frame, pack_toolbar=False)
        axes = figure.add_subplot()
        axes.plot(df.time, df.concentration)
        axes.set_title('Кинетическая кривая')
        axes.set_ylabel('Концентрация, мг/л')
        axes.set_xlabel('Время, мин')
        axes.set_facecolor('xkcd:light blue grey')
        figure.patch.set_facecolor('xkcd:light blue grey')
        figure_canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=(10, 0))
        toolbar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='w')
        table_frame.grid(row=0, column=2, padx=40)
        clear_tree()
        make_treeview(df)
        solution_frame.grid(row=0, column=1, padx=40)
    except IndexError:
        messagebox.showerror('Ошибка', 'Файл не выбран!')
    except ValueError:
        messagebox.showerror('Ошибка', 'Выбран файл неверного формата или введены некорректные данные!')
    except TypeError:
        messagebox.showerror('Ошибка', 'Возможна ошибка в исходных данных!')


def make_treeview(df) -> None:
    """Отображает таблицу с данными"""
    df_tree.heading("#1", text="Время")
    df_tree.heading("#2", text="Концентрация")
    df_tree.column('#1', width=100)
    df_tree.column('#2', width=100)
    df_rows = df.to_numpy().tolist()
    df_tree.grid(row=0, column=0, padx=10, pady=10)
    tree_scroll.grid(row=0, column=1, sticky='NS')
    for row in df_rows:
        df_tree.insert(parent='', index='end', values=row)


def clear_tree() -> None:
    """Очищает Treeview"""
    df_tree.delete(*df_tree.get_children())


menu_frame = tk.CTkFrame(
    root,
    width=400,
    height=800,
    fg_color=('#E2DCDE', '#00303D'),
    corner_radius=14
)
solution_frame = tk.CTkFrame(
    root,
    width=400,
    height=800,
    fg_color=('#E2DCDE', '#00303D'),
    corner_radius=14
)
table_frame = tk.CTkFrame(
    root,
    width=100,
    height=800,
    fg_color=('#E2DCDE', '#00303D'),
    corner_radius=14,
)
calculate_button = tk.CTkButton(
    menu_frame,
    text='Провести расчет',
    width=450,
    height=50,
    corner_radius=10,
    border_width=2,
    font=('Merriweather Regular', 20),
    command=make_plot,
    fg_color=('#CEB1BE', '#004052'),
    hover_color=('#B97375', '#005066'),
    border_color=('#2D2D34', '#00607A'),
    text_color=('#2D2D34', '#a9d6e5')
)
load_calibration_data_button = tk.CTkButton(
    menu_frame,
    text='Загрузить данные для градуировки',
    width=450,
    height=50,
    corner_radius=10,
    border_width=2,
    font=('Merriweather Regular', 20),
    command=get_calibfilepath,
    fg_color=('#CEB1BE', '#004052'),
    hover_color=('#B97375', '#005066'),
    border_color=('#2D2D34', '#00607A'),
    text_color=('#2D2D34', '#a9d6e5')
)
load_user_data_button = tk.CTkButton(
    menu_frame,
    text='Загрузить данные для расчета',
    width=450,
    height=50,
    corner_radius=10,
    border_width=2,
    font=('Merriweather Regular', 20),
    command=get_userfilepath,
    fg_color=('#CEB1BE', '#004052'),
    hover_color=('#B97375', '#005066'),
    border_color=('#2D2D34', '#00607A'),
    text_color=('#2D2D34', '#a9d6e5')
)
exit_button = tk.CTkButton(
    menu_frame, text='Выход',
    width=450,
    height=50,
    corner_radius=10,
    border_width=2,
    font=('Merriweather Regular', 20),
    command=close_root,
    fg_color=('#CEB1BE', '#004052'),
    hover_color=('#B97375', '#005066'),
    border_color=('#2D2D34', '#00607A'),
    text_color=('#2D2D34', '#a9d6e5')
)
calib_file_label = tk.CTkLabel(
    menu_frame,
    text='Файл для градуировки не выбран',
    width=300,
    height=16,
    font=('Merriweather Regular', 14),
    text_color=('#2D2D34', '#a9d6e5')
)
user_file_label = tk.CTkLabel(
    menu_frame,
    text='Файл c данными по кинетике не выбран',
    width=300,
    height=16,
    font=('Merriweather Regular', 14),
    text_color=('#2D2D34', '#a9d6e5')
)
df_tree = ttk.Treeview(
    table_frame,
    columns=['Время', 'Концентрация'],
    show='headings',
    height=15
)
tree_scroll = ttk.Scrollbar(
    table_frame,
    orient=tk.VERTICAL,
    command=df_tree.yview
)
df_tree.config(yscrollcommand=tree_scroll.set)

root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.rowconfigure(index=0, weight=1)
table_frame.rowconfigure(index=0, weight=1)
table_frame.columnconfigure(index=0, weight=1)

load_calibration_data_button.grid(row=0, column=0, padx=10, pady=10)
calib_file_label.grid(row=1, column=0, padx=10, pady=10)
load_user_data_button.grid(row=2, column=0, padx=10, pady=10)
user_file_label.grid(row=3, column=0, padx=10, pady=10)
calculate_button.grid(row=4, column=0, padx=10, pady=10)
exit_button.grid(row=5, column=0, padx=10, pady=10)

menu_frame.grid(sticky='w', padx=40)

root.mainloop()
