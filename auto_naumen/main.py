from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from config import log, pas

URL = "http://sdn.pilot.ru:8080/fx"

# log, pas = input("Введите логин\n"), input("Введите пароль\n")
driver = webdriver.Chrome(ChromeDriverManager().install())


def start_naumen(url):
    """Функция старта наумена"""
    driver.get(url)
    time.sleep(0.5)
    driver.find_element_by_id('login').send_keys(log)
    driver.find_element_by_id('password').send_keys(pas)
    time.sleep(0.5)
    driver.find_element_by_name('LogonFormSubmit').click()
    time.sleep(1)


def find_search(query):
    """Функция поиска по заявке"""
    index_url = "http://sdn.pilot.ru:8080/fx/sd/ru.naumen.sd.published_jsp?uuid=corebofs000080000ikhm8pnur5l85oc"
    driver.get(index_url)
    driver.find_element_by_id('sdsearch_ServiceCallIdSearchType').clear()
    driver.find_element_by_id("sdsearch_ServiceCallIdSearchType").send_keys(query)
    time.sleep(0.5)
    driver.find_element_by_id("dosearchsdsearch_ServiceCallIdSearchType").click()


def parser_body():
    """Получение текста заявки"""
    time.sleep(1)
    descriprion = driver.find_element_by_class_name("servicecall_description_inner").text
    return descriprion


def send_mail(query, description):
    """Функция для отправки почты. Передается номер и тело заявки
    Получение ссылки на отправку комментария
    """

    link_mail = driver.find_element_by_id("ServiceCall.MailingList.SCMailing").get_attribute("href").split("?")[-1]
    link_comment = driver.find_element_by_id("ServiceCall.SDCommentList.AddSDComment").get_attribute("href").split("?")[
        -1]
    # print(f"mail {link_mail}\ncomment {link_comment}")
    driver.get("http://sdn.pilot.ru:8080/fx/$guic/ru.naumen.guic.components.forms.form_jsp?" + link_mail)
    driver.find_element_by_name('mailText').clear()
    text = f"""Здравствуйте!\nПросьба подтвердить выполенние работ ответным письмо по заявке № {query}\n\n{description}
\n\nС уважением,\nСлужба Поддержки Пользователей\nООО \"Пилот - бизнес решения для торговли\"\n107023, Москва, 
Барабанный переулок, дом 3\nтел. +7 495 564-8794\nфакс +7 495 564-8369\ne-mail: service_desk@pilot.ru"""
    driver.find_element_by_id("mailText").send_keys(text)
    time.sleep(2)
    # клик по отправке
    driver.find_element_by_name('send').click()
    time.sleep(1)

    driver.get("http://sdn.pilot.ru:8080/fx/$guic/ru.naumen.guic.components.forms.form_jsp?" + link_comment)
    driver.find_element_by_id("text").send_keys("Направлен запрос заказчику")
    driver.find_element_by_id("privateComment").click()
    # клик по отправке
    driver.find_element_by_name('add').click()


def main():
    bad = []
    count = 0
    with open("query.txt", "r") as file:
        for query in file:
            find_search(query)
            try:
                send_mail(query, parser_body())
            except:
                bad.append(query)
            time.sleep(1)
            count += 1
            print(count, "отправлено писем")
    driver.close()
    if len(bad) > 0:
        with open('bad_request.txt', 'w') as f:
            for request in bad:
                f.write(request, '\n')


if __name__ == '__main__':
    start_naumen(URL)
    main()
