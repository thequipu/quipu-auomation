from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# -------------------- setup + login --------------------
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
login_btn.click();time.sleep(5)

# -------------------- navigate to schema --------------------
hamburger_icon = wait.until(EC.element_to_be_clickable((By.ID, "page-menu")))
hamburger_icon.click(); time.sleep(2)
accessmanagement = wait.until(EC.element_to_be_clickable((By.ID, "Access Management-page")))
accessmanagement.click()
#==========flow for entity type schema================================
"""
addnew_btn = wait.until(EC.element_to_be_clickable((By.ID,"addNew-btn")))
addnew_btn.click();time.sleep(2)
#---step 1----------
entity_dropdown = wait.until(EC.presence_of_element_located((By.ID,"entityType")))
entity_dropdown.click();time.sleep(1)
element_select = wait.until(EC.presence_of_element_located((By.ID,"ent-SCHEMA")))
element_select.click();time.sleep(1)
schema_select = wait.until(EC.presence_of_element_located((By.ID,"schema-200MDATA")))
schema_select.click();time.sleep(1)
# --- Step 2: Fill in 'User Identifier' ---
user_field = wait.until(EC.presence_of_element_located((By.ID,"userId")))
user_field.send_keys("sample_user_001");time.sleep(1)
# --- Step 3: Fill in 'Permission' ---
permission_dropdowm = wait.until(EC.presence_of_element_located((By.ID,"permissions")))
permission_dropdowm.click();time.sleep(1)
select_permission =  wait.until(EC.presence_of_element_located((By.ID,"permission-VIEW")))
select_permission.click();time.sleep(1)
# --- Step 4: Click Save ---
save_button = wait.until(EC.element_to_be_clickable((By.ID,"save-btn")))
save_button.click()
#-Optional: Pause to observe
time.sleep(10)
"""
#==========flow for entity type ================================

addnew_btn = wait.until(EC.element_to_be_clickable((By.ID,"addNew-btn")))
addnew_btn.click();time.sleep(4)
#---step 1----------
entity_dropdown = wait.until(EC.presence_of_element_located((By.ID,"entityType")))
entity_dropdown.click();time.sleep(1)
element_select = wait.until(EC.presence_of_element_located((By.ID,"ent-DATA_SOURCE")))
element_select.click();time.sleep(1)
datasource_dropdown = wait.until(EC.presence_of_element_located((By.ID,"dataSource")))
datasource_dropdown.click();time.sleep(1)
element_select = wait.until(EC.presence_of_element_located((By.ID,"ds-MolecularFunction")))
element_select.click();time.sleep(1)
user_field = wait.until(EC.presence_of_element_located((By.ID,"userId")))
user_field.send_keys("nani3");time.sleep(1)
# --- Step 3: Fill in 'Permission' ---
permission_dropdowm = wait.until(EC.presence_of_element_located((By.ID,"permissions")))
permission_dropdowm.click();time.sleep(1)
select_permission =  wait.until(EC.presence_of_element_located((By.ID,"permission-VIEW")))
select_permission.click()
time.sleep(2)

save_btn = wait.until(EC.presence_of_element_located((By.ID,"save-btn")))
save_btn.click(),time.sleep(3)

user_menu = wait.until(EC.presence_of_element_located((By.ID,"user-menu")))
user_menu.click()
time.sleep(1)
log_out = wait.until(EC.presence_of_element_located((By.ID,"logout-btn")))
log_out.click()
time.sleep(3)


# Close the browser
driver.quit()

