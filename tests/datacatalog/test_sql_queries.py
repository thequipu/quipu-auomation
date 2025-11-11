# tests/datacatalog/test_sql_queries.py
import os
import time
import json
import pytest

from selenium.webdriver.support.ui import WebDriverWait

from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.datacatalog_page import DataCatalogPage


def read_config():
    with open("config/config.json", "r") as f:
        return json.load(f)


def screenshot(driver, name):
    path = os.path.join("artifacts", f"{name}.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.save_screenshot(path)


@pytest.mark.datacatalog
def test_sql_queries_and_description():
    cfg = read_config()
    driver = DriverFactory.get_driver(cfg)
    wait = WebDriverWait(driver, 20)

    # test inputs from your original script
    datasource_id = "dev_policyadmin2_connacted"   # keep your exact ID
    table_id = "payments"                          # keep your exact ID
    first_sql = "SELECT Amount_paid FROM payments LIMIT 10;"
    second_sql = "SELECT payment_status, COUNT(*) FROM payments GROUP BY payment_status;"
    desc_text = "Auto description note"

    try:
        # ---------------- Login ----------------
        lp = LoginPage(driver, wait)
        lp.open(cfg["base_url"])
        lp.enter_tenant_id(cfg["tenant"])
        lp.click_proceed()
        lp.enter_username(cfg["username"])
        lp.enter_password(cfg["password"])
        lp.click_login()
        time.sleep(2)

        # ---------------- Navigate: Data Catalog ----------------
        dcp = DataCatalogPage(driver, wait)
        dcp.open()                  # hamburger -> Data Catalog
        dcp.click_show_all()
        dcp.select_datasource_by_id(datasource_id)

        # ---------------- Table + SQL #1 ----------------
        dcp.open_table_by_id(table_id)
        screenshot(driver, "01_payments_selected")

        dcp.open_sql_panel()
        dcp.set_sql_and_execute(first_sql)
        screenshot(driver, "02_first_query_results")

        # ---------------- SQL #2 ----------------
        dcp.clear_sql_if_available()
        dcp.set_sql_and_execute(second_sql)
        screenshot(driver, "03_second_query_results")

        # ---------------- Description ----------------
        dcp.open_description_for_table(table_id)
        dcp.set_description_and_save(desc_text)
        screenshot(driver, "04_description_added")

    finally:
        driver.quit()