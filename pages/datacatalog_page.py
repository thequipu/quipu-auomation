# pages/datacatalog_page.py
import time
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver import ActionChains

try:
    import pyautogui  # optional, used only if available (for download confirm on macOS)
except Exception:
    pyautogui = None


class DataCatalogPage:
    """
    POM for Data Catalog page.
    Keeps your exact IDs and sleeps. Only adds safe fallbacks (ActionChains/JS click).
    """

    # ----- Common / Navigation -----
    HAMBURGER = (By.ID, "page-menu")
    DATACATALOG_MENU = (By.ID, "Data Catalog-page")
    SHOW_ALL = (By.ID, "show-ds-btn")
    CLEAR_NAVBAR = (By.ID, "navbar-cleear-btn")

    # ----- Add New Data Source -----
    ADD_NEW = (By.ID, "add-new-btn")
    DS_TYPE_DROPDOWN = (By.ID, "ds-type-selector")
    ORACLE_TYPE = (By.ID, "ORACLE-ds-type")

    INPUT_TITLE = (By.ID, "inputTitle")
    TA_DESCRIPTION = (By.ID, "taDescription")
    INPUT_DB_HOST = (By.ID, "inputDbHostName")
    INPUT_DB_PORT = (By.ID, "inputDbPort")
    INPUT_DB_NAME = (By.ID, "inputDatabaseName")
    INPUT_DB_SCHEMA = (By.ID, "dbSchemaName")
    INPUT_DB_USER = (By.ID, "inputDbUserName")
    INPUT_DB_PASS = (By.ID, "inputDbPassword")

    TEST_CONN = (By.ID, "ds-testConnection")
    DS_SAVE = (By.ID, "ds-save")

    # ----- Signature / Edit / Download -----
    SIGNATURE_BTN = (By.ID, "signature-btn")
    SAMPLE_SIZE = (By.ID, "sampleSize")
    ITERATIONS = (By.ID, "iterations")
    SIGNATURE_UPDATE = (By.ID, "ds-signature-update")
    EDIT_DS_BTN = (By.ID, "edit-ds-btn")
    CLOSE_DIALOG = (By.ID, "ds-close-dialog")
    DOWNLOAD_BTN = (By.ID, "download-btn")

    # ----- SQL queries IDs -----
    SQL_BTN = (By.ID, "sql-qry-btn")
    SQL_INPUT = (By.ID, "sql-query-input")
    SQL_EXECUTE = (By.ID, "execute-query-btn")
    SQL_CLEAR = (By.ID, "clear-query-btn")  # optional; guarded in code

    # ----- Description for table -----
    # Example table info icon id: "info-payments"
    DESC_INPUT = (By.ID, "description-inbox")
    DESC_SAVE = (By.ID, "save-description-bn")

    def __init__(self, driver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    # ------------------ Helpers (no ID changes) ------------------
    def _scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", element)

    def _click_safely(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        try:
            self._scroll_into_view(el)
        except Exception:
            pass
        try:
            self.wait.until(EC.element_to_be_clickable(locator))
            el.click()
            return
        except ElementClickInterceptedException:
            pass
        try:
            ActionChains(self.driver).move_to_element(el).pause(0.1).click().perform()
            return
        except ElementClickInterceptedException:
            pass
        self.driver.execute_script("arguments[0].click();", el)

    def _type(self, locator, text: str):
        el = self.wait.until(EC.presence_of_element_located(locator))
        try:
            el.clear()
        except Exception:
            self.driver.execute_script("arguments[0].value='';", el)
        el.send_keys(text)

    def _accept_alert_if_present(self, sleep_after: float = 0.6) -> bool:
        try:
            alert = self.driver.switch_to.alert
            _ = alert.text
            alert.accept()
            time.sleep(sleep_after)
            return True
        except Exception:
            return False

    # ------------------ Navigation ------------------
    def goto_datacatalog(self):
        self._click_safely(self.HAMBURGER)
        time.sleep(1)
        self._click_safely(self.DATACATALOG_MENU)
        time.sleep(2)

    # ------------------ Add Data Source (Oracle) ------------------
    def click_add_new(self):
        self._click_safely(self.ADD_NEW)
        time.sleep(2)

    def choose_oracle_type(self):
        self._click_safely(self.DS_TYPE_DROPDOWN)
        time.sleep(0.4)
        self._click_safely(self.ORACLE_TYPE)
        time.sleep(1)

    def fill_oracle_form(self, name: str, description: str, host: str, port: str,
                         dbname: str, schema: str, username: str, password: str):
        self._type(self.INPUT_TITLE, name)
        time.sleep(0.2)
        self._type(self.TA_DESCRIPTION, description)
        time.sleep(0.2)
        self._type(self.INPUT_DB_HOST, host)
        time.sleep(0.2)
        self._type(self.INPUT_DB_PORT, port)
        time.sleep(0.2)
        self._type(self.INPUT_DB_NAME, dbname)
        time.sleep(0.2)
        self._type(self.INPUT_DB_SCHEMA, schema)
        time.sleep(0.2)
        self._type(self.INPUT_DB_USER, username)
        time.sleep(0.2)
        self._type(self.INPUT_DB_PASS, password)
        time.sleep(0.2)

    def test_connection(self):
        self._click_safely(self.TEST_CONN)
        time.sleep(2)

    def save_datasource(self):
        self._click_safely(self.DS_SAVE)
        time.sleep(2)

    # ------------------ Select an existing DS by its visible card ID ------------------
    def show_all_and_select(self, datasource_card_id: str):
        self._click_safely(self.SHOW_ALL)
        time.sleep(1)
        self._click_safely((By.ID, datasource_card_id))
        time.sleep(1)

    # ------------------ Signature adjustments ------------------
    def open_signature(self):
        self._click_safely(self.SIGNATURE_BTN)
        time.sleep(1)

    def step_numeric_field(self, field_id: str, up_times: int = 1, down_times: int = 1):
        el = self.wait.until(EC.presence_of_element_located((By.ID, field_id)))
        from selenium.webdriver.common.keys import Keys
        for _ in range(max(0, up_times)):
            el.send_keys(Keys.ARROW_UP)
            time.sleep(0.2)
        for _ in range(max(0, down_times)):
            el.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.2)

    def apply_signature_update(self):
        self._click_safely(self.SIGNATURE_UPDATE)
        time.sleep(1)

    def open_edit_then_close(self):
        self._click_safely(self.EDIT_DS_BTN)
        time.sleep(1)
        self._click_safely(self.CLOSE_DIALOG)
        time.sleep(0.5)

    def download_data(self, confirm_with_os_shortcut: bool = False):
        self._click_safely(self.DOWNLOAD_BTN)
        time.sleep(2)
        if confirm_with_os_shortcut and pyautogui:
            try:
                pyautogui.hotkey('command', 'down')
                time.sleep(0.6)
                pyautogui.press('return')
                time.sleep(1.2)
            except Exception:
                pass

    def clear_navbar(self):
        try:
            self._click_safely(self.CLEAR_NAVBAR)
            time.sleep(0.6)
        except Exception:
            pass

    # ------------------ SQL Queries and Description ------------------
    def select_connection_by_id(self, connection_id: str):
        self._click_safely((By.ID, connection_id))
        time.sleep(1)

    def open_table_by_id(self, table_id: str):
        self._click_safely((By.ID, table_id))
        time.sleep(1)

    def open_sql_panel(self):
        self._click_safely(self.SQL_BTN)
        time.sleep(0.5)

    def set_sql_and_execute(self, query: str):
        editor = self.wait.until(EC.presence_of_element_located(self.SQL_INPUT))
        try:
            editor.clear()
        except Exception:
            self.driver.execute_script("arguments[0].value='';", editor)
        editor.send_keys(query)
        time.sleep(0.2)
        self._click_safely(self.SQL_EXECUTE)
        time.sleep(2)

    def clear_sql_if_button_present(self):
        try:
            self._click_safely(self.SQL_CLEAR)
            time.sleep(0.4)
        except Exception:
            pass

    def open_description_for_table(self, table_info_id: str):
        self._click_safely((By.ID, table_info_id))
        time.sleep(0.4)

    def set_description_and_save(self, text: str):
        el = self.wait.until(EC.presence_of_element_located(self.DESC_INPUT))
        try:
            el.clear()
        except Exception:
            self.driver.execute_script("arguments[0].value='';", el)
        el.send_keys(text)
        self._click_safely(self.DESC_SAVE)
        time.sleep(1)

    # ------------------ Shared delete button helper for alerts (used elsewhere if needed) ------------------
    def click_delete_and_accept_two_alerts(self, delete_button_id: str):
        self._click_safely((By.ID, delete_button_id))
        time.sleep(0.5)
        self._accept_alert_if_present(0.7)
        self._accept_alert_if_present(0.9)