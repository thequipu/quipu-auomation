import time
from drivers.driver_factory import DriverFactory
from pages.knowledge_graph_page import KnowledgeGraphPage


def test_double_click_node():
    """Test double-click on node to navigate to next graph"""

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

        # Scan and click first node
        clicked_px = kg.scan_and_click_node(step=80)

        if not clicked_px:
            print("No node found on canvas")
            return

        # Double-click same node
        kg.double_click_node_at(clicked_px[0], clicked_px[1])

        print("✅ Test completed successfully!")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise

    finally:
        time.sleep(10)
        DriverFactory.quit_driver(driver)


if __name__ == "__main__":
    test_double_click_node()