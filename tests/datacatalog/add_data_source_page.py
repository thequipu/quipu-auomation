import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v137.cache_storage import delete_entry
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



# -------------------- setup + login --------------------
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)
driver.get("http://localhost:4200/login")
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

# -------------------- navigate to DS --------------------
hamburger_icon = wait.until(EC.element_to_be_clickable((By.ID, "page-menu")))
hamburger_icon.click(); time.sleep(2)

datacatalogpage = wait.until(EC.element_to_be_clickable((By.ID, "Data Catalog-page")))
datacatalogpage.click(); time.sleep(2)

showall_btn = wait.until(EC.element_to_be_clickable((By.ID, "show-ds-btn")))
showall_btn.click(); time.sleep(2)

element_select = wait.until(EC.element_to_be_clickable((By.ID,"demo_policyadmin_s1")))
element_select.click();time.sleep(5)

edit_btn = wait.until(EC.element_to_be_clickable((By.ID,"edit-ds-btn")))
edit_btn.click();time.sleep(2)

description_input = wait.until(EC.element_to_be_clickable((By.ID,"taDescription")))
description_input.send_keys('nani')
description_input.click();time.sleep(2)

# --- update description and verify before/after on same ID ---
expected_desc = "nani"  # change this if you want a different test value
desc_el = wait.until(EC.element_to_be_clickable((By.ID, "taDescription")))


update_btn = wait.until(EC.element_to_be_clickable((By.ID,"ds-save")))
update_btn.click();time.sleep(8)

edit_btn = wait.until(EC.element_to_be_clickable((By.ID,"edit-ds-btn")))
edit_btn.click();time.sleep(2)








# take screenshot
driver.save_screenshot("artifacts/datasource_edit_screenshot.png")
driver.quit()







"""
addnew_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-new-btn")))
addnew_btn.click(); time.sleep(2)

datasource_type_dropdown = wait.until(EC.element_to_be_clickable((By.ID,"ds-type-selector")))
datasource_type_dropdown.click()

"""

#--------------------------POSTGRES----------------------------------------
"""
element_select = wait.until(EC.presence_of_element_located((By.ID,"POSTGRES-ds-type")))
element_select.click()
time.sleep(5)
#element_upload = wait.until(EC.element_to_be_clickable((By.ID,"ds-metadata-json")))
#element_upload.click()
#time.sleep(7)
# Absolute path of the file
"""
"""
file_path = os.path.abspath("/Users/krishnapraveengunnam/Desktop")

# Locate the file input element
upload_input = wait.until(EC.presence_of_element_located((By.ID, "ds-metadata-json")))

# Send the file path to the input
upload_input.send_keys(file_path)
"""
"""
name_input = wait.until(EC.presence_of_element_located((By.ID, "inputTitle")))
name_input.send_keys('kfc_y')
name_input.click()

discription_input = wait.until(EC.presence_of_element_located((By.ID,"taDescription")))
discription_input.send_keys('kpnani')
discription_input.click()


host_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbHostName")))
host_input.send_keys('167.86.123.100')
host_input.click()

dbport_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbPort")))
dbport_input.send_keys('5433')
dbport_input.click()

dbname_input = wait.until(EC.presence_of_element_located((By.ID,"inputDatabaseName")))
dbname_input.send_keys('kyc_s')
dbname_input.click()


dbschema_input = wait.until(EC.presence_of_element_located((By.ID,"dbSchemaName")))
dbschema_input.send_keys('public')
dbschema_input.click()


dbusername_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbUserName")))
dbusername_input.send_keys('postgres')
dbusername_input.click()

dbpassword_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbPassword")))
dbpassword_input.send_keys('2c510254-b82a-4562-9950-ad18e561cdee')
dbpassword_input.click()

"""


#__________________________________BIGQUERY___________________________________

"""

element_select = wait.until(EC.presence_of_element_located((By.ID,"BIGQUERY-ds-type")))
element_select.click()
time.sleep(5)

name_input = wait.until(EC.presence_of_element_located((By.ID, "inputTitle")))
name_input.send_keys('kfc_y')
name_input.click()

discription_input = wait.until(EC.presence_of_element_located((By.ID,"taDescription")))
discription_input.send_keys('kpnani')
discription_input.click()


projectid_input = wait.until(EC.presence_of_element_located((By.ID,"projectId")))
projectid_input.send_keys('')
projectid_input.click()

clientemail_input = wait.until(EC.presence_of_element_located((By.ID,"")))
clientemail_input.send_keys('')
clientemail_input.click()

clientid_input = wait.until(EC.presence_of_element_located((By.ID,"")))
clientid_input.send_keys('')
clientid_input.click()


privatekeyid_input = wait.until(EC.presence_of_element_located((By.ID,"")))
privatekeyid_input.send_keys('')
privatekeyid_input.click()


privatekey_input = wait.until(EC.presence_of_element_located((By.ID,"")))
privatekey_input.send_keys('')
privatekey_input.click()

datasetname_input = wait.until(EC.presence_of_element_located((By.ID,"")))
datasetname_input.send_keys('')
datasetname_input.click()
"""

#------------------------------snowflake--------------------------------


