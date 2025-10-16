import os, time, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver import ActionChains

# ---------- Read config ----------
def read_config():
    with open("config/config.json", "r") as f:
        return json.load(f)

# ---------- Screenshot helper ----------
def screenshot(driver, name):
    path = os.path.join("artifacts", f"{name}.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.save_screenshot(path)

# ---------- Helpers ----------
def wait_for_overlays_to_disappear(driver, wait):
    # Add / remove selectors if your app uses different overlays
    overlays = [
        (By.CSS_SELECTOR, ".cdk-overlay-backdrop"),
        (By.CSS_SELECTOR, ".cdk-overlay-pane"),
        (By.CSS_SELECTOR, ".mat-mdc-menu-panel"),
        (By.CSS_SELECTOR, ".modal-backdrop.show"),
        (By.CSS_SELECTOR, ".modal.show"),
        (By.CSS_SELECTOR, ".ngx-spinner-overlay"),
        (By.CSS_SELECTOR, ".spinner, .loading, .loader"),
    ]
    for by, sel in overlays:
        try:
            wait.until(EC.invisibility_of_element_located((by, sel)))
        except TimeoutException:
            pass

def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", element)

def scroll_page_until_visible(driver, wait, locator, max_scrolls=8, step=600):
    """
    Gently scrolls down until the element is visible in viewport or max_scrolls reached.
    """
    for _ in range(max_scrolls):
        try:
            el = wait.until(EC.visibility_of_element_located(locator))
            scroll_into_view(driver, el)
            time.sleep(0.2)
            return el
        except TimeoutException:
            driver.execute_script(f"window.scrollBy(0, {step});")
            time.sleep(0.2)
    # last try: return visibility wait (may raise)
    return wait.until(EC.visibility_of_element_located(locator))

def click_safely(driver, wait, locator):
    el = scroll_page_until_visible(driver, wait, locator)
    wait_for_overlays_to_disappear(driver, wait)
    try:
        wait.until(EC.element_to_be_clickable(locator))
        el.click()
        return
    except ElementClickInterceptedException:
        pass
    # ActionChains fallback
    try:
        ActionChains(driver).move_to_element(el).pause(0.1).click().perform()
        return
    except ElementClickInterceptedException:
        pass
    # JS fallback
    driver.execute_script("arguments[0].click();", el)

# ---------- Test ----------
def test_sql_queries():
    cfg = read_config()

    # ---- Driver Setup (inline) ----
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    # SQL Queries (kept here, not in config)
    first_sql  = "SELECT Amount_paid FROM payments LIMIT 10;"
    second_sql = "SELECT payment_status, COUNT(*) FROM payments GROUP BY payment_status;"

    try:
        # ---------------- Login ----------------
        driver.get(cfg["base_url"])
        tenant_input = wait.until(EC.presence_of_element_located((By.ID, "tenantId")))  # <- keep / edit
        tenant_input.send_keys(cfg["tenant"])
        proceed_btn = wait.until(EC.element_to_be_clickable((By.ID, "tenant-btn")))     # <- keep / edit
        proceed_btn.click()

        username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))  # <- keep / edit
        username_input.send_keys(cfg["username"])
        password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))  # <- keep / edit
        password_input.send_keys(cfg["password"])
        login_btn = wait.until(EC.element_to_be_clickable((By.ID, "signIn-btn")))         # <- keep / edit
        login_btn.click()
        time.sleep(2)

        # ---------------- Navigate to Data Source ----------------
        click_safely(driver, wait, (By.ID, "page-menu"))                 # hamburger
        time.sleep(1)
        click_safely(driver, wait, (By.ID, "Data Catalog-page"))         # data sources menu item
        time.sleep(1)

        # Toggle show all and give the page a small settle time
        click_safely(driver, wait, (By.ID, "show-ds-btn"))               # Show All
        time.sleep(0.6)

        # Ensure scrolled to the list before clicking dev option
        click_safely(driver, wait, (By.ID, "dev_policyadmin2_connacted"))  # your DEV option ID
        time.sleep(1)

        # ---------------- Open payments table (with pre-scroll) ----------------
        click_safely(driver, wait, (By.ID, "payments"))
        time.sleep(1)
        screenshot(driver, "01_payments_selected")

        # ---------------- SQL Query 1 ----------------
        click_safely(driver, wait, (By.ID, "sql-qry-btn"))
        time.sleep(0.5)

        sql_editor = scroll_page_until_visible(driver, wait, (By.ID, "sql-query-input"))
        try:
            sql_editor.clear()
        except Exception:
            # fallback for editors that don't support .clear()
            driver.execute_script("arguments[0].value='';", sql_editor)
        sql_editor.send_keys(first_sql)

        click_safely(driver, wait, (By.ID, "execute-query-btn"))
        time.sleep(2)
        screenshot(driver, "02_first_query_results")

        # optional clear if you have a clear button
        try:
            click_safely(driver, wait, (By.ID, "clear-query-btn"))
        except Exception:
            pass

        # ---------------- SQL Query 2 ----------------
        sql_editor = scroll_page_until_visible(driver, wait, (By.ID, "sql-query-input"))
        try:
            sql_editor.clear()
        except Exception:
            driver.execute_script("arguments[0].value='';", sql_editor)
        sql_editor.send_keys(second_sql)

        click_safely(driver, wait, (By.ID, "execute-query-btn"))
        time.sleep(2)
        screenshot(driver, "03_second_query_results")

        # ---------------- Add Description ----------------
        click_safely(driver, wait, (By.ID, "info-payments"))   # if you truly need CSS like '#info-payment_status > i', change By.ID to By.CSS_SELECTOR
        time.sleep(0.4)
        click_safely(driver, wait, (By.ID, "description-inbox"))
        desc_input = wait.until(EC.presence_of_element_located((By.ID, "description-inbox")))
        desc_input.send_keys("Auto description note")

        click_safely(driver, wait, (By.ID, "save-description-bn"))
        time.sleep(1)
        screenshot(driver, "04_description_added")

    finally:
        driver.quit()