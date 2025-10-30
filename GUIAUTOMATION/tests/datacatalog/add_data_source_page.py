import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyautogui


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

# -------------------- navigate to DS --------------------
hamburger_icon = wait.until(EC.element_to_be_clickable((By.ID, "page-menu")))
hamburger_icon.click(); time.sleep(2)

datacatalogpage = wait.until(EC.element_to_be_clickable((By.ID, "Data Catalog-page")))
datacatalogpage.click(); time.sleep(2)

addnew_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-new-btn")))
addnew_btn.click(); time.sleep(2)

datasource_type_dropdown = wait.until(EC.element_to_be_clickable((By.ID,"ds-type-selector")))
datasource_type_dropdown.click()

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


element_select = wait.until(EC.presence_of_element_located((By.ID,"ORACLE-ds-type")))
element_select.click()
time.sleep(5)

name_input = wait.until(EC.presence_of_element_located((By.ID, "inputTitle")))
name_input.send_keys('kfc_y')
name_input.click()

description_input = wait.until(EC.presence_of_element_located((By.ID,"taDescription")))
description_input.send_keys('kpnani')
description_input.click()


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


#--------------------EXCEL------------------------------
"""
element_select = wait.until(EC.presence_of_element_located((By.ID,"EXCEL-ds-type")))
element_select.click()
time.sleep(5)

name_input = wait.until(EC.presence_of_element_located((By.ID, "inputTitle")))
name_input.send_keys('kfc_z')
name_input.click()

description_input = wait.until(EC.presence_of_element_located((By.ID,"taDescription")))
description_input.send_keys('kpnani')
description_input.click()

awsbucket_input = wait.until(EC.presence_of_element_located((By.ID,"awsBucket")))
awsbucket_input.send_keys("")
awsbucket_input.click();time.sleep(1)
awsfilekey_input = wait.until(EC.presence_of_element_located((By.ID,"awsKey")))
awsfilekey_input.send_keys("")
awsfilekey_input.click();time.sleep(1)
awsregion_input = wait.until(EC.presence_of_element_located((By.ID,"awsRegion")))
awsregion_input.send_keys("")
awsregion_input.click();time.sleep(1)
awsaccesskey_input = wait.until(EC.presence_of_element_located((By.ID,"awsAccessKey")))
awsaccesskey_input.send_keys("")
awsaccesskey_input.click();time.sleep(1)
awssecret_input = wait.until(EC.presence_of_element_located((By.ID,"awsAccessSecret")))
awssecret_input.send_keys("")
awssecret_input.click();time.sleep(1)
testconnection = wait.until(EC.element_to_be_clickable((By.ID, "ds-testConnection")))
testconnection.click()

dssave_btn = wait.until(EC.element_to_be_clickable((By.ID,"ds-save")))
dssave_btn.click()
"""
#----------------------PDF-------------------------
"""
element_select = wait.until(EC.presence_of_element_located((By.ID,"PDF-ds-type")))
element_select.click()
time.sleep(5)

name_input = wait.until(EC.presence_of_element_located((By.ID, "inputTitle")))
name_input.send_keys('kfc_z')
name_input.click()

description_input = wait.until(EC.presence_of_element_located((By.ID,"taDescription")))
description_input.send_keys('kpnani')
description_input.click()
file_url_input = wait.until(EC.presence_of_element_located((By.ID,"fileUrl")))
file_url_input.send_keys('')
file_url_input.click()

awsbucket_input = wait.until(EC.presence_of_element_located((By.ID,"awsBucket")))
awsbucket_input.send_keys("")
awsbucket_input.click();time.sleep(1)
awsfilekey_input = wait.until(EC.presence_of_element_located((By.ID,"awsKey")))
awsfilekey_input.send_keys("")
awsfilekey_input.click();time.sleep(1)
awsregion_input = wait.until(EC.presence_of_element_located((By.ID,"awsRegion")))
awsregion_input.send_keys("")
awsregion_input.click();time.sleep(1)
awsaccesskey_input = wait.until(EC.presence_of_element_located((By.ID,"awsAccessKey")))
awsaccesskey_input.send_keys("")
awsaccesskey_input.click();time.sleep(1)
awssecret_input = wait.until(EC.presence_of_element_located((By.ID,"awsAccessSecret")))
awssecret_input.send_keys("")
awssecret_input.click();time.sleep(1)

testconnection = wait.until(EC.element_to_be_clickable((By.ID, "ds-testConnection")))
testconnection.click()

dssave_btn = wait.until(EC.element_to_be_clickable((By.ID,"ds-save")))
dssave_btn.click()
"""
show_all = wait.until(EC.element_to_be_clickable((By.ID,"show-ds-btn")))
show_all.click()

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
time.sleep(2)

close_btn = wait.until(EC.element_to_be_clickable((By.ID,"ds-close-dialog")))
close_btn.click()
download_data = wait.until(EC.element_to_be_clickable((By.ID,"download-btn")))
download_data.click()
time.sleep(2)

# Press Command + Down to open Downloads or confirm path
pyautogui.hotkey('command', 'down')
time.sleep(1)
# Press Return (Enter) to confirm Save
pyautogui.press('return')
time.sleep(2)
print("✅ File download confirmed and saved to default location.")


clear_btn = wait.until(EC.element_to_be_clickable((By.ID,"navbar-cleear-btn")))
clear_btn.click()


#delete_btn = wait.until(EC.element_to_be_clickable((By.ID,"ds-delete")))
#delete_btn.click()
"""
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