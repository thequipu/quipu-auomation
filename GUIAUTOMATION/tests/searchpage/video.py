import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------- Setup (auto-allow camera/mic) --------------------
ORIGIN = "https://app-preprod-1.thequipu.in"  # base origin for permission scoping

opts = webdriver.ChromeOptions()
# Suppress the getUserMedia permission prompt
opts.add_argument("--use-fake-ui-for-media-stream")
# Optional for CI: feed a fake device instead of real webcam/mic
# opts.add_argument("--use-fake-device-for-media-stream")
# opts.add_argument("--use-file-for-fake-video-capture=/path/to/sample.y4m")
# opts.add_argument("--use-file-for-fake-audio-capture=/path/to/sample.wav")

prefs = {
    # Global defaults: 1=allow, 2=block, 0=ask
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.notifications": 1,
    "profile.default_content_setting_values.geolocation": 1,
    # Scope to your site (keeps other origins at defaults)
    "profile.content_settings.exceptions.media_stream_camera": {f"{ORIGIN},*": {"setting": 1}},
    "profile.content_settings.exceptions.media_stream_mic":    {f"{ORIGIN},*": {"setting": 1}},
    "profile.content_settings.exceptions.notifications":       {f"{ORIGIN},*": {"setting": 1}},
    "profile.content_settings.exceptions.geolocation":         {f"{ORIGIN},*": {"setting": 1}},
}
opts.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=opts)
wait = WebDriverWait(driver, 20)

driver.get(f"{ORIGIN}/")
driver.maximize_window()

# -------------------- Login --------------------
tenant_input = wait.until(EC.presence_of_element_located((By.ID, "tenantId")))
tenant_input.send_keys("preprodquipuai1")
time.sleep(1)
wait.until(EC.element_to_be_clickable((By.ID, "tenant-btn"))).click()

wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("narenm")
wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("12!Quipu345")
wait.until(EC.element_to_be_clickable((By.ID, "signIn-btn"))).click()

# -------------------- Navigate to Fabric --------------------
wait.until(EC.presence_of_element_located((By.ID, "fabric-menu"))).click()
time.sleep(2)
wait.until(EC.presence_of_element_located((By.ID, "Hetionet-fabric"))).click()
time.sleep(2)

# -------------------- Video Icon Action --------------------
video_icon = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-search/main/div/div/div[2]/form/div/div[2]/button[2]/i"))
)
video_icon.click()
time.sleep(8)

# Optional: close the browser when done
# driver.quit()