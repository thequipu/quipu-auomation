from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# -------------------- setup + driver --------------------
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)
driver.get("https://app-preprod-1.thequipu.in/")
driver.maximize_window()
#==========login=====================
tenant_input = wait.until(EC.presence_of_element_located((By.ID,"tenantId")))
tenant_input.send_keys("preprodquipuai1");time.sleep(1)
proceed_btn = wait.until(EC.element_to_be_clickable((By.ID,"tenant-btn")))
proceed_btn.click()
username_input = wait.until(EC.presence_of_element_located((By.ID,"username")))
username_input.send_keys("narenm")
password_input = wait.until(EC.presence_of_element_located((By.ID,"password")))
password_input.send_keys("12!Quipu345")
login_btn = wait.until(EC.element_to_be_clickable((By.ID,"signIn-btn")))
login_btn.click();time.sleep(5)

user_menu = wait.until(EC.presence_of_element_located((By.ID,"user-menu")))
user_menu.click();time.sleep(1)
log_out = wait.until(EC.presence_of_element_located((By.ID,"logout-btn")))
user_menu.click()
time.sleep(3)
driver.quit()