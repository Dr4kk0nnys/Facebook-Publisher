from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from pyautogui import typewrite, press

from random import randint
import base64
from time import sleep
from sys import argv


class Publisher():

    def __init__(self, email, password, product_info):
        
        self.publish(email, password, product_info)

    def publish(self, email, password, product_info):
        # few options to make it prettier
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        # chrome_options.add_argument('--log-level=OFF')

        # initialize the webdriver
        self.webdriver = webdriver.Chrome(options=chrome_options)

        # go to facebook.com
        self.webdriver.get('https://www.facebook.com')

        self.webdriver.find_element_by_id('email').send_keys(email)
        self.webdriver.find_element_by_id('pass').send_keys(password + Keys.ENTER)

        # wait for the page to load
        self.wait_for_selector('//div[@aria-label="Facebook"]', False)

        # TODO: This is not going to work with everybody
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

        # typing the product info ( title, price, ... ), the product info is an object
        self.type_product_info(product_info)

        # wait for everything to finish uploading
        sleep(3)

        # clicking next ( go to group selection page )
        next_group_selector = '//div[@aria-label="Avançar"]'
        self.wait_for_selector(next_group_selector, True)

        # wait for the group animation
        sleep(1.25)

        # clicking on every group
        groups = self.webdriver.find_elements_by_xpath('//img[@width="24"]')

        # 1 until 13 are the groups i want to post things about
        # if you want to remove a group ( in some cases your groups aren't for selling, you can black-mail the group-index value )
        # TODO: This is not going to worki with everybody
        for i in range(1, 14):
            groups[i].click()

        # publishing it
        # self.webdriver.find_element_by_xpath('//*[text()="Publicar"]').click()

        sleep(10)

        print('Done!')

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

        # elements = [title, price]
        elements_xpath = '//input[@type="text"]'
        elements = self.webdriver.find_elements_by_xpath(elements_xpath)

        elements[0].send_keys(product_info.get('title'))
        elements[1].send_keys(product_info.get('price'))

        description = self.webdriver.find_element_by_xpath('//textarea')
        description.send_keys(product_info.get('description'))

        self.send_images(product_info.get('images'))

    # perform all the clicks and operations, once the image_selector is open
    def send_images(self, images):

        text_selector = '//*[text()="Adicionar fotos"]'

        for i, image in enumerate(images):
            self.webdriver.find_element_by_xpath(text_selector).click()
            sleep(2)

            # first occurrence has to be setted up
            if (i == 0):
                press('left')
                for i in range(7):
                    press('down')
                press('enter')
                press('right')
                press('enter')
                sleep(1)

            typewrite(image)
            press('enter')
            sleep(2)

            text_selector = '//*[text()="Adicionar foto"]'


if __name__ == '__main__':
    Publisher(' '.join(argv[1:]))

