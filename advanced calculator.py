import tkinter as tk

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Ошибка")

def clear():
    entry.delete(0, tk.END)

def backspace():
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current[:-1])

# Создание основного окна
root = tk.Tk()
root.title("Калькулятор")
root.resizable(False, False)

# Поле ввода
entry = tk.Entry(root, width=20, font=('Arial', 16), borderwidth=5, justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Кнопки
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
    ('←', 5, 0), ('=', 5, 1)
]

for (text, row, col) in buttons:
    if text == '=':
        btn = tk.Button(root, text=text, width=8, height=2, command=calculate)
    elif text == 'C':
        btn = tk.Button(root, text=text, width=8, height=2, command=clear)
    elif text == '←':
        btn = tk.Button(root, text=text, width=8, height=2, command=backspace)
    else:
        btn = tk.Button(root, text=text, width=8, height=2, 
                       command=lambda t=text: entry.insert(tk.END, t))
    btn.grid(row=row, column=col, padx=2, pady=2)

root.mainloop()