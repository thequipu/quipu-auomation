# tests/datacatalog/test_add_data_source_oracle.py
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.datacatalog_page import DataCatalogPage


@pytest.mark.datacatalog
def test_add_oracle_datasource_and_signature(driver, config):
    wait = WebDriverWait(driver, 20)

    # ---------- login ----------
    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])
    lp.enter_tenant_id(config["tenant"])
    lp.click_proceed()
    lp.enter_username(config["username"])
    lp.enter_password(config["password"])
    lp.click_login()

    # ---------- go to Data Catalog ----------
    dcp = DataCatalogPage(driver, wait)
    dcp.open_datacatalog()
    dcp.click_add_new()
    dcp.choose_ds_type_oracle()

    # Use the same values from your original script
    dcp.fill_oracle_fields(
        name="kfc_y",
        description="kpnani",
        host="207.180.249.216",
        port="1521",
        dbname="FREE",
        schema="HETIONET",
        username="hetionet",
        password="hetionet",
    )
    dcp.test_connection_and_save()

    # ---------- open saved DS and tweak signature ----------
    dcp.show_all()
    time.sleep(1)
    dcp.select_ds_by_id("kfc_y")
    dcp.open_signature()
    dcp.tweak_signature_and_update()

    # ---------- edit/view dialog then close ----------
    dcp.edit_then_close()

    # ---------- download and clear ----------
    dcp.download_data_and_confirm()
    dcp.clear_search()

    # Keep a small pause for stability (your style)
    time.sleep(3)