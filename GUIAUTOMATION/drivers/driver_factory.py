import os, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

class DriverFactory:
    @staticmethod
    def load_config(path="config/config.json"):
        try:
            with open(path, "r") as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}
        cfg.setdefault("browser", "chrome")
        cfg.setdefault("headless", False)
        cfg.setdefault("remote", False)
        cfg.setdefault("remote_url", "")
        t = cfg.setdefault("timeouts", {})
        cfg["timeouts"] = {
            "page_load": t.get("page_load", 90),
            "explicit": t.get("explicit", 30),
            "implicit": t.get("implicit", 0)
        }
        cfg["base_url"] = os.getenv("BASE_URL", cfg.get("base_url", ""))
        cfg["tenant"] = os.getenv("TENANT", cfg.get("tenant", ""))
        cfg["username"] = os.getenv("USERNAME", cfg.get("username", ""))
        cfg["password"] = os.getenv("PASSWORD", cfg.get("password", ""))
        return cfg

    @staticmethod
    def get_driver(config_path="config/config.json"):
        cfg = DriverFactory.load_config(config_path)
        browser = cfg["browser"]
        headless = cfg["headless"]
        is_remote = cfg["remote"]
        timeouts = cfg["timeouts"]

        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            driver = webdriver.Remote(cfg["remote_url"], options=options) if is_remote else webdriver.Chrome(options=options)
        elif browser == "firefox":
            options = FirefoxOptions()
            options.headless = headless
            driver = webdriver.Remote(cfg["remote_url"], options=options) if is_remote else webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.set_page_load_timeout(timeouts["page_load"])
        if timeouts["implicit"]:
            driver.implicitly_wait(timeouts["implicit"])
        wait = WebDriverWait(driver, timeouts["explicit"])
        return driver, wait