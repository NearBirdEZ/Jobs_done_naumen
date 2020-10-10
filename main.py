import api_naumen
import time
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException


class Send_message:
    api = api_naumen.API_Naumen()

    def __init__(self, gui_window):
        gui_window.title('LDB T_T')
        gui_window.geometry('320x600')

        self.lbl_l_naumen = tk.Label(gui_window, text='Login Naumen')
        self.lbl_p_naumen = tk.Label(gui_window, text='Password Naumen')

        self.login_area = tk.Entry(gui_window, width=30)
        self.password_area = tk.Entry(gui_window, width=30, show="*")

        self.btn_send = tk.Button(text='Отправить логин и\nпароль', command=self.send_log_pass)
        self.btn_clear = tk.Button(text='Очистить поле\nлогина и пароля', command=self.clear)

        self.btn_run = tk.Button(text='Запустить отправку писем', command=self.begin)
        self.btn_view = tk.Button(text='Показать процесс\n в браузере',
                                  command=self.view)

        self.txt = scrolledtext.ScrolledText(gui_window, width=30, height=24)
        self.lbl_count = tk.Label(gui_window, text='')

        self.lbl_l_naumen.place(relx=0.01, rely=0.01)
        self.lbl_p_naumen.place(relx=0.01, rely=0.05)

        self.login_area.place(relx=0.37, rely=0.01)
        self.password_area.place(relx=0.37, rely=0.05)

        self.btn_send.place(relx=0.05, rely=0.11)
        self.btn_clear.place(relx=0.6, rely=0.11)
        self.btn_run.place(relx=0.27, rely=0.9)
        self.btn_view.place(relx=0.3, rely=0.184)

        self.txt.place(relx=0.1, rely=0.25)
        self.lbl_count.place(relx=0.3, rely=0.95)

    def view(self):
        self.api.driver.set_window_position(0, 0)
        self.btn_view.configure(state='disabled')

    def send_log_pass(self):
        login = self.login_area.get()
        password = self.password_area.get()
        if login == '' or password == '':
            messagebox.showinfo('Ошибка', 'Не заполнены\nлогин и пароль')
            self.clear()
            return
        self.btn_send.configure(state='disabled')
        self.btn_clear.configure(state='disabled')
        self.api.start_naumen(login, password)

    def clear(self):
        self.login_area.delete('0', tk.END)
        self.password_area.delete('0', tk.END)

    def run(self):
        bad = []
        lst = self.txt.get('0.1', tk.END).split('\n')
        n = lst.count('')
        count = 0
        self.lbl_count.configure(text='Сейчас начнется выполнение')
        for _ in range(n):
            lst.remove('')

        if len(lst) == 0:
            messagebox.showinfo('Ошибка', 'Не найдена ни одна заявка')
            return
        total_request = len(lst)
        self.btn_run.configure(state='disabled')
        for request in lst:
            count += 1
            description = self.api.description_body(request)
            text = f"""\
Здравствуйте!
Просьба подтвердить выполнение работ ответным письмо по запросу № {request}

{description}

С уважением,\nСлужба Поддержки Пользователей
ООО \"Пилот - бизнес решения для торговли\"
107023, Москва, Барабанный переулок, дом 3
тел. +7 495 564-8794
факс +7 495 564-8369
e-mail: service_desk@pilot.ru
"""
            try:
                self.api.send_mail(text)
                self.api.send_comments(request, 'Направлен запрос для подтверждения выполненных работ', True)
                time.sleep(1)
            except NoSuchElementException:
                bad.append(request)
            self.lbl_count.configure(text=f'Выполнено {count} из {total_request}')
            window.title(f'{count} из {total_request}')
        if len(bad) > 0:
            with open('errors.txt', 'w') as bad:
                for query in bad:
                    bad.write(query, '\n')
        self.api.driver.close()
        messagebox.showinfo('Done', 'Все было отправлено\n'
                                    'Требуется проверить файл\n'
                                    'errors.txt, если есть')
        return

    def begin(self):
        threading.Thread(target=self.run, daemon=True).start()


if __name__ == '__main__':
    window = tk.Tk()
    app = Send_message(window)
    window.mainloop()
