from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_page_elements(driver, config):
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 10)
    assert wait.until(EC.presence_of_element_located((By.ID, "tenantId")))
    assert wait.until(EC.presence_of_element_located((By.ID, "tenant-btn")))
    driver.find_element(By.ID, "tenantId").send_keys(config["tenant"])
    driver.find_element(By.ID, "tenant-btn").click()
    assert wait.until(EC.presence_of_element_located((By.ID, "username")))
    assert wait.until(EC.presence_of_element_located((By.ID, "password")))
    assert wait.until(EC.presence_of_element_located((By.ID, "signIn-btn")))