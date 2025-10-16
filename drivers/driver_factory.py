import os, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

class DriverFactory:
    @staticmethod
    def load_config(path: str = "config/config.json") -> dict:
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
            "page_load": t.get("page_load", 60),
            "explicit":  t.get("explicit", 20),
            "implicit":  t.get("implicit", 0)
        }
        # env overrides
        cfg["browser"]    = os.getenv("BROWSER",  cfg["browser"]).lower()
        cfg["headless"]   = os.getenv("HEADLESS", str(cfg["headless"])).lower() == "true"
        cfg["remote"]     = os.getenv("REMOTE",   str(cfg["remote"])).lower() == "true"
        cfg["remote_url"] = os.getenv("REMOTE_URL", cfg["remote_url"]) or cfg["remote_url"]
        cfg["base_url"]   = os.getenv("BASE_URL", cfg.get("base_url", ""))
        cfg["tenant"]     = os.getenv("TENANT",   cfg.get("tenant", ""))
        cfg["username"]   = os.getenv("USERNAME", cfg.get("username", ""))
        cfg["password"]   = os.getenv("PASSWORD", cfg.get("password", ""))
        return cfg

    @staticmethod
    def get_driver(config_path: str = "config/config.json"):
        cfg = DriverFactory.load_config(config_path)
        browser, headless, remote, url, timeouts = cfg["browser"], cfg["headless"], cfg["remote"], cfg["remote_url"], cfg["timeouts"]

        if browser == "chrome":
            opts = ChromeOptions()
            if headless: opts.add_argument("--headless=new")
            opts.add_argument("--disable-gpu")
            opts.add_argument("--window-size=1920,1080")
            driver = webdriver.Remote(url, options=opts) if remote else webdriver.Chrome(options=opts)
        elif browser == "firefox":
            opts = FirefoxOptions()
            opts.headless = headless
            driver = webdriver.Remote(url, options=opts) if remote else webdriver.Firefox(options=opts)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.set_page_load_timeout(timeouts["page_load"])
        if timeouts["implicit"]:
            driver.implicitly_wait(timeouts["implicit"])
        wait = WebDriverWait(driver, timeouts["explicit"])
        return driver, wait