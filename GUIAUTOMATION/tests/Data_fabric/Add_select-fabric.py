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

def close_overlay_by_edge_click(driver):
    body = driver.find_element(By.TAG_NAME, "body")
    a = ActionChains(driver)
    edges = [(10, 10), (-10, 10), (10, -10), (-10, -10)]  # TL, TR, BL, BR
    for dx, dy in edges:
        try:
            a.move_to_element_with_offset(
                body,
                dx if dx > 0 else body.rect["width"] + dx,
                dy if dy > 0 else body.rect["height"] + dy
            ).click().perform()
            time.sleep(0.5)
            return
        except Exception:
            continue
    # fallback: ESC if clicks fail
    a.send_keys(Keys.ESCAPE).perform()

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

# Wait for "Data fabric" option to become clickable
datafabric = wait.until(EC.element_to_be_clickable((By.ID, "Data Fabric-page")))
datafabric.click();time.sleep(0.5)

#backarrow_btn = wait.until(EC.element_to_be_clickable((By.ID, "realm-back-btn")))
#backarrow_btn.click()


#------------ADD NEW  and SCHEMA VIEW-----------------------------------------
addnew_btn = wait.until(EC.element_to_be_clickable((By.ID,"create-realm-btn")))
addnew_btn.click()

name_input = wait.until(EC.presence_of_element_located((By.ID, "inputTitle")))
name_input.send_keys("nani");time.sleep(0.5)

dropdown_selectsehema = wait.until(EC.presence_of_element_located((By.ID,"selectSchema")))
dropdown_selectsehema.click();time.sleep(0.5)
dropdown_option = wait.until(EC.element_to_be_clickable((By.ID,"200MDATA")))
dropdown_option.click();time.sleep(0.5)

dropdown_dataselect = wait.until(EC.presence_of_element_located((By.ID,"selectVersion")))
dropdown_dataselect.click();time.sleep(0.5)
dropdown_option = wait.until(EC.presence_of_element_located((By.ID,"v1")))
dropdown_option.click();time.sleep(0.5)

discription_input = wait.until(EC.presence_of_element_located((By.ID,"taDescription")))
discription_input.send_keys("krishna");time.sleep(0.5)
"""
schemaview_btn = wait.until(EC.element_to_be_clickable((By.ID, "schema-view-btn")))
schemaview_btn.click();time.sleep(0.5)

# Close overlay using helper
close_overlay_by_edge_click(driver)    #------schema view helper---------------
"""
save_btn = wait.until(EC.element_to_be_clickable((By.ID, "save-btn")))
save_btn.click();time.sleep(0.5)
close_btn = wait.until(EC.element_to_be_clickable((By.ID, "realm-dialog-close-btn")))
close_btn.click();time.sleep(0.5)

# ------------------------------   EXISTING FABRIC CLICK=============

dbtrealworlddatamart = wait.until(EC.element_to_be_clickable((By.ID, "dbtrealworlddatamart-realm")))
dbtrealworlddatamart.click()
""" ##-------------------GENERATE AND SAVE BUTTON---------------------------
generate_btn = wait.until(EC.element_to_be_clickable((By.ID, "generate-btn")))
generate_btn.click()
popup = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'popup') or contains(@class,'modal')]")))
# Get the text of the popup
popup_text = popup.text
print(f"Popup text: {popup_text}")
# Look for buttons within the popup
confirm_button = popup.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]")
confirm_button.click()
save_btn = wait.until(EC.element_to_be_clickable((By.ID, "save-btn")));save_btn.click()
"""
addnew_btn = wait.until(EC.element_to_be_clickable((By.ID,"add-new-btn")));addnew_btn.click()

name_input = wait.until(EC.presence_of_element_located((By.ID, "inputName")));name_input.send_keys("NANI")

decription_input = wait.until(EC.presence_of_element_located((By.ID, "description")));discription_input.send_keys("kp")

dropdown_streamtype = wait.until(EC.presence_of_element_located((By.ID, "stream-type-selector")));dropdown_streamtype.click()
dropdown_option = wait.until(EC.element_to_be_clickable((By.ID, "stream-type-node")));dropdown_option.click()

dropdown_selectdatasource = wait.until(EC.presence_of_element_located((By.ID, "datasource-selector")))
dropdown_selectdatasource.click()
dropdown_option = wait.until(EC.element_to_be_clickable((By.ID, "kyc_management-ds")))
dropdown_option.click()

dropdown_sourcetablelable = wait.until(EC.presence_of_element_located((By.ID, "table-name-selector")))
dropdown_sourcetablelable.click()
dropdown_option = wait.until(EC.element_to_be_clickable((By.ID,"source-table-industrysectorclassifier")))
dropdown_option.click()

testquery_btn = wait.until(EC.element_to_be_clickable((By.ID,"test-query-btn")))
testquery_btn.click()
# screenshot after test query
from datetime import datetime
os.makedirs(os.path.join("artifacts", "screenshots"), exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_path = os.path.join("artifacts", "screenshots", f"test_query_{ts}.png")
driver.save_screenshot(screenshot_path)
print(f"Screenshot saved to {screenshot_path}")


save_btn = wait.until(EC.element_to_be_clickable((By.ID, "save-stream-btn")))
save_btn.click();time.sleep(3)

#close_btn = wait.until(EC.element_to_be_clickable((By.ID, "stream-dialog-close")))
#close_btn.click()
"""
startstreaming_btn = wait.until(EC.element_to_be_clickable((By.ID, "start-streaming-btn")))
startstreaming_btn.click()
stopstreaming_btn = wait.until(EC.element_to_be_clickable((By.ID, "")))
stopstreaming_btn.click()
"""

# =================CONSTRAINTS=============================

constraint_btn = wait.until(EC.element_to_be_clickable((By.ID, "constraints-tab")))
constraint_btn.click();time.sleep(2)

addnew_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-new-constraint")))
addnew_btn.click();time.sleep(0.5)

name_input = wait.until(EC.element_to_be_clickable((By.ID, "constraintName")))
name_input.click();time.sleep(0.5)
node_dropdown = wait.until(EC.element_to_be_clickable((By.ID,""))) #-----missing iD========
node_dropdown.click();time.sleep(0.5)
select_element = wait.until(EC.visibility_of_element_located((By.ID,"")));select_element.click();time.sleep(0.5)
type_dropdown = wait.until(EC.element_to_be_clickable((By.ID,""))) #-----missing iD========
type_dropdown.click();time.sleep(0.5)
select_element = wait.until(EC.visibility_of_element_located((By.ID,"")));select_element.click();time.sleep(0.5)
addtypes_input = wait.until(EC.element_to_be_clickable((By.ID,"")));addtypes_input.send_keys("");time.sleep(0.5)
save_btn = wait.until(EC.element_to_be_clickable((By.ID, "")))
save_btn.click()
#close_btn = wait.until(EC.element_to_be_clickable((By.ID, "")));save_btn.click()


time.sleep(3)
driver.quit()
