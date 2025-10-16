from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("http://localhost:4200/login")
driver.maximize_window()

wait = WebDriverWait(driver, 20)

tenant_input = wait.until(EC.presence_of_element_located(
    (By.ID, "tenantId']")))
tenant_input.send_keys("preprodquipuai")
time.sleep(1)

proceed_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "tenant-btn")))
proceed_btn.click()

username_input = wait.until(EC.presence_of_element_located(
    (By.ID, "username")))
username_input.send_keys("krishna")

password_input = wait.until(EC.presence_of_element_located(
    (By.ID, "password")))
password_input.send_keys("gunnam")

login_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "signIn-btn")))
login_btn.click()

hamburger_icon = wait.until(EC.element_to_be_clickable((By.ID, 'page-menu')))
hamburger_icon.click()
time.sleep(2)
# Wait for "Data Sources" option to become clickable
datafabric = wait.until(EC.element_to_be_clickable(
    (By.ID, "Data Fabric-page")))
datafabric.click()

backarrow_btn = wait.until(EC.element_to_be_clickable((By.ID, "realm-back-btn")))
backarrow_btn.click()

automobileautoseners_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "AutomobileAutosensors-realm")))
automobileautoseners_btn.click()

addnew_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "create-realm-btn")))
addnew_btn.click()

name_input = wait.until(EC.presence_of_element_located(
    (By.ID, "inputTitle")))
name_input.send_keys("nani")

discription_input = wait.until(EC.presence_of_element_located(
    (By.ID, "taDescription")))
discription_input.send_keys("krishna")

dropdown_selectsehema = wait.until(EC.presence_of_element_located(
    (By.ID, "selectSchema")))
dropdown_selectsehema.click()

dropdown_option = wait.until(EC.element_to_be_clickable(
    (By.ID, "carsdemo")))
dropdown_option.click()

dropdown_dataelect = wait.until(EC.presence_of_element_located(
    (By.ID, "")))
dropdown_dataelect.click()

dropdown_version = wait.until(EC.element_to_be_clickable((By.ID, "selectVersion")))
dropdown_option.click()

schemaview_btn = wait.until(EC.element_to_be_clickable((By.ID, "schema-view-btn")))
schemaview_btn.click()

save_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "save-btn")))
save_btn.click()

close_btn = wait.until(EC.element_to_be_clickable((By.ID, "realm-dialog-close-btn")))
close_btn.click()

# ------------------------------page clicks=============
"""
transformation_btn = wait.until(EC.element_to_be_clickable((By.ID, "transformation-tab")))
transformation_btn.click()

generate_btn = wait.until(EC.element_to_be_clickable((By.ID, "generate-btn")))
generate_btn.click()

popup = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'popup') or contains(@class,'modal')]")))

# Get the text of the popup
popup_text = popup.text
print(f"Popup text: {popup_text}")

# Look for buttons within the popup
confirm_button = popup.find_element(
    By.XPATH, "//button[contains(text(), 'Confirm')]")
confirm_button.click()
"""
save_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "save-btn")))
save_btn.click()

addnew_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-new-btn")))
addnew_btn.click()

name_input = wait.until(EC.presence_of_element_located((By.ID, "inputName")))
name_input.send_keys("nani")

decription_input = wait.until(EC.presence_of_element_located((By.ID, "description")))
discription_input.send_keys("nani")

dropdown_streamtype = wait.until(EC.presence_of_element_located((By.ID, "stream-type-selector")))
dropdown_streamtype.click()

dropdown_option = wait.until(EC.element_to_be_clickable(
    (By.ID, "stream-type-node")))
dropdown_option.click()

dropdown_selectdatasource = wait.until(EC.presence_of_element_located((By.ID, "datasource-selector")))
dropdown_selectdatasource.click()

dropdown_option = wait.until(EC.element_to_be_clickable((By.ID, "")))
dropdown_option.click()

dropdown_sourcetablelable = wait.until(EC.presence_of_element_located((By.ID, "table-name-selector")))
dropdown_sourcetablelable.click()

dropdown_option = wait.until(EC.element_to_be_clickable((By.ID, "")))
dropdown_option.click()

save_btn = wait.until(EC.element_to_be_clickable((By.ID, "save-stream-btn")))
save_btn.click()

