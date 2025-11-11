# pages/login_page.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    # ----- Exact IDs from your UI -----
    TENANT_ID = (By.ID, "tenantId")
    TENANT_PROCEED = (By.ID, "tenant-btn")
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SIGNIN = (By.ID, "signIn-btn")

    # A stable element that exists only after successful login
    HOME_SENTINEL = (By.ID, "fabric-menu")

    def __init__(self, driver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    # ---------- Navigation ----------
    def open(self, base_url: str):
        self.driver.get(base_url)
        self.driver.maximize_window()
        time.sleep(1)

    # ---------- Tenant ----------
    def enter_tenant_id(self, tenant: str):
        t = self.wait.until(EC.presence_of_element_located(self.TENANT_ID))
        t.clear()
        t.send_keys(tenant)
        time.sleep(1)

    def click_proceed(self):
        self.wait.until(EC.element_to_be_clickable(self.TENANT_PROCEED)).click()
        time.sleep(1)

    # ---------- Credentials ----------
    def enter_username(self, username: str):
        u = self.wait.until(EC.presence_of_element_located(self.USERNAME))
        u.clear()
        u.send_keys(username)
        time.sleep(0.5)

    def enter_password(self, password: str):
        p = self.wait.until(EC.presence_of_element_located(self.PASSWORD))
        p.clear()
        p.send_keys(password)
        time.sleep(0.5)

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable(self.SIGNIN)).click()
        time.sleep(2)

    # ---------- Post-login wait ----------
    def wait_for_home(self):
        elem = self.wait.until(EC.presence_of_element_located(self.HOME_SENTINEL))
        time.sleep(1)
        return elem

    # ---------- Optional best-effort logout (safe, won’t fail if missing) ----------
    def try_logout(self):
        # If your app has different IDs, adjust here later.
        # This is best-effort and ignored if elements are absent.
        CAND_USER_MENU_IDS = ["avatar-menu", "user-menu", "profile-menu"]
        CAND_LOGOUT_IDS = ["logout-btn", "logout", "signout-btn"]

        try:
            for mid in CAND_USER_MENU_IDS:
                try:
                    self.driver.find_element(By.ID, mid).click()
                    time.sleep(1)
                    break
                except Exception:
                    pass

            for lid in CAND_LOGOUT_IDS:
                try:
                    self.driver.find_element(By.ID, lid).click()
                    time.sleep(1)
                    break
                except Exception:
                    pass
        except Exception:
            pass