import time
from drivers.driver_factory import DriverFactory
from pages.knowledge_graph_page import KnowledgeGraphPage


def test_node_dots():
    """Test clicking 2 nodes and capturing screenshots"""

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

        # Click 2 nodes and take screenshots
        shots = kg.click_two_nodes_with_screenshots(step=80)

        print(f"✅ Test completed! Captured {shots} screenshots")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise

    finally:
        time.sleep(1)
        DriverFactory.quit_driver(driver)


if __name__ == "__main__":
    test_node_dots()