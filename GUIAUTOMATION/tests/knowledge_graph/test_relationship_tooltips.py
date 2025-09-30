# tests/knowledge_graph/test_relationship_tooltips.py
from pages.fabric_page import FabricPage
from pages.knowledge_graph_page import KnowledgeGraphPage

def test_relationship_tooltips(login):
    # Already logged in via fixture
    fabric = FabricPage(login)
    fabric.open_real_world_datamart()

    kg = KnowledgeGraphPage(login)
    kg.open()

    csv_path = kg.export_relationships_to_csv("artifacts/relationships_tooltips.csv")
    rows = kg.read_relationships_from_csv(csv_path)

    for r in rows:
        print(f"Relationship: {r['Relationship']} | Tooltip: {r['Tooltip']}")

    # Assertions
    assert len(rows) > 0, "No relationships exported! Check locators or page state."
    assert all(r['Tooltip'] for r in rows), "Some relationships have empty tooltips!"