import csv
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# ---------- Setup ----------
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 30)
actions = ActionChains(driver)

# ---------- Login ----------
driver.get("https://app-preprod-1.thequipu.in/login")

wait.until(EC.presence_of_element_located((By.ID, "tenantId"))).send_keys("preprodquipuai1")
wait.until(EC.element_to_be_clickable((By.ID, "tenant-btn"))).click()
wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("narenm")
wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("12!Quipu345")
wait.until(EC.element_to_be_clickable((By.ID, "signIn-btn"))).click()
time.sleep(5)

# ---------- Navigate to Knowledge Graph ----------
wait.until(EC.element_to_be_clickable((By.ID, "page-menu"))).click()
wait.until(EC.element_to_be_clickable((By.ID, "Knowledge Graph-page"))).click()
time.sleep(8)

# ---------- Hover over Relationship tooltips ----------
print("Collecting relationship tooltips...")

tooltip_data = []
os.makedirs("artifacts", exist_ok=True)
csv_path = "artifacts/relationship_tooltips.csv"

relationship_elements = driver.find_elements(By.CSS_SELECTOR, ".relationship, .ng-star-inserted")

for rel in relationship_elements:
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", rel)
        time.sleep(1)
        actions.move_to_element(rel).perform()
        time.sleep(2)
        tooltip = rel.get_attribute("title") or rel.text
        text_value = rel.text.strip() if rel.text.strip() else "Unnamed"
        tooltip_text = tooltip.strip() if tooltip else "No tooltip found"
        tooltip_data.append({"Relationship": text_value, "Tooltip": tooltip_text})
        print(f"{text_value} - {tooltip_text}")
    except Exception as e:
        print(f"Error while reading tooltip: {str(e)}")

with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Relationship", "Tooltip"])
    writer.writeheader()
    writer.writerows(tooltip_data)

print(f"Exported {len(tooltip_data)} relationship tooltips to {csv_path}")

with open(csv_path, "r", encoding="utf-8") as file:
    reader = list(csv.DictReader(file))
    print(f"Verified {len(reader)} rows read from file")
    assert len(reader) > 0, "No tooltips saved in the CSV file"

driver.quit()