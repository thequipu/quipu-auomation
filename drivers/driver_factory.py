import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class DriverFactory:
    @staticmethod
    def get_driver():
        # read timeouts from config.json
        try:
            with open("config/config.json") as f:
                cfg = json.load(f)
            page_timeout = cfg.get("timeouts", {}).get("page", 30)
            element_timeout = cfg.get("timeouts", {}).get("element", 20)
        except Exception:
            page_timeout = 30
            element_timeout = 20

        options = Options()
        options.add_argument("--start-maximized")
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_script_timeout(page_timeout)
        driver.set_page_load_timeout(page_timeout)

        # return both driver and wait so pages can use directly
        wait = WebDriverWait(driver, element_timeout)
        return driver, wait