"""
element_select = wait.until(EC.presence_of_element_located((By.ID,"SNOWFLAKE-ds-type")))
element_select.click()
time.sleep(5)

name_input = wait.until(EC.presence_of_element_located((By.ID, "inputTitle")))
name_input.send_keys('kfc_y')
name_input.click()

discription_input = wait.until(EC.presence_of_element_located((By.ID,"taDescription")))
discription_input.send_keys('kpnani')
discription_input.click()


host_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbHostName")))
host_input.send_keys('OYYQWYP-MD26878.snowflakecomputing.com')
host_input.click()

dbhost_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbHostName")))
dbhost_input.send_keys('')
dbhost_input.click()

dbname_input = wait.until(EC.presence_of_element_located((By.ID,"inputDatabaseName")))
dbname_input.send_keys('INVESTMENT_MANAGEMENT')
dbname_input.click()


dbschema_input = wait.until(EC.presence_of_element_located((By.ID,"dbSchemaName")))
dbschema_input.send_keys('PUBLIC')
dbschema_input.click()


dbusername_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbUserName")))
dbusername_input.send_keys('QUIPU')
dbusername_input.click()

dbpassword_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbPassword")))
dbpassword_input.send_keys('quipu@S0')
dbpassword_input.click()
"""

#------------------------------------MYSQL---------------------------------------
"""

element_select = wait.until(EC.presence_of_element_located((By.ID,"MYSQL-ds-type")))
element_select.click()
time.sleep(5)

name_input = wait.until(EC.presence_of_element_located((By.ID, "inputTitle")))
name_input.send_keys('kfc_y')
name_input.click()

discription_input = wait.until(EC.presence_of_element_located((By.ID,"taDescription")))
discription_input.send_keys('kpnani')
discription_input.click()


host_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbHostName")))
host_input.send_keys('207.180.249.216')
host_input.click()

dbport_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbPort")))
dbport_input.send_keys('3306')
dbport_input.click()

dbname_input = wait.until(EC.presence_of_element_located((By.ID,"inputDatabaseName")))
dbname_input.send_keys('hetionet_D_SE')
dbname_input.click()


dbschema_input = wait.until(EC.presence_of_element_located((By.ID,"dbSchemaName")))
dbschema_input.send_keys('hetionet_D_SE')
dbschema_input.click()


dbusername_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbUserName")))
dbusername_input.send_keys('root')
dbusername_input.click()

dbpassword_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbPassword")))
dbpassword_input.send_keys('!ChangeMe!')
dbpassword_input.click()

"""

#----------------------------------Oracle----------------------------------
"""

element_select = wait.until(EC.presence_of_element_located((By.ID,"ORACLE-ds-type")))
element_select.click()
time.sleep(5)

name_input = wait.until(EC.presence_of_element_located((By.ID, "inputTitle")))
name_input.send_keys('kfc_y')
name_input.click()

discription_input = wait.until(EC.presence_of_element_located((By.ID,"taDescription")))
discription_input.send_keys('kpnani')
discription_input.click()


host_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbHostName")))
host_input.send_keys('207.180.249.216')
host_input.click()

dbport_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbPort")))
dbport_input.send_keys('1521')
dbport_input.click()

dbname_input = wait.until(EC.presence_of_element_located((By.ID,"inputDatabaseName")))
dbname_input.send_keys('FREE')
dbname_input.click()


dbschema_input = wait.until(EC.presence_of_element_located((By.ID,"dbSchemaName")))
dbschema_input.send_keys('HETIONET')
dbschema_input.click()


dbusername_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbUserName")))
dbusername_input.send_keys('hetionet')
dbusername_input.click()

dbpassword_input = wait.until(EC.presence_of_element_located((By.ID,"inputDbPassword")))
dbpassword_input.send_keys('hetionet')
dbpassword_input.click()

testconnection = wait.until(EC.element_to_be_clickable((By.ID, "ds-testConnection")))
testconnection.click()

dssave_btn = wait.until(EC.element_to_be_clickable((By.ID,"ds-save")))
dssave_btn.click()

time.sleep(15)

element_select = wait.until(EC.element_to_be_clickable((By.ID,"kfc_y")))
element_select.click()

signature_btn = wait.until(EC.element_to_be_clickable((By.ID,"signature-btn")))
signature_btn.click()

samplesize_input = wait.until(EC.presence_of_element_located((By.ID, "sampleSize")))
# Increment value by 1
samplesize_input.send_keys(Keys.ARROW_UP);time.sleep(2)
# Decrement value by 1
samplesize_input.send_keys(Keys.ARROW_DOWN);time.sleep(2)

iterations_input = wait.until(EC.presence_of_element_located((By.ID, "iterations")))
# Increment value by 1
iterations_input.send_keys(Keys.ARROW_UP);time.sleep(2)
# Decrement value by 1
iterations_input.send_keys(Keys.ARROW_DOWN);time.sleep(2)

readmultiplier_input = wait.until(EC.presence_of_element_located((By.ID, "iterations")))
# Increment value by 1
readmultiplier_input.send_keys(Keys.ARROW_UP);time.sleep(2)
# Decrement value by 1
readmultiplier_input.send_keys(Keys.ARROW_DOWN);time.sleep(2)

update_btn = wait.until(EC.presence_of_element_located((By.ID,"ds-signature-update")))
update_btn.click()


time.sleep(5)

edit_btn = wait.until(EC.element_to_be_clickable((By.ID,"edit-ds-btn")))
edit_btn.click()
time.sleep(3)

delete_btn = wait.until(EC.element_to_be_clickable((By.ID,"ds-delete")))
delete_btn.click()

#---------------------------------pop-up-click---------------------------

# First popup
alert1 = driver.switch_to.alert
print(alert1.text)
alert1.accept()

time.sleep(2)

# Second popup
alert2 = driver.switch_to.alert
print(alert2.text)
alert2.accept()


"""



time.sleep(10)

#driver.quit()