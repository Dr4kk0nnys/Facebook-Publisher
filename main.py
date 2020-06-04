from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from pyautogui import typewrite, click, press
from pyautogui import locateCenterOnScreen

from random import randint
import base64
from time import sleep
from sys import argv


class Publisher():

    def __init__(self, product_name):
        # few options to make it prettier
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        # chrome_options.add_argument('--log-level=OFF')

        # initialize the webdriver
        self.webdriver = webdriver.Chrome(chrome_options=chrome_options)

        # go to facebook.com
        self.webdriver.get('https://www.facebook.com')

        # email and password credentials ( already decrypted )
        credentials = self.get_login_info()

        # typing the email and password and logging in
        email = self.webdriver.find_element_by_id('email')
        email.send_keys(credentials.get('email'))

        password = self.webdriver.find_element_by_id('pass')
        password.send_keys(credentials.get('password'))

        self.webdriver.find_element_by_id('pass').send_keys(Keys.ENTER)

        # wait for the page to load
        self.wait_for_selector('//div[@aria-label="Facebook"]', False)

        # choosing a random group
        groups = [
            'https://www.facebook.com/groups/424204217729696',
            'https://www.facebook.com/groups/mercadonegromontesclaros/',
            'https://www.facebook.com/groups/310280522400702/',
            'https://www.facebook.com/groups/432417496866854/'
        ]
        random_group = groups[randint(0, len(groups) - 1)]
        self.webdriver.get(random_group)

        # wait for the 'vender algo' selector, and click it
        self.wait_for_selector('//div[@aria-label="Vender algo"]', True)

        # wait for the 'Item a venda' selector
        self.wait_for_selector('//input[@aria-invalid="false"]', False)

        # product info got by the terminal argument
        product = self.get_product_info(product_name)

        # typing the product info ( title, price, ... ), the product info is an object
        self.type_product_info(product)

        # wait for everything to finish uploading
        sleep(3)

        # clicking next ( go to group selection page )
        self.webdriver.find_element_by_xpath(
            '//div[@aria-label="Avançar"]').click()

        # wait for the group animation
        sleep(2)

        # clicking on every group
        groups = self.webdriver.find_elements_by_xpath('//img[@width="24"]')

        # 1 until 13 are the groups i want to post things about
        # if you want to remove a group ( in some cases your groups aren't for selling, you can black-mail the group-index value )
        for i in range(1, 14):
            groups[i].click()

        # publishing it
        self.webdriver.find_element_by_xpath('//*[text()="Publicar"]').click()

        sleep(10)

        print('Done!')

    # also responsable for encryption and decryption
    def get_login_info(self):

        # email and password are encrypted saved into a hidden 'login_info.txt' file. also hidden through '.gitignore'
        file = open('.login_info.txt', 'r')
        lines = file.readlines()

        encrypted_email = lines[0]
        encrypted_password = lines[1]

        encrypted_email_bytes = encrypted_email.encode('ascii')
        encrypted_password_bytes = encrypted_password.encode('ascii')

        decrypted_email_bytes = base64.b64decode(encrypted_email_bytes)
        decrypted_password_bytes = base64.b64decode(encrypted_password_bytes)

        email = decrypted_email_bytes.decode('ascii')
        password = decrypted_password_bytes.decode('ascii')

        return {
            'email': email,
            'password': password
        }

    def wait_for_selector(self, selector='', should_click=False):

        while (True):
            try:
                if (should_click):
                    self.webdriver.find_element_by_xpath(selector).click()
                else:
                    self.webdriver.find_element_by_xpath(selector)

                break
            except:
                sleep(3)

    def type_product_info(self, product_info: {}):

        elements = self.webdriver.find_elements_by_xpath(
            '//input[@type="text"]')

        # title
        elements[0].send_keys(product_info.get('title'))
        # price
        elements[1].send_keys(product_info.get('price'))

        # description
        self.webdriver.find_element_by_xpath(
            '//textarea').send_keys(product_info.get('description'))

        # images
        self.send_images(product_info.get('images'))

    def send_images(self, images):

        text_selector = '//*[text()="Adicionar fotos"]'
        for image in images:
            self.webdriver.find_element_by_xpath(text_selector).click()
            sleep(2)
            typewrite(image)
            press('enter')
            sleep(2)

            # text selector changes from plural to singular after the first image ( ??? ), so i had to improvise ...
            text_selector = '//*[text()="Adicionar foto"]'

    def get_product_info(self, name='notebook'):

        product_info = ''

        if (name == 'notebook'):
            product_info = {
                'title': 'Notebook lenovo x230',
                'price': '1200',
                'description': '''# - Notebook''',
                'images': ['notebook_1.jpg', 'notebook_2.jpg']
            }

        elif (name == 'moletom'):
            product_info = {
                'title': 'Moletom algodao e poliester, muito confortavel',
                'price': '60',
                'description': '''# - Moletom''',
                'images': ['moletom_1.jpg', 'moletom_2.jpg']
            }

        else:
            raise 'Invalid product name!'

        return product_info


if __name__ == '__main__':
    Publisher(argv[1])
