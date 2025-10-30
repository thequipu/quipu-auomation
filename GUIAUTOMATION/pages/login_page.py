from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def enter_tenant(self, tenant):
        self.driver.find_element(By.ID, "tenantId").send_keys(tenant)

    def click_proceed(self):
        self.driver.find_element(By.ID, "tenant-btn").click()

    def enter_username(self, username):
        self.driver.find_element(By.ID, "username").send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(By.ID, "password").send_keys(password)

    def click_login(self):
        self.driver.find_element(By.ID, "signIn-btn").click()
