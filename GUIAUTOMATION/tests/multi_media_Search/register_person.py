import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from utils.screenshots import take_screenshot
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

driver.get("https://app-preprod-1.thequipu.in/login")
driver.maximize_window()

wait.until(EC.presence_of_element_located((By.ID, "tenantId"))).send_keys("preprodquipuai1")
wait.until(EC.element_to_be_clickable((By.ID, "tenant-btn"))).click()
wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("narenm")
wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("12!Quipu345")
wait.until(EC.element_to_be_clickable((By.ID, "signIn-btn"))).click()

# -------------------- navigate to MM --------------------
wait.until(EC.element_to_be_clickable((By.ID, "page-menu"))).click(); time.sleep(2)
wait.until(EC.element_to_be_clickable((By.ID, "Multi Media Search-page"))).click(); time.sleep(2)
"""
wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/app-multi-media-search/main/div/div[2]/div/div[2]/div[2]/button[1]"))).click();time.sleep(4)

# Type file path and press Enter
pyautogui.write("/Users/krishnapraveengunnam/Desktop/krishna/video.mp4")
pyautogui.press('return')
print("✅ File selected in Finder and uploaded.");time.sleep(3)
"""

register_user_btn = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/app-multi-media-search/main/div/div[1]/button")))
register_user_btn.click()
time.sleep(2)

record_btn = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/app-multi-media-search/main/div/div[2]/div[1]/div[2]/div[2]/button[2]")))
record_btn.click()
time.sleep(3)
stop_recording_btn = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/app-multi-media-search/main/div/div[2]/div/div[2]/div[2]/button[2]")));
stop_recording_btn.click()
time.sleep(2)

person_name_input = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/app-root/app-multi-media-search/main/div/div[2]/div/form/div[1]/input")))
person_name_input.send_keys("krishna")
time.sleep(2)
URI_input = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/app-root/app-multi-media-search/main/div/div[2]/div/form/div[2]/input")))
URI_input.send_keys("krishna")
time.sleep(2)

start_webcam_stream = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/app-multi-media-search/main/div/div[2]/div/div[2]/div[2]/button[3]")))
start_webcam_stream.click();time.sleep(4)
# stop_webcam_stream =  wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/app-multi-media-search/main/div/div[2]/div/div[2]/div[2]/button[3]")));time.sleep(4)

take_screenshot(driver, "video_uploaded")

time.sleep(3)
wait.until(EC.element_to_be_clickable((By.ID,"user-menu"))).click()
wait.until(EC.element_to_be_clickable((By.ID,"logout-btn"))).click()

driver.quit()
