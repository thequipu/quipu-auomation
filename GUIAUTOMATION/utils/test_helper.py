# utils/browser_permission_helper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_browser_with_permissions():
    options = Options()
    prefs = {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver