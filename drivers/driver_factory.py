# drivers/driver_factory.py
import json
import os
from pathlib import Path
from typing import Dict, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class DriverFactory:
    @staticmethod
    def load_config() -> Dict:
        cfg_path = PROJECT_ROOT / "config" / "config.json"
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def get_driver(cfg: Dict):
        browser = (cfg.get("browser") or "chrome").strip().lower()
        if browser == "chrome":
            return DriverFactory._get_chrome_driver(cfg)
        if browser == "firefox":
            return DriverFactory._get_firefox_driver(cfg)
        raise ValueError(f"Unsupported browser: {browser}")

    # ------------------------ Chrome ------------------------
    @staticmethod
    def _get_chrome_driver(cfg: Dict):
        opts = ChromeOptions()

        # headless?
        if bool(cfg.get("headless", False)):
            opts.add_argument("--headless=new")
            # optional headless resolution
            res = str(cfg.get("headless_resolution", "1920,1080"))
            if "," in res:
                w, h = res.split(",", 1)
                opts.add_argument(f"--window-size={int(w)},{int(h)}")

        # common stability flags
        if cfg.get("disable_gpu", True):
            opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")

        # accept insecure certs
        if cfg.get("accept_insecure_certs", True):
            opts.set_capability("acceptInsecureCerts", True)

        # Optional: auto-allow camera/mic for tests that need WebRTC
        if cfg.get("allow_camera_mic", False):
            origin = (cfg.get("base_url") or "").rstrip("/")
            prefs = {
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.media_stream_mic": 1,
                "profile.default_content_setting_values.notifications": 1,
            }
            if origin:
                # scope it to your origin
                prefs["profile.content_settings.exceptions.media_stream_camera"] = {f"{origin},*": {"setting": 1}}
                prefs["profile.content_settings.exceptions.media_stream_mic"] = {f"{origin},*": {"setting": 1}}
                prefs["profile.content_settings.exceptions.notifications"] = {f"{origin},*": {"setting": 1}}
            opts.add_experimental_option("prefs", prefs)
            # suppress prompt
            opts.add_argument("--use-fake-ui-for-media-stream")

        # Try local chromedriver first; if not present, let Selenium Manager handle it
        local_driver = PROJECT_ROOT / "drivers" / "chromedriver"
        service: Optional[ChromeService] = None
        if local_driver.is_file():
            service = ChromeService(executable_path=str(local_driver))
        else:
            # service=None means Selenium Manager will auto-resolve and download
            service = ChromeService()  # no path -> auto

        try:
            driver = webdriver.Chrome(service=service, options=opts)
        except Exception as e:
            # Helpful message if a stale/invalid local binary is the cause
            if local_driver.is_file():
                raise RuntimeError(
                    f"Failed to start Chrome with local driver at '{local_driver}'. "
                    f"Make sure it matches your Chrome version and is executable (chmod +x). "
                    f"Original error: {e}"
                )
            raise

        # Maximize for headed runs
        if not cfg.get("headless", False):
            try:
                driver.maximize_window()
            except Exception:
                pass

        return driver

    # ------------------------ Firefox (optional) ------------------------
    @staticmethod
    def _get_firefox_driver(cfg: Dict):
        opts = FirefoxOptions()
        if bool(cfg.get("headless", False)):
            opts.add_argument("-headless")
        if cfg.get("accept_insecure_certs", True):
            opts.set_capability("acceptInsecureCerts", True)

        # Let Selenium Manager fetch geckodriver automatically
        service = FirefoxService()
        driver = webdriver.Firefox(service=service, options=opts)

        if not cfg.get("headless", False):
            try:
                driver.maximize_window()
            except Exception:
                pass
        return driver