# GUIAUTOMATION/tests/document_linker/test_extract_document.py
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.document_linker_page import DocumentLinkerPage

@pytest.mark.document_linker
def test_extract_document(driver, config):
    wait = WebDriverWait(driver, 30)

    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])
    lp.enter_tenant_and_proceed(config["tenant"])
    lp.login(config["username"], config["password"])

    dl = DocumentLinkerPage(driver, wait)
    dl.open_menu()
    dl.goto_document_linker()
    dl.open_extract_dialog()

    dl.select_slinker_by_index(12)
    dl.select_datasource_by_index(0)

    dl.click_extract()
    time.sleep(2)