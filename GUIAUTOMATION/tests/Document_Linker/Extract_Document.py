from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

from tests.schema.create_version import element_select

# -------------------- setup + login --------------------
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
login_btn.click()
# -------------------- navigate to schema --------------------
hamburger_icon = wait.until(EC.element_to_be_clickable((By.ID,"page-menu")))
hamburger_icon.click(); time.sleep(2)
document_linker = wait.until(EC.element_to_be_clickable((By.ID,"Document Linker-page")))
document_linker.click();time.sleep(3)
Extract_document = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/app-document-visualizer/main/div/div/div[2]/button")))
Extract_document.click();time.sleep(1)
Slinker = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/app-document-visualizer/main/div/div[2]/div/form/div[1]/select")))
Slinker.click();time.sleep(1)
select_element = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/app-document-visualizer/main/div/div[2]/div/form/div[1]/select/option[13]")))
select_element.click();time.sleep(2)




