import os, json, time

from PIL.ImageChops import screen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def take_screenshot(driver, name_prefix):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    directory = "artifacts/screenshots"
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f"{directory}/{name_prefix}_{timestamp}.png"
    driver.save_screenshot(filename)

driver = webdriver.Chrome()
driver.get("http://localhost:4200/login")
driver.maximize_window()

wait = WebDriverWait(driver, 20)
tenant_input = wait.until(EC.presence_of_element_located((By.ID, "tenantId")))
tenant_input.send_keys("preprodquipuai1")
time.sleep(1)

proceed_btn = wait.until(EC.element_to_be_clickable((By.ID, "tenant-btn")))
proceed_btn.click()

username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
username_input.send_keys("narenm")

password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
password_input.send_keys("12!Quipu345")

login_btn = wait.until(EC.element_to_be_clickable((By.ID, "signIn-btn")))
login_btn.click()

hamburger_icon = wait.until(EC.element_to_be_clickable((By.ID, 'page-menu')))
hamburger_icon.click()
time.sleep(2)

datafabric = wait.until(EC.element_to_be_clickable((By.ID, "Data Fabric-page")))
datafabric.click()
time.sleep(2)
#-------------add new fabric-----------------------------
add_new_button = wait.until(EC.element_to_be_clickable((By.ID,"create-realm-btn")))
add_new_button.click()
time.sleep(2)
name_input = wait.until(EC.element_to_be_clickable((By.ID,"inputTitle")))
name_input.send_keys('Nani')
name_input.click()
time.sleep(2)
select_schema_dropdown= wait.until(EC.element_to_be_clickable((By.ID,"selectSchema")))
select_schema_dropdown.click()
element_select = wait.until(EC.element_to_be_clickable((By.ID,"200MDATA")))
element_select.click()

select_schemaversion_dropdown = wait.until(EC.element_to_be_clickable((By.ID,"selectVersion")))
select_schemaversion_dropdown.click()
time.sleep(2)

select_schemaversion = wait.until(EC.element_to_be_clickable((By.ID,"v1")))
select_schemaversion.click()
time.sleep(2)

description_input = wait.until(EC.element_to_be_clickable((By.ID,"taDescription")))
description_input.send_keys('nanikp')
description_input.click()
#----------------------for schmea view----------------------
schemaview_btn = wait.until(EC.element_to_be_clickable((By.ID,"schema-view-btn")))
schemaview_btn.click()
time.sleep(5)
# take screenshot
take_screenshot(driver, "fabric_view")
time.sleep(3)




driver.quit()