close_btn = wait.until(EC.element_to_be_clickable((By.ID, "stream-dialog-close")))
close_btn.click()

startstreaming_btn = wait.until(EC.element_to_be_clickable((By.ID, "start-streaming-btn")))
startstreaming_btn.click()

# STREAMS(NODE)

search_text = wait.until(EC.presence_of_element_located((By.ID, "search-filter")))
search_text.send_keys("vehicle")

vehicle_btn = wait.until(EC.element_to_be_clickable((By.ID, "vehicle-stream")))
vehicle_btn.click()

decription_input = wait.until(EC.presence_of_element_located((By.ID, "description")))
discription_input.send_keys("Vehicle")

testplay_btn = wait.until(EC.element_to_be_clickable((By.ID, "test-query-btn")))
testplay_btn.click()

save_btn = wait.until(EC.element_to_be_clickable((By.ID, "save-stream-btn")))
save_btn.click()

close_btn = wait.until(EC.element_to_be_clickable((By.ID, "stream-dialog-close")))
close_btn.click()

dropdown_filter = wait.until(EC.element_to_be_clickable((By.ID, "filter")))
dropdown_filter.click()
dropdown_menu = wait.until(EC.element_to_be_clickable((By.ID, "filter-menu")))
dropdown_menu.click()
bydatasouce_btn = wait.until(EC.element_to_be_clickable((By.ID, "datasourceMenu")))
bydatasouce_btn.click()
second_dropdown_option = wait.until(EC.element_to_be_clickable((By.ID, "automobileautosensors")))
second_dropdown_option.click()

clear_filter_btn = wait.until(EC.element_to_be_clickable((By.ID, "clear-filter")))
clear_filter_btn.click()

# CONSTRAINTS

constraint_btn = wait.until(EC.element_to_be_clickable((By.ID, "constraints-tab")))
constraint_btn.click()

"""

element_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "sensor_value-stream")))
element_btn.click()

discription_input = wait.until(EC.presence_of_element_located(
    (By.ID, "description")))
discription_input.send_keys("T1")
save_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "save-stream-btn")))
save_btn.click()
"""

"""
delete_btn = wait.until(EC.element_to_be_clickable((By.ID, "rf-delete-realm")))
delete_btn.click()

 # Try to locate the popup by its content or structure
popup = wait.until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'popup') or contains(@class, 'modal')]")))

# Get the text of the popup
popup_text = popup.text
print(f"Popup text: {popup_text}")

# Look for buttons within the popup
confirm_button = popup.find_element(
    By.XPATH,"")
confirm_button.click()


((((

driver.find_element(By.ID, "filter-btn").click()

driver.find_element(By.ID, "single-select").click()


multi_ids = ["multi1", "multi2", "multi3"]
for mid in multi_ids:
    driver.find_element(By.ID, mid).click()


driver.find_element(By.ID, "refresh-btn").click()


# Click to trigger popup
driver.find_element(By.ID, "popup-btn").click()
time.sleep(1)

# Accept (Yes)
driver.switch_to.alert.accept()

# OR Dismiss (No)
# driver.switch_to.alert.dismiss()


from selenium.webdriver.support.ui import Select

dropdown = Select(driver.find_element(By.ID, "dropdown-id"))
dropdown.select_by_visible_text("Option 1")
# dropdown.select_by_index(0)
# dropdown.select_by_value("opt1")



driver.find_element(By.ID, "input-id").send_keys("Some Value")
driver.find_element(By.ID, "submit-btn").click()


driver.find_element(By.ID, "play-btn").click()

))))

back_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "realm-back-btn")))
back_btn.click()

add_realm_btn = wait.until(EC.element_to_be_clickable(
    (By.ID,"create-realm-btn")))
add_realm_btn.click()

back_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "realm-dialog-close-btn")))
back_btn.click()

name_input = wait.until(EC.presence_of_element_located(
    (By.ID, "inputTitle")))
name_input.send_keys("11111")

# Wait for "Save" button to become clickable
save_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "save-btn")))
save_btn.click()
time.sleep(2)

close_btn = wait.until(EC.element_to_be_clickable(
   (By.ID,"realm-dialog-close-btn")))
close_btn.click()
"""
time.sleep(2)

driver.quit()
