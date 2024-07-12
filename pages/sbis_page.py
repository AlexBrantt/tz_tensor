from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils import logger


class SbisPage:
    URL = "https://sbis.ru/"
    CONTACTS_LINK = (By.LINK_TEXT, "Контакты")
    TENSOR_BANNER = (By.XPATH, "//a[@href='https://tensor.ru/']")
    BLOCK_CONTENT = (By.CLASS_NAME, "tensor_ru-Index__block4-content")
    ABOUT_LINK = (By.XPATH, "//a[@href='/about']")
    ABOUT_URL = "https://tensor.ru/about"
    PHOTO_SELECTOR = ".tensor_ru-About__block3-image"
    REGION_LABEL = (By.CLASS_NAME, "sbis_ru-Region-Chooser__text")
    PARTNERS_LIST = (By.CLASS_NAME, 'controls-ListView__itemContent')
    REGION_ITEM = (By.XPATH, "//span[text()='41 Камчатский край']")
    NEW_REGION = 'Камчатский край'

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def go_to_contacts(self):
        self.driver.find_element(*self.CONTACTS_LINK).click()

    def click_tensor_banner(self):
        self.driver.find_element(*self.TENSOR_BANNER).click()

    def switch_to_new_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[1])

    def wait_for_block_content(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.BLOCK_CONTENT)
            )
        except TimeoutException:
            logger.error("Блок 'Сила в людях' не был найден")

    def click_about_link(self):
        self.driver.find_element(*self.ABOUT_LINK).click()

    def wait_for_about_page(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_to_be(self.ABOUT_URL)
            )
        except TimeoutException:
            logger.error("Переадресация на '/about' не произошла")

    def find_photos(self):
        return self.driver.find_elements(By.CSS_SELECTOR, self.PHOTO_SELECTOR)

    def check_photos_dimensions(self):
        photos = self.find_photos()
        first_photo_size = (photos[0].get_attribute("width"),
                            photos[0].get_attribute("height"))

        for photo in photos[1:]:
            assert (photo.get_attribute("width"), photo.get_attribute("height")) == first_photo_size, (
                f"Фотография {photos.index(photo) + 1} имеет другие размеры")

    def get_region_label(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.REGION_LABEL)
            )
        except TimeoutException:
            logger.error("Элемент региона не найден")
        return self.driver.find_element(*self.REGION_LABEL)

    def get_partners_list(self):
        return self.driver.find_elements(*self.PARTNERS_LIST)

    def selet_region(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.REGION_ITEM)
            )
        except TimeoutException:
            logger.error("Регион не был выбран в течении 10 секунд")

        self.driver.find_element(*self.REGION_ITEM).click()

    def wait_for_region_change(self, expected_region):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element(self.REGION_LABEL,
                                                 expected_region)
            )
        except TimeoutException:
            logger.error("Регион не был изменен в течении 10 секунд")
