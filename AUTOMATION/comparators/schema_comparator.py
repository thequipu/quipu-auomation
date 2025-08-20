from typing import List, Dict, Any, Tuple
from models.schema_models import Schema, Node, Relationship, BaseModel

class SchemaComparator:
    def __init__(self, correct: Schema, incorrect: Schema):
        self.correct = correct
        self.incorrect = incorrect
        self.differences: List[str] = []
        self.metrics: Dict[str, int] = {key: 0 for key in [
            # Node metrics
            "count_datasource", "count_tables", "count_property", "count_nodes",
            "count_node_property", "count_node_relationship",
            "count_extra_datasource", "count_extra_tables", "count_extra_property",
            "count_extra_nodes", "count_extra_node_property", "count_extra_node_relationship",
            # Links metrics
            "count_has_tables", "count_has_property", "count_foreign_key",
            "count_maps_to_target_node_property", "count_composite_column",
            "count_has_node_relationship", "count_maps_to_column",
            "count_maps_to_foreign_key_column",
            "count_extra_has_tables", "count_extra_has_property", "count_extra_foreign_key",
            "count_extra_maps_to_target_node_property", "count_extra_composite_column",
            "count_extra_has_node_relationship", "count_extra_maps_to_column",
            "count_extra_maps_to_foreign_key_column",
            # Missing
            "missing_values"
        ]}

    def compare(self) -> Tuple[List[str], Dict[str, int]]:
        self.differences.clear()
        self._compare_prefix()
        self._compare_nodes()
        self._compare_links()
        return self.differences, self.metrics

    def _to_dict(self, val: Any) -> Any:
        if isinstance(val, BaseModel):
            return val.dict()
        elif isinstance(val, list):
            return [self._to_dict(item) for item in val]
        else:
            return val

    def _compare_prefix(self):
        if self.correct.prefix != self.incorrect.prefix:
            self.differences.append(
                f"Prefix mismatch: Correct='{self.correct.prefix}', Current Value='{self.incorrect.prefix}'"
            )
            self.metrics["missing_values"] += 1

    # NODE COMPARISON
    def _compare_nodes(self):
        correct_nodes = {n.id: n for n in self.correct.nodes}
        incorrect_nodes = {n.id: n for n in self.incorrect.nodes}

        # Count totals
        self.metrics["count_nodes"] = len(self.correct.nodes)
        self.metrics["count_tables"] = sum(1 for n in self.correct.nodes if n.node_type == "table")
        self.metrics["count_property"] = sum(1 for n in self.correct.nodes if n.node_type == "property")
        self.metrics["count_datasource"] = sum(1 for n in self.correct.nodes if n.node_type == "datasource")
        self.metrics["count_node_property"] = sum(1 for n in self.correct.nodes if n.node_type == "node_property")
        self.metrics["count_node_relationship"] = sum(1 for n in self.correct.nodes if n.node_type == "node_relationship")

        # Missing
        for node_id, node in correct_nodes.items():
            if node_id not in incorrect_nodes:
                self.differences.append(f"Node '{node_id}' missing in newly generated JSON")
                self.metrics["missing_values"] += 1
        # Extra
        for node_id, node in incorrect_nodes.items():
            if node_id not in correct_nodes:
                self.differences.append(f"Extra node '{node_id}' in newly generated JSON")
                key = f"count_extra_{node.node_type}" if f"count_extra_{node.node_type}" in self.metrics else "count_extra_nodes"
                self.metrics[key] += 1

        # Compare common
        for node_id in set(correct_nodes) & set(incorrect_nodes):
            self._compare_node_fields(correct_nodes[node_id], incorrect_nodes[node_id], node_id)

    def _compare_node_fields(self, correct_node: Node, incorrect_node: Node, node_id: str):
        for field in correct_node.__fields__:
            if field == "identity":  # Skip identity field
                continue
            correct_val = getattr(correct_node, field)
            incorrect_val = getattr(incorrect_node, field, None)
            if correct_val != incorrect_val:
                self.differences.append(
                    f"Node '{node_id}' {field} mismatch: Correct={self._to_dict(correct_val)}, Current Value={self._to_dict(incorrect_val)}"
                )
                self.metrics["missing_values"] += 1

    # LINK COMPARISON
    def _compare_links(self):
        correct_links = {l.identity: l for l in self.correct.links}
        incorrect_links = {l.identity: l for l in self.incorrect.links}

        # Count totals
        self.metrics["count_has_tables"] = sum(1 for l in self.correct.links if l.relationship == "has_table")
        self.metrics["count_has_property"] = sum(1 for l in self.correct.links if l.relationship == "has_property")
        self.metrics["count_foreign_key"] = sum(1 for l in self.correct.links if l.relationship == "foreign_key")
        self.metrics["count_maps_to_target_node_property"] = sum(1 for l in self.correct.links if l.relationship == "maps_to_target_node_property")
        self.metrics["count_composite_column"] = sum(1 for l in self.correct.links if l.relationship == "composite_column")
        self.metrics["count_has_node_relationship"] = sum(1 for l in self.correct.links if l.relationship == "has_node_relationship")
        self.metrics["count_maps_to_column"] = sum(1 for l in self.correct.links if l.relationship == "maps_to_column")
        self.metrics["count_maps_to_foreign_key_column"] = sum(1 for l in self.correct.links if l.relationship == "maps_to_foreign_key_column")

        # Missing
        for link_id, link in correct_links.items():
            if link_id not in incorrect_links:
                self.differences.append(
                    f"Link from '{link.source}' to '{link.target}' with relationship '{link.relationship}' missing in newly generated JSON"
                )
                self.metrics["missing_values"] += 1

        # Extra
        for link_id, link in incorrect_links.items():
            if link_id not in correct_links:
                self.differences.append(
                    f"Extra link from '{link.source}' to '{link.target}' with relationship '{link.relationship}' in newly generated JSON"
                )
                key = f"count_extra_{link.relationship}" if f"count_extra_{link.relationship}" in self.metrics else None
                if key and key in self.metrics:
                    self.metrics[key] += 1

        # Compare common
        for link_id in set(correct_links) & set(incorrect_links):
            self._compare_link_fields(correct_links[link_id], incorrect_links[link_id], link_id)

    def _compare_link_fields(self, correct_link: Relationship, incorrect_link: Relationship, link_id: str):
        for field in correct_link.__fields__:
            if field == "identity": #skip the field
                continue
            correct_val = getattr(correct_link, field)
            incorrect_val = getattr(incorrect_link, field, None)
            if correct_val != incorrect_val:
                self.differences.append(
                    f"Link from '{correct_link.source}' to '{correct_link.target}' with relationship '{correct_link.relationship}' {field} mismatch: Correct={self._to_dict(correct_val)}, Incorrect={self._to_dict(incorrect_val)}"
                )
                self.metrics["missing_values"] += 1

