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

# Wait for "Data fabric" option to become clickable
datafabric = wait.until(EC.element_to_be_clickable((By.ID, "Data Fabric-page")))
datafabric.click();time.sleep(5)

select_fabric = wait.until(EC.element_to_be_clickable((By.ID,"dbtrealworlddatamart-realm")))
select_fabric.click()
time.sleep(1)


#========create and delete==================
select_constraints = wait.until(EC.element_to_be_clickable((By.ID,"constraints-tab")));select_constraints.click()
time.sleep(2)
addnew_btn = wait.until(EC.element_to_be_clickable((By.ID,"add-new-constraint")));addnew_btn.click();time.sleep(1)
input_name = wait.until(EC.presence_of_element_located((By.ID,"constraintName")));input_name.send_keys("krish")
time.sleep(2)
node_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/ngb-offcanvas-panel/div[2]/div[2]/div/select")))
node_dropdown.click();time.sleep(1)

select_node = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/ngb-offcanvas-panel/div[2]/div[2]/div[1]/select/option[2]")))
select_node.click();time.sleep(0.5)

node_property = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/ngb-offcanvas-panel/div[2]/div[2]/div[2]/select/option[2]")))
node_property.click();time.sleep(1)

type_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/ngb-offcanvas-panel/div[2]/div[3]/div/select")))
type_dropdown.click();time.sleep(1)

select_type = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/ngb-offcanvas-panel/div[2]/div[3]/div/select/option[2]")))
select_type.click();time.sleep(1)

save_btn = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/ngb-offcanvas-panel/div[3]/button[1]")))
save_btn.click();time.sleep(1)

close_btn = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/ngb-offcanvas-panel/div[3]/button[2]")))
close_btn.click();time.sleep(1)
delete_constraints = wait.until(EC.presence_of_element_located((By.ID,"drop-constraint-krish")));delete_constraints.click()

time.sleep(5)
userlogout_btn = wait.until(EC.element_to_be_clickable((By.ID,"user-menu")))
userlogout_btn.click()
time.sleep(1)
logout_UI = wait.until(EC.element_to_be_clickable((By.ID,"logout-btn")))
logout_UI.click()

time.sleep(3)
driver.quit()


