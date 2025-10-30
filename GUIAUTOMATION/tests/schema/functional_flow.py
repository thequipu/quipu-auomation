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
login_btn.click()

# -------------------- navigate to schema --------------------
hamburger_icon = wait.until(EC.element_to_be_clickable((By.ID, "page-menu")))
hamburger_icon.click(); time.sleep(2)

schemapage = wait.until(EC.element_to_be_clickable((By.ID, "Schema-page")))
schemapage.click(); time.sleep(2)

csv6tablesdios = wait.until(EC.element_to_be_clickable((By.ID, "csv6tablesdios-schema")))
csv6tablesdios.click();time.sleep(3)

#graphzoomin_icon = wait.until(EC.element_to_be_clickable((By.ID, "graph-zoom-out-btn")))
#graphzoomin_icon.click();time.sleep(1)
# locate the element
graphzoomout= driver.find_element(By.ID, "graph-zoom-out-btn")
# create action chain and double-click
actions = ActionChains(driver)
actions.double_click(graphzoomout).perform()

graphzoomin= driver.find_element(By.ID, "graph-zoom-in-btn")
# create action chain and double-click
actions = ActionChains(driver)
actions.double_click(graphzoomin).perform()
time.sleep(2)

graphfit_btn = wait.until(EC.element_to_be_clickable((By.ID, "graph-fit-to-screen-btn")))
graphfit_btn.click(); time.sleep(2)

nodeconfigpanel_icon = wait.until(EC.element_to_be_clickable((By.ID,"nodeConfigPanel-btn")))
nodeconfigpanel_icon.click();time.sleep(2)

nodeconfigpanel = wait.until(EC.element_to_be_clickable((By.ID,"node-configuration")))
nodeconfigpanel.click();time.sleep(2)
from utils.screenshots import take_screenshot
take_screenshot(driver, "schema_flow")

back_icon = wait.until(EC.element_to_be_clickable((By.ID,"Go back to Node Config Panel")))
back_icon.click();time.sleep(2)

edit_schema = wait.until(EC.element_to_be_clickable((By.ID,"edit-schema-btn")))
edit_schema.click();time.sleep(2)

similarity_view = wait.until(EC.element_to_be_clickable((By.ID,"similarityView-btn")))
similarity_view.click();time.sleep(2)
take_screenshot(driver, "similarity_view")

#hyperperameter_config = wait.until(EC.element_to_be_clickable((By.ID,"schema-hyperParemeter-btn")))
#hyperperameter_config.click();time.sleep(2)
#take_screenshot(driver, "hyper_view")

#close_btn = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="mat-mdc-dialog-20"]/div/div/app-schema-hyperparameter-dialog/mat-dialog-actions/button[3]')))
#close_btn.click();time.sleep(2)

editnodeconfigpanel = wait.until(EC.element_to_be_clickable((By.ID,"nodeConfigPanel-btn")))
editnodeconfigpanel.click();time.sleep(2)
"""
ESnodeconfigpanel = wait.until(EC.element_to_be_clickable((By.ID,"node-configuration")))
ESnodeconfigpanel.click();time.sleep(2)

node_input = wait.until(EC.presence_of_element_located((By.ID, "mat-input-17")))
node_input.send_keys("K1")

datasource_dropdown = wait.until(EC.presence_of_element_located((By.ID, "datasources")))
datasource_dropdown.click()
#select_element = wait.until(EC.presence_of_element_located((By.ID,"ds-csv_medical_procedures")))
#select_element.click()


# Add or remove option IDs here as needed
option_ids = [
    "ds-csv_medical_procedures",
    "ds-csv_employers",
    "ds-csv_members",
    "ds-csv_insurance_plans",
    "ds-csv_providers",
    "ds-csv_diagnoses"
]

for oid in option_ids:
    try:
        opt = wait.until(EC.element_to_be_clickable((By.ID, oid)))
        opt.click(); time.sleep(0.4)  # individual selection
    except TimeoutException:
        print(f"[WARN] Data source option not found or not clickable: {oid}")

# click the dropdown trigger again to close the panel
try:
    datasource_dropdown.click(); time.sleep(0.5)
except Exception:
    print("[INFO] Dropdown already closed or trigger not clickable")

"""
"""
graphlabel = wait.until(EC.element_to_be_clickable((By.ID,"graph-labels")))
graphlabel.click();time.sleep(1)
"""
back_icon = wait.until(EC.element_to_be_clickable((By.ID,"back-to-schema-workspace-page")))
back_icon.click()
back_to_schema = wait.until(EC.element_to_be_clickable((By.ID,"back-to-schema-page")))
back_to_schema.click()
#--------we can edit any schema depands on the case----------------
edit_schema = wait.until(EC.element_to_be_clickable((By.ID,"csv6tablesdios-schema-edit")))
edit_schema.click()

description_option = wait.until(EC.presence_of_element_located((By.ID,"taDescription")))
description_option.send_keys("schema")
description_option.click()

view_version = wait.until(EC.element_to_be_clickable((By.ID,"ngb-accordion-item-1-toggle")))
view_version.click()

save_schema = wait.until(EC.element_to_be_clickable((By.ID,"save-schema")))
save_schema.click()
edit_schema = wait.until(EC.element_to_be_clickable((By.ID,"csv6tablesdios-schema-edit")))
edit_schema.click()
close_schema = wait.until(EC.element_to_be_clickable((By.ID,"schema-dialog-back")))
close_schema.click()


#--------logout ----------
user_menu_dropdown = wait.until(EC.visibility_of_element_located((By.ID,"user-menu")))
user_menu_dropdown.click()
logout_UI = wait.until(EC.visibility_of_element_located((By.ID,"logout-btn")))
logout_UI.click()

time.sleep(7)