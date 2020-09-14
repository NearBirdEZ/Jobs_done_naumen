import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox


def click():
    login = login_area.get()
    password = password_area.get()
    if login == '' or password == '':
        messagebox.showinfo('Ошибка', 'Не заполнены\nлогин и пароль')
        clear()
        return
    btn_send.configure(state='disabled')
    btn_clear.configure(state='disabled')
    print(login, password)
    return


def clear():
    login_area.delete('0', tk.END)
    password_area.delete('0', tk.END)


def run():
    lst = txt.get('0.1', tk.END).split('\n')
    n = lst.count('')
    for _ in range(n):
        lst.remove('')
    if len(lst) == 0:
        messagebox.showinfo('Ошибка', 'Не найдена ни одна заявка')
        return

    btn_run.configure(state='disabled')
    print(lst)
    return


window = tk.Tk()
window.title('LDB T_T')
window.geometry('320x600')

lbl_l_naumen = tk.Label(window, text='Login Naumen')
lbl_p_naumen = tk.Label(window, text='Password Naumen')

login_area = tk.Entry(window, width=30)
password_area = tk.Entry(window, width=30)

btn_send = tk.Button(text='Отправить логин и\nпароль', command=click)
btn_clear = tk.Button(text='Очистить поле\nлогина и пароля', command=clear)

btn_run = tk.Button(text='Запустить отправку писем', command=run)

txt = scrolledtext.ScrolledText(window, width=30, height=24)

lbl_l_naumen.place(relx=0.01, rely=0.01)
lbl_p_naumen.place(relx=0.01, rely=0.05)

login_area.place(relx=0.37, rely=0.01)
password_area.place(relx=0.37, rely=0.05)

btn_send.place(relx=0.05, rely=0.11)
btn_clear.place(relx=0.6, rely=0.11)
btn_run.place(relx=0.27, rely=0.9)

txt.place(relx=0.1, rely=0.25)

tk.mainloop()
