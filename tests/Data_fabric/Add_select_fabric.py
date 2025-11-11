import os, time
#from pandas import describe_option
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

fabric_delete =  wait.until(EC.presence_of_element_located((By.ID,"kp-delete-realm")));fabric_delete.click();time.sleep(1)
try:
    alert = driver.switch_to.alert
    print("Alert text:", alert.text)
    alert.accept()
    time.sleep(1)
    # Handle the second pop-up if it appears
    alert2 = driver.switch_to.alert
    print("Second alert text:", alert2.text)
    alert2.accept()
    time.sleep(1)
except:
    print("No alerts found after delete action.")


#========================= SQL QUERY EDIT  AND ADD DESCRIPTION===============

select_realm = wait.until(EC.element_to_be_clickable((By.ID,"kp1-edit-realm")));select_realm.click();time.sleep(1)
description_input = wait.until(EC.presence_of_element_located((By.ID,"taDescription")))
description_input.send_keys("automation");time.sleep(0.5)
save_btn = wait.until(EC.element_to_be_clickable((By.ID,"save-btn")));save_btn.click();time.sleep(1)


# ========================= MULTI-SELECT & DELETE (each with two popups) =========================
# Fill the exact selectable IDs you want to delete (edit these to your real IDs):
realm_ids_to_delete = [
    "kp3-delete-realm",
    "kp1-delete-realm",
    "kp2-delete-realm",
]

# The delete button used to remove selected realms (edit if your button ID differs):
delete_button_id = "kp-delete-realm"

for rid in realm_ids_to_delete:
    try:
        # Select each realm by its clickable/selectable control ID
        selectable = wait.until(EC.element_to_be_clickable((By.ID, rid)))
        selectable.click(); time.sleep(0.5)

        # Click the same Delete button for each selected ID
        del_btn = wait.until(EC.element_to_be_clickable((By.ID, delete_button_id)))
        del_btn.click(); time.sleep(0.6)

        # Popup #1 (e.g., "Hard Delete? Cancel for Soft Delete") — accept
        try:
            alert = driver.switch_to.alert
            print("Alert #1:", alert.text)
            alert.accept(); time.sleep(0.6)
        except Exception:
            print(f"No first alert for {rid}")

        # Popup #2 (e.g., confirmation like "Are you sure you want to soft delete this realm?") — accept
        try:
            alert2 = driver.switch_to.alert
            print("Alert #2:", alert2.text)
            alert2.accept(); time.sleep(0.8)
        except Exception:
            print(f"No second alert for {rid}")

    except TimeoutException:
        print(f"Could not delete id: {rid}")


time.sleep(2)
driver.quit()
