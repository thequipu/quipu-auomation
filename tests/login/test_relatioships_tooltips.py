# login/test_tooltips_labels_relationships.py
import json
import time
from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.fabric_page import FabricPage
from pages.knowledge_graph_page import KnowledgeGraphPage

def test_labels_tooltips():
    # Load config
    with open("config/config.json") as f:
        config = json.load(f)

    driver,wait = DriverFactory.get_driver()

    # Login
    login_page = LoginPage(driver)
    login_page.open(config["base_url"])
    login_page.enter_tenant(config["tenant"])
    login_page.click_proceed()
    login_page.enter_username(config["username"])
    login_page.enter_password(config["password"])
    login_page.click_login()
    time.sleep(2)

    # Navigate to Real World DataMart
    fabric_page = FabricPage(driver)
    fabric_page.open_real_world_datamart()
    time.sleep(2)

    # Open Knowledge Graph
    kg_page = KnowledgeGraphPage(driver)
    kg_page.open()
    time.sleep(2)

    # Write CSV to artifacts/ and read it back
    csv_path = kg_page.export_labels_to_csv("artifacts/labels_tooltips.csv")
    rows = kg_page.read_labels_from_csv(csv_path)

    # Print readback
    for r in rows:
        print(f"CSV -> Label: {r['Label']} | Tooltip: {r['Tooltip']}")

    time.sleep(2)
    driver.quit()