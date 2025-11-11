import csv
import time
import os
from drivers.driver_factory import DriverFactory
from pages.knowledge_graph_page import KnowledgeGraphPage


def test_rel_tooltips_collect():
    """Collect relationship tooltips and save to CSV and MD"""

    driver = DriverFactory.get_driver()
    cfg = DriverFactory.load_config()
    kg = KnowledgeGraphPage(driver)

    try:
        # Login
        kg.login(cfg["base_url"], cfg["tenant"], cfg["username"], cfg["password"])
        time.sleep(5)

        # Navigate to Knowledge Graph
        kg.open_knowledge_graph()
        time.sleep(6)

        # Collect tooltips
        rows = kg.collect_relationship_tooltips()

        # Save to CSV
        os.makedirs("artifacts", exist_ok=True)
        csv_path = "artifacts/relationship_tooltips.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["Relationship", "Tooltip"])
            w.writeheader()
            w.writerows(rows)

        # Save to Markdown
        md_path = "artifacts/relationship_tooltips.md"
        with open(md_path, "w", encoding="utf-8") as md:
            md.write("| Relationship | Tooltip |\n")
            md.write("|--------------|---------|\n")
            for r in rows:
                md.write(
                    f"| {r['Relationship'].replace('|', ' ')} | {r['Tooltip'].replace('|', ' ').replace(chr(10), ' ')} |\n")

        print(f"✅ Exported {len(rows)} rows to {csv_path} and {md_path}")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise

    finally:
        DriverFactory.quit_driver(driver)


if __name__ == "__main__":
    test_rel_tooltips_collect()