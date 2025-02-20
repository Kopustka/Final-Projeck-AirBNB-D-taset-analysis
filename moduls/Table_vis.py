import pandas as pd
import tkinter as tk
from tkinter import ttk

# Функция для отображения таблицы
def show_table(dataframe):
    root = tk.Tk()
    root.title("Просмотр данных")

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=list(dataframe.columns), show="headings")

    # Устанавливаем заголовки столбцов
    for col in dataframe.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Добавляем строки в таблицу
    for index, row in dataframe.iterrows():
        tree.insert("", tk.END, values=list(row))

    tree.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    root.mainloop()


