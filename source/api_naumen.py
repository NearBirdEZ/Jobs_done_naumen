from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time


class API_Naumen:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_position(0, -2000)

    def start_naumen(self, login, password):
        """Функция старта наумена"""
        self.driver.get('http://sdn.pilot.ru:8080/fx')
        time.sleep(0.5)
        self.enter_words('login', login)
        self.enter_words("password",
                         password,
                         '//*[@id="LogonForm"]/table/tbody/tr/td/table/tbody/tr[4]/td/input')

    def enter_words(self, id_xpath_area, words, id_xpath_button=None, t=0.5, private=False):
        """Функция для заполнения полей по ID или XPATH
           При необходимости нажатие на кнопку. По-умолчанию без нажатия
           атрибут private спецаильно для поля с комментарием, по-умолчанию данная опция выключена"""

        if id_xpath_area.startswith('//*[@'):
            self.driver.find_element_by_xpath(id_xpath_area).clear()
            self.driver.find_element_by_xpath(id_xpath_area).send_keys(words)
        else:
            self.driver.find_element_by_id(id_xpath_area).clear()
            self.driver.find_element_by_id(id_xpath_area).send_keys(words)
        time.sleep(t)
        if private:
            self.driver.find_element_by_id("privateComment").click()

        if id_xpath_button:
            if id_xpath_button.startswith('//*[@'):
                self.driver.find_element_by_xpath(id_xpath_button).click()
            else:
                self.driver.find_element_by_id(id_xpath_button).click()
        time.sleep(t)


    """
    
    
    Три самый часто используемые запроса поиска
    - По номеру запроса
    - По названию магазина
    - По серийному номеру
    
    
    """


    def search_by_request(self, request):
        self.enter_words('//*[@id="sdsearch_ServiceCallIdSearchType"]',
                         request,
                         '//*[@id="dosearchsdsearch_ServiceCallIdSearchType"]')


    def search_by_shop(self, shop):
        self.enter_words('//*[@id="searchString"]', shop, '//*[@id="doSearch"]')


    def search_by_serial_number(self, serial_number):
        self.enter_words('//*[@id="sdsearch_CMDBObjectInvNumberSearchTypeCMDBObjectAdvSearch"]',
                         serial_number,
                         '//*[@id="dosearchsdsearch_CMDBObjectInvNumberSearchTypeCMDBObjectAdvSearch"]')


    '''
    
    При необходимости можно удалить
    
    '''


    def back_to_request(func):
        # Выход на главную и переход по номеру запроса
        # Функция декоратор
        def wrapper(self, *args, **kwargs):
            request, *_ = args
            print(request)
            self.driver.get(
                'http://sdn.pilot.ru:8080/fx/sd/ru.naumen.sd.published_jsp?uuid=corebofs000080000ikhm8pnur5l85oc')
            self.search_by_request(request)

            link_request = self.driver.find_element_by_xpath('//*[@id="navpath"]/a[3]').get_attribute('href')

            func(self, *args, **kwargs)

            self.driver.get(link_request)
            return

        return wrapper


    def description_body(self, request):
        """Получение текста заявки"""
        self.search_by_request(request)
        time.sleep(1)
        description = self.driver.find_element_by_class_name("servicecall_description_inner").text
        return description


    def shop_request(self, request):
        """Получить магазин у заявки"""
        self.search_by_request(request)
        time.sleep(1)
        shop = self.driver.find_element_by_xpath('//*[@id="ServiceCall.Container.Column_2.CustomerProps.'
                                                 'client"]/a/span').text
        return shop


    def send_mail(self, text):
        """Функция для отправки почты.текст письма(с переносами)"""
        link_mail = self.driver.find_element_by_id("ServiceCall.MailingList.SCMailing").get_attribute("href")
        self.driver.get(link_mail)
        self.enter_words('//*[@id="mailText"]', text, '//*[@id="send"]')
        time.sleep(1)


    @back_to_request
    def send_comments(self, request, comment_text, conf=False):
        link_comment = self.driver.find_element_by_id("ServiceCall.SDCommentList.AddSDComment").get_attribute("href")

        self.driver.get(link_comment)
        self.enter_words('//*[@id="text"]', comment_text, '//*[@id="add"]', private=conf)
        time.sleep(1)


if __name__ == '__main__':
    pass
