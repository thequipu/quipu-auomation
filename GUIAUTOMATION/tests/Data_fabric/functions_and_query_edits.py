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

# Wait for "Data fabric" option to become clickable
datafabric = wait.until(EC.element_to_be_clickable((By.ID, "Data Fabric-page")))
datafabric.click();time.sleep(0.5)

#===============delete  fabric======== single_and_multi

fabric_delete =  wait.until(EC.presence_of_element_located((By.ID,"custom-check")));fabric_delete.click()
# select multiple specific elements by their unique IDs
ids_to_select = ["#mat-mdc-checkbox-506 > div > label"]

for each_id in ids_to_select:
    element = wait.until(EC.element_to_be_clickable((By.ID, each_id)))
    element.click()
    time.sleep(0.3)
"""
delete_streams = wait.until(EC.element_to_be_clickable((By.ID,"delete-stream-btn")));delete_streams.click();time.sleep(1)
force_ingest_toggle =  wait.until(ec.element_to_be_clickable((By.ID,"force-ingest-toggle-btn-button))),force_ingest_toggle.click();time.sleep(1)
clear_selections = wait.until(EC.element_to_be_clickable((By.ID,"cleare-selection")));clear_selections.click();time.sleep(1)
deselect_all = wait.until(EC.element_to_be_clickable((By.ID,"deselectAll-btn")));deselect_all.click();time.sleep(1)
resetstream_btn = wait.until(EC.element_to_be_clickable((By.ID,"reset-streamStats-btn")));resetstream_btn.click();time.sleep(1)

"""
deselect_all = wait.until(EC.element_to_be_clickable((By.ID,"deselectAll-btn")));deselect_all.click();time.sleep(1)

#========================= SQL QUERY EDIT  AND ADD DESCRIPTION===============

select_stream = wait.until(EC.element_to_be_clickable((By.ID,"inventorycurrent-stream")));select_stream.click();time.sleep(1)
description_input = wait.until(EC.presence_of_element_located((By.ID,"description")))
description_input.send_keys("automation")

# locate the input box cyper queris
input_cyper_queries = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ngb-offcanvas-panel/div[2]/form/div[4]/ngx-codemirror/div/div[6]/div[1]/div/div/div/div[5]/div/pre")))

# click inside to focus
input_cyper_queries.click()
time.sleep(0.5)
# select all and copy the current value
input_cyper_queries.send_keys(Keys.CONTROL, 'a')   # or Keys.COMMAND on macOS
input_cyper_queries.send_keys(Keys.CONTROL, 'c')
# clear the field
input_cyper_queries.send_keys(Keys.CONTROL, 'a')
input_cyper_queries.send_keys(Keys.BACK_SPACE)
time.sleep(0.5)
# paste the copied value back
input_cyper_queries.send_keys(Keys.CONTROL, 'v')

save_queris = wait.until(EC.visibility_of_element_located((By.ID,"save-stream-btn")))
save_queris.click();time.sleep(2)







