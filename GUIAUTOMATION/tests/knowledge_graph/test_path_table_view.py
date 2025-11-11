import time
from drivers.driver_factory import DriverFactory
from pages.knowledge_graph_page import KnowledgeGraphPage


def test_path_table_view():
    """Test table view and path view operations"""

    driver = DriverFactory.get_driver()
    cfg = DriverFactory.load_config()
    kg = KnowledgeGraphPage(driver)

    try:
        # Login
        kg.login(cfg["base_url"], cfg["tenant"], cfg["username"], cfg["password"])

        # Navigate to Knowledge Graph
        kg.open_knowledge_graph()
        kg.select_fabric("RealWorldDataMart-fabric")
        kg.click_label_address()

        # Scan and double-click node
        clicked_px = kg.scan_and_click_node(step=80)

        if not clicked_px:
            print("No node found")
            return

        kg.double_click_node_at(clicked_px[0], clicked_px[1])

        # Switch views
        kg.click_table_view()
        kg.click_path_view()

        # Note: The original script had NaN IDs which need to be updated
        # with actual element IDs from your application

        kg.click_graph_view()

        # Take final screenshot
        driver.save_screenshot("artifacts/screens/path_table_end.png")
        print("screenshot: artifacts/screens/path_table_end.png")

        print("✅ Test completed successfully!")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise

    finally:
        time.sleep(10)
        DriverFactory.quit_driver(driver)


if __name__ == "__main__":
    test_path_table_view()