import os, time
from pandas import describe_option
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

driver.get("https://app-preprod-1.thequipu.in/")
driver.maximize_window()

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

# -------------------- navigate to schema --------------------
hamburger_icon = wait.until(EC.element_to_be_clickable((By.ID, "page-menu")))
hamburger_icon.click(); time.sleep(2)

searchconfiguratioin = wait.until(EC.element_to_be_clickable((By.ID, "Search Configuration-page")))
searchconfiguratioin.click();time.sleep(5)

# click fabric menu
selectfabric_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "fabric-dropdown")))
selectfabric_dropdown.click()
time.sleep(1)

 # select fabric
fabric_btn = wait.until(EC.element_to_be_clickable((By.ID,"dbtrealworlddatamart")))
fabric_btn.click()
time.sleep(2)

data_select = wait.until(EC.element_to_be_clickable((By.ID,"person")))
data_select.click();time.sleep(1)
# select multiple elements by their IDs
ids_to_select = [
    "Person Node-cb",
    "Person's Email-cb",
    "Person's Telephone Number-cb",
    "Person's Physical Address-cb",
    "Person's Security Holdings-cb",
    "Person's Security Transactions-cb",
    "Person's country of citizenship and place of birth-cb"
]
for each_id in ids_to_select:
    element = wait.until(EC.element_to_be_clickable((By.ID, each_id)))
    element.click()
    time.sleep(1)

for each_id in ids_to_select:
    element = wait.until(EC.element_to_be_clickable((By.ID, each_id)))
    element.click()
    time.sleep(1)

save_btn = wait.until(EC.element_to_be_clickable((By.ID,"person-save")))
save_btn.click();time.sleep(1)

corporation_node =  wait.until(EC.element_to_be_clickable((By.ID,"corporation")))
corporation_node.click();time.sleep(1)

cop_node_query = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="innerAccordion1"]/div[1]/h2/div')))
cop_node_query.click();time.sleep(1)
# scroll down the full page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

save_btn = wait.until(EC.element_to_be_clickable((By.ID,"save-e360-path-btn")))
save_btn.click();time.sleep(1)
close_btn = wait.until(EC.element_to_be_clickable((By.ID,"close-e360-path-btn")))
close_btn.click();time.sleep(1)

driver.quit()



