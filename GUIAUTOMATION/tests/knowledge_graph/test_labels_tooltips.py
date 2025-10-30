import os, csv, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# ----- setup -----
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 30)
actions = ActionChains(driver)

# ----- login -----
driver.get("https://app-preprod-1.thequipu.in/login")
wait.until(EC.presence_of_element_located((By.ID, "tenantId"))).send_keys("preprodquipuai1")
wait.until(EC.element_to_be_clickable((By.ID, "tenant-btn"))).click()
wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("narenm")
wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("12!Quipu345")
wait.until(EC.element_to_be_clickable((By.ID, "signIn-btn"))).click()
time.sleep(5)

# ----- nav to KG -----
wait.until(EC.element_to_be_clickable((By.ID, "page-menu"))).click()
wait.until(EC.element_to_be_clickable((By.ID, "Knowledge Graph-page"))).click()
time.sleep(6)

# ----- helpers -----
def is_visible(el):
    try:
        if not el.is_displayed():
            return False
        rect = el.rect
        return rect.get("width", 0) > 0 and rect.get("height", 0) > 0
    except:
        return False

def relationship_chips():
    # scope to the Relationships section
    section = None
    for cand in driver.find_elements(By.XPATH, "//div[.//text()[contains(., 'Relationships')]]"):
        if cand.is_displayed():
            section = cand
            break
    if not section:
        return []

    # common chip selectors under the section
    candidates = []
    xps = [
        ".//button[normalize-space()!='']",
        ".//*[contains(@class,'chip')]",
        ".//*[contains(@class,'tag')]",
        ".//span[normalize-space()!='' and not(*)]",
        ".//a[normalize-space()!='']"
    ]
    for xp in xps:
        candidates.extend(section.find_elements(By.XPATH, xp))
    # visible only
    return [el for el in candidates if is_visible(el)]

def get_tooltip_text(target):
    # 1) aria-describedby path
    try:
        tid = target.get_attribute("aria-describedby")
        if tid:
            t = driver.execute_script("var n=document.getElementById(arguments[0]); return n? n.innerText.trim():'';", tid)
            if t:
                return t
    except:
        pass
    # 2) common overlay containers (Angular Material, CDK, generic)
    overlay_selectors = [
        ".cdk-overlay-container .mat-tooltip",
        ".cdk-overlay-container [role='tooltip']",
        ".cdk-overlay-container .mat-tooltip-panel",
        "[role='tooltip']",
        ".tooltip",
        ".ngx-tooltip",
        "[class*='tooltip']"
    ]
    end = time.time() + 2.5
    while time.time() < end:
        for sel in overlay_selectors:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            for el in els:
                try:
                    if is_visible(el):
                        txt = el.text.strip()
                        if txt:
                            return txt
                except:
                    continue
        time.sleep(0.1)
    # 3) fallbacks on the element itself
    for attr in ["title", "aria-label", "data-tooltip", "data-title"]:
        val = (target.get_attribute(attr) or "").strip()
        if val:
            return val
    return ""

# ----- collect -----
print("Collecting relationship tooltips")
chips = relationship_chips()
print(f"Found {len(chips)} visible relationship chips")

rows = []
os.makedirs("artifacts", exist_ok=True)

for idx, chip in enumerate(chips, 1):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", chip)
        time.sleep(0.3)
        actions.move_to_element(chip).perform()
        time.sleep(1.2)  # allow overlay to appear
        tip = get_tooltip_text(chip)
        name = chip.text.strip() or f"Relationship_{idx}"
        if not tip:
            tip = "no tooltip"
        rows.append({"Relationship": name, "Tooltip": tip})
        print(f"{idx}. {name} -> {tip}")
    except Exception as e:
        print(f"{idx}. hover/read failed: {e}")

# ----- save -----
csv_path = "artifacts/relationship_tooltips.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["Relationship", "Tooltip"])
    w.writeheader()
    w.writerows(rows)

md_path = "artifacts/relationship_tooltips.md"
with open(md_path, "w", encoding="utf-8") as md:
    md.write("| Relationship | Tooltip |\n")
    md.write("|--------------|---------|\n")
    for r in rows:
        md.write(f"| {r['Relationship'].replace('|',' ')} | {r['Tooltip'].replace('|',' ').replace('\n',' ')} |\n")

print(f"Exported {len(rows)} rows to {csv_path} and {md_path}")
driver.quit()
