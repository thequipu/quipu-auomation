# tests/schema/adddnew_nodeclick.py
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.schema_page import SchemaPage
from utils.canvas_helper import get_canvas, get_canvas_rect, capture_panel_screenshots

def test_add_new_node_click_flow():
    cfg = DriverFactory.load_config("config/config.json")
    driver, wait = DriverFactory.get_driver()

    try:
        # ----- login (exactly your working flow, but via POM + config) -----
        lp = LoginPage(driver, wait)
        lp.open(cfg["base_url"])
        lp.enter_tenant(cfg["tenant"]); time.sleep(1)
        lp.click_proceed()
        lp.enter_username(cfg["username"])
        lp.enter_password(cfg["password"])
        lp.click_login()

        # ----- schema create + builder open (your IDs preserved) -----
        sp = SchemaPage(driver)
        sp.open_menu()
        sp.start_add_new()
        sp.fill_basic_details("K1", "K11", "nani")
        sp.create_schema_open_builder()
        sp.attach_tables_from_typeahead("KYC_MINI")

        # ----- canvas interactions (your CDP + detection logic) -----
        canvas = get_canvas(driver)
        rect = get_canvas_rect(driver, canvas)
        shots = capture_panel_screenshots(driver, rect, want=2, prefix="dot_")
        assert shots >= 1, "No panel screenshots captured"

    finally:
        time.sleep(1.0)
        driver.quit()