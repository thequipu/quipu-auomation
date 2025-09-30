import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------- setup + login --------------------
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

driver.get("https://app-preprod-1.thequipu.in/")
driver.maximize_window()

tenant_input = wait.until(EC.presence_of_element_located((By.ID, "tenantId")))
tenant_input.send_keys("preprodquipuai1"); time.sleep(1)
wait.until(EC.element_to_be_clickable((By.ID, "tenant-btn"))).click()

wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("narenm")
wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("12!Quipu345")
wait.until(EC.element_to_be_clickable((By.ID, "signIn-btn"))).click()

wait.until(EC.presence_of_element_located((By.ID, "fabric-menu"))).click(); time.sleep(2)
wait.until(EC.presence_of_element_located((By.ID, "Hetionet-fabric"))).click(); time.sleep(2)

# --------------- search page ----------------------
search_input = wait.until(EC.presence_of_element_located((By.ID, "search-query")))
search_text = "cancer symptoms"   # reuse this to find the node by label
search_input.send_keys(search_text)
search_input.send_keys(Keys.ENTER)
time.sleep(10)

#os.makedirs("artifacts/screens", exist_ok=True)
#out = "artifacts/screens/cancer_symptoms.png"
#driver.save_screenshot(out)

tableview_btn =  wait.until(EC.presence_of_element_located((By.ID, "tableView-btn")))
tableview_btn.click()
next_btn = wait.until(EC.visibility_of_element_located((By.ID,'')))

next_btn.click()





time.sleep(10)


