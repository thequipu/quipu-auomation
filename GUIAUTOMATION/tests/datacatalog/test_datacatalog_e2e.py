# tests/datacatalog/test_datacatalog_e2e.py
import os
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.datacatalog_page import DataCatalogPage


def save_shot(driver, name):
    path = os.path.join("artifacts", "screens", "datacatalog", f"{name}.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.save_screenshot(path)


@pytest.mark.datacatalog
def test_datacatalog_end_to_end(driver, config):
    wait = WebDriverWait(driver, 20)

    # ---------------- Login ----------------
    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])
    lp.enter_tenant_id(config["tenant"])
    lp.click_proceed()
    lp.enter_username(config["username"])
    lp.enter_password(config["password"])
    lp.click_login()
    time.sleep(1.5)
    save_shot(driver, "00_after_login")

    # ---------------- Go to Data Catalog ----------------
    dcp = DataCatalogPage(driver, wait)
    dcp.goto_datacatalog()
    save_shot(driver, "01_datacatalog_page")

    # ---------------- Add Oracle Data Source ----------------
    dcp.click_add_new()
    dcp.choose_oracle_type()
    save_shot(driver, "02_add_new_oracle_open")

    dcp.fill_oracle_form(
        name="kfc_y",
        description="kpnani",
        host="207.180.249.216",
        port="1521",
        dbname="FREE",
        schema="HETIONET",
        username="hetionet",
        password="hetionet",
    )
    save_shot(driver, "03_form_filled")

    dcp.test_connection()
    save_shot(driver, "04_after_test_connection")

    dcp.save_datasource()
    time.sleep(4)
    save_shot(driver, "05_after_save_datasource")

    # ---------------- Select created DS → Signature → Edit/Close → Download ----------------
    dcp.show_all_and_select("kfc_y")
    save_shot(driver, "06_ds_card_open")

    dcp.open_signature()
    save_shot(driver, "07_signature_open")

    dcp.step_numeric_field("sampleSize", up_times=1, down_times=1)
    dcp.step_numeric_field("iterations", up_times=1, down_times=1)
    dcp.apply_signature_update()
    save_shot(driver, "08_signature_updated")

    dcp.open_edit_then_close()
    save_shot(driver, "09_edit_dialog_closed")

    dcp.download_data(confirm_with_os_shortcut=False)  # keep False on mac unless pyautogui is granted
    save_shot(driver, "10_after_download_click")

    dcp.clear_navbar()
    save_shot(driver, "11_after_clear_nav")

    # ---------------- SQL Queries + Description (uses your existing DEV connection) ----------------
    dcp.show_all_and_select("show-ds-btn")  # show all again (id kept as per your code)
    dcp.select_connection_by_id("dev_policyadmin2_connacted")
    time.sleep(1)
    save_shot(driver, "12_dev_connection_open")

    dcp.open_table_by_id("payments")
    time.sleep(1)
    save_shot(driver, "13_payments_table_open")

    dcp.open_sql_panel()
    dcp.set_sql_and_execute("SELECT Amount_paid FROM payments LIMIT 10;")
    save_shot(driver, "14_query1_results")

    dcp.clear_sql_if_button_present()

    dcp.set_sql_and_execute(
        "SELECT payment_status, COUNT(*) FROM payments GROUP BY payment_status;"
    )
    save_shot(driver, "15_query2_results")

    dcp.open_description_for_table("info-payments")
    dcp.set_description_and_save("Auto description note")
    save_shot(driver, "16_description_saved")

    # If we reached here without exceptions, consider it a pass
    assert True