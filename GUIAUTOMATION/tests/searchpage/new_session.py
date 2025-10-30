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

#--------------------------------create new session or new agent-------------------------------

flex_switch = wait.until(EC.element_to_be_clickable((By.ID,"flexSwitchCheckDefault")))
flex_switch.click(); time.sleep(2)

dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > app-root > app-search > main > div > app-agentic-chat > div > div.overlay.ng-star-inserted > div > form > div:nth-child(1) > select")))
dropdown.click()

# Wait for and click the option inside the dropdown
option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > app-root > app-search > main > div > app-agentic-chat > div > div.overlay.ng-star-inserted > div > form > div:nth-child(1) > select > option")))
option.click()
time.sleep(1)

sessionID = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-search/main/div/app-agentic-chat/div/div[2]/div/form/div[2]/input")))
sessionID.send_keys('k1')
sessionID.click()

dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-search/main/div/app-agentic-chat/div/div[2]/div/form/div[3]/select")))
dropdown.click()

# Wait for and click the option inside the dropdown
option = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-search/main/div/app-agentic-chat/div/div[2]/div/form/div[3]/select/option[1]")))
option.click()
time.sleep(1)

dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-search/main/div/app-agentic-chat/div/div[2]/div/form/div[4]/select")))
dropdown.click()

# Wait for and click the option inside the dropdown
option = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-search/main/div/app-agentic-chat/div/div[2]/div/form/div[4]/select/option[1]")))
option.click()
time.sleep(1)

create_btn = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/app-search/main/div/app-agentic-chat/div/div[2]/div/form/div[5]/button[1]")))
create_btn.click()

time.sleep(4)






