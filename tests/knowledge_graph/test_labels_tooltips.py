import csv
import time
import os
from drivers.driver_factory import DriverFactory
from pages.knowledge_graph_page import KnowledgeGraphPage


def test_labels_tooltips():
    """Simple tooltip collection test"""

    driver = DriverFactory.get_driver()
    cfg = DriverFactory.load_config()
    kg = KnowledgeGraphPage(driver)

    try:
        # Login
        kg.login(cfg["base_url"], cfg["tenant"], cfg["username"], cfg["password"])
        time.sleep(5)

        # Navigate to Knowledge Graph
        kg.open_knowledge_graph()
        time.sleep(8)

        # Collect simple tooltips
        tooltip_data = kg.collect_simple_tooltips()

        # Save to CSV
        os.makedirs("artifacts", exist_ok=True)
        csv_path = "artifacts/relationship_tooltips.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Relationship", "Tooltip"])
            writer.writeheader()
            writer.writerows(tooltip_data)

        print(f"✅ Exported {len(tooltip_data)} relationship tooltips to {csv_path}")

        # Verify
        with open(csv_path, "r", encoding="utf-8") as file:
            reader = list(csv.DictReader(file))
            print(f"Verified {len(reader)} rows read from file")
            assert len(reader) > 0, "No tooltips saved in the CSV file"

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise

    finally:
        DriverFactory.quit_driver(driver)


if __name__ == "__main__":
    test_labels_tooltips()