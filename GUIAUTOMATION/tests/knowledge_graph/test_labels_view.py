import os, json, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://localhost:4200/login")
driver.maximize_window()

wait = WebDriverWait(driver, 20)
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

hamburger_icon = wait.until(EC.element_to_be_clickable((By.ID, 'page-menu')))
hamburger_icon.click()
time.sleep(2)

knowledgegraps = wait.until(EC.element_to_be_clickable((By.ID, "Knowledge Graph-page")))
knowledgegraps.click()
time.sleep(2)

fabricpage_dropdown = wait.until(EC.presence_of_element_located((By.ID, "fabric-menu")))
fabricpage_dropdown.click()
time.sleep(2)

dropdown = wait.until(EC.presence_of_element_located((By.ID, "RealWorldDataMart-fabric")))
dropdown.click()
time.sleep(2)
"""
label_view_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "label-listedsecurity")))
label_view_btn.click()
time.sleep(2)

nodeconfigpanel_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "nodeConfigPanel-btn")))
nodeconfigpanel_btn.click()


node = wait.until(EC.element_to_be_clickable(
    (By.ID, "node-configuration")))
node.click()

select_option = wait.until(EC.element_to_be_clickable(
    (By.ID,"NaN")))
select_option.click()


back_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "Go back to Node Config Panel")))
back_btn.click()

zoomout = wait.until(EC.element_to_be_clickable(
    (By.ID,"graph-zoom-out-btn")))
zoomout.click()

zoom_in  =  wait.until(EC.element_to_be_clickable(
    (By.ID,"graph-zoom-in-btn")))
zoom_in.click()

zoom_in  =  wait.until(EC.element_to_be_clickable(
    (By.ID,"graph-zoom-in-btn")))
zoom_in.click()

adjust = wait.until(EC.element_to_be_clickable(
    (By.ID,"graph-fit-to-screen-btn")))
adjust.click()


cancel_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "clearGraphView-btn")))
cancel_btn.click()


wait = WebDriverWait(driver, 10)
upload_button = driver.find_element(By.ID, "upload-document") # Replace with actual ID
upload_button.click()
time.sleep(1)

# Click upload button (opens Finder dialog)
upload_btn = wait.until(EC.element_to_be_clickable(
(By.XPATH, "/html/body/ngb-offcanvas-panel/div[2]/app-documents-upload/div/div[1]/div/button")))
upload_btn.click()
# Give Finder a moment to appear
time.sleep(2)

# Shortcut to "Go to Folder"
pyautogui.hotkey('command', 'shift', 'g')
time.sleep(0.5)
pyautogui.hotkey('command', 'shift', 'g')  # send again just in case
time.sleep(1)
pyautogui.write('/Users/krishnapraveengunnam/Desktop')
pyautogui.press(['return', 'enter'])
time.sleep(2)
# Enter full filename with extension
pyautogui.write('[]')
pyautogui.press('enter')  # Select file
time.sleep(2)
close_btn = wait.until(EC.element_to_be_clickable( (By.CSS_SELECTOR,"body > ngb-offcanvas-panel > div.offcanvas-footer > button.btn.btn-outline-primary.me-2")))
close_btn.click()
time.sleep(1)
"""
search_input = wait.until(EC.presence_of_element_located((By.ID, "search")))
search_input.send_keys("address")
search_input.send_keys(Keys.ENTER)
time.sleep(2)
run_icon_btn =  wait.until(EC.element_to_be_clickable((By.ID, "runQuery-for-result-btn")))
run_icon_btn.click()

time.sleep(5)
driver.quit()






