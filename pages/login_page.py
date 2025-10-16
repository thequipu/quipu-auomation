from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver, wait=None, timeout=20):
        self.driver = driver
        self.wait = wait or WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def enter_tenant(self, tenant):
        self.wait.until(EC.presence_of_element_located((By.ID, "tenantId"))).send_keys(tenant)

    def click_proceed(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "tenant-btn"))).click()

    def enter_username(self, username):
        self.wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)

    def enter_password(self, password):
        self.wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "signIn-btn"))).click()