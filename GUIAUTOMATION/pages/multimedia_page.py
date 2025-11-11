import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MultiMediaSearchPage:
    MENU = (By.ID, "page-menu")
    MMS_PAGE = (By.ID, "Multi Media Search-page")

    REGISTER_USER_BTN = (By.XPATH, "/html/body/app-root/app-multi-media-search/main/div/div[1]/button")

    RECORD_BTN = (By.XPATH, "/html/body/app-root/app-multi-media-search/main/div/div[2]/div[1]/div[2]/div[2]/button[2]")
    STOP_RECORD_BTN = (By.XPATH, "/html/body/app-root/app-multi-media-search/main/div/div[2]/div/div[2]/div[2]/button[2]")

    PERSON_NAME_INPUT = (By.XPATH, "/html/body/app-root/app-multi-media-search/main/div/div[2]/div/form/div[1]/input")
    URI_INPUT = (By.XPATH, "/html/body/app-root/app-multi-media-search/main/div/div[2]/div/form/div[2]/input")

    START_WEBCAM_BTN = (By.XPATH, "/html/body/app-root/app-multi-media-search/main/div/div[2]/div/div[2]/div[2]/button[3]")

    USER_MENU = (By.ID, "user-menu")
    LOGOUT_BTN = (By.ID, "logout-btn")

    def __init__(self, driver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def open_via_menu(self):
        self.wait.until(EC.element_to_be_clickable(self.MENU)).click()
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable(self.MMS_PAGE)).click()
        time.sleep(2)

    def click_register_user(self):
        self.wait.until(EC.element_to_be_clickable(self.REGISTER_USER_BTN)).click()
        time.sleep(2)

    def record_and_stop(self):
        self.wait.until(EC.element_to_be_clickable(self.RECORD_BTN)).click()
        time.sleep(3)
        self.wait.until(EC.element_to_be_clickable(self.STOP_RECORD_BTN)).click()
        time.sleep(2)

    def fill_person_details(self, name_text, uri_text):
        self.wait.until(EC.presence_of_element_located(self.PERSON_NAME_INPUT)).send_keys(name_text)
        time.sleep(1)
        self.wait.until(EC.presence_of_element_located(self.URI_INPUT)).send_keys(uri_text)
        time.sleep(1)

    def start_webcam(self):
        self.wait.until(EC.element_to_be_clickable(self.START_WEBCAM_BTN)).click()
        time.sleep(4)

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.USER_MENU)).click()
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BTN)).click()