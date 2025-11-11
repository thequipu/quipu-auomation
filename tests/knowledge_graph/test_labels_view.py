import time
from drivers.driver_factory import DriverFactory
from pages.knowledge_graph_page import KnowledgeGraphPage


def test_labels_view():
    """Test complete Knowledge Graph workflow - zoom, search, query"""

    driver = DriverFactory.get_driver()
    cfg = DriverFactory.load_config()
    kg = KnowledgeGraphPage(driver)

    try:
        # Login
        kg.login(cfg["base_url"], cfg["tenant"], cfg["username"], cfg["password"])

        # Navigate to Knowledge Graph
        kg.open_knowledge_graph()
        kg.select_fabric("RealWorldDataMart-fabric")
        kg.click_label_listedsecurity()

        # Node config panel operations
        kg.open_node_config_panel()
        kg.open_node_configuration()
        kg.back_from_node_config_panel()

        # Canvas controls
        kg.zoom_out()
        kg.zoom_in(times=2)
        kg.fit_to_screen()
        kg.clear_graph_view()

        # Search and run query
        kg.search_and_enter("address")
        kg.run_query()

        print("✅ Test completed successfully!")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise

    finally:
        time.sleep(5)
        DriverFactory.quit_driver(driver)


if __name__ == "__main__":
    test_labels_view()