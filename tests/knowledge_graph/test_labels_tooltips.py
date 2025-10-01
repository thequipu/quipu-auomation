from pages.fabric_page import FabricPage
from pages.knowledge_graph_page import KnowledgeGraphPage

def test_labels_tooltips(login):
    # Already logged in (login fixture)
    fabric = FabricPage(login)
    fabric.open_real_world_datamart()

    kg = KnowledgeGraphPage(login)
    kg.open()

    csv_path = kg.export_labels_to_csv("artifacts/labels_tooltips.csv")
    rows = kg.read_labels_from_csv(csv_path)

    for r in rows:
        print(f"Label: {r['Label']} | Tooltip: {r['Tooltip']}")

    assert len(rows) > 0, "No labels exported!"
    assert all(r['Tooltip'] for r in rows), "Some labels have empty tooltips!"