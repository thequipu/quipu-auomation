from selenium.webdriver.common.by import By

def test_login_page_elements(driver, config):
    driver.get(config["base_url"])
    assert driver.find_element(By.ID, "tenantId")
    driver.find_element(By.ID, "tenant-btn").click()
    assert driver.find_element(By.ID, "username")
    assert driver.find_element(By.ID, "password")
    assert driver.find_element(By.ID, "signIn-btn")