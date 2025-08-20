# from typing import List, Dict, Any


# class JSONSchemaComparator:
#     def __init__(self, correct: dict, incorrect: dict):
#         self.correct = correct
#         self.incorrect = incorrect
#         self.differences = []

#     def compare(self) -> List[str]:
#         self.differences.clear()
#         self._compare_nodes()
#         self._compare_links()
#         return self.differences

#     def _compare_nodes(self):
#         correct_nodes = {n["id"]: n for n in self.correct.get("nodes", [])}
#         incorrect_nodes = {n["id"]: n for n in self.incorrect.get("nodes", [])}

#         # Missing nodes
#         for node_id in correct_nodes:
#             if node_id not in incorrect_nodes:
#                 self.differences.append(f"Missing node in v2: {node_id}")
#         # Extra nodes
#         for node_id in incorrect_nodes:
#             if node_id not in correct_nodes:
#                 self.differences.append(f"Extra node in v2: {node_id}")

#         # Compare common nodes
#         for node_id in set(correct_nodes) & set(incorrect_nodes):
#             self._compare_dicts(correct_nodes[node_id], incorrect_nodes[node_id], f"Node {node_id}")

#     def _compare_links(self):
#         correct_links = {l["identity"]: l for l in self.correct.get("links", [])}
#         incorrect_links = {l["identity"]: l for l in self.incorrect.get("links", [])}

#         # Missing links
#         for link_id in correct_links:
#             if link_id not in incorrect_links:
#                 self.differences.append(f"Missing link in v2: {link_id}")
#         # Extra links
#         for link_id in incorrect_links:
#             if link_id not in correct_links:
#                 self.differences.append(f"Extra link in v2: {link_id}")

#         # Compare common links
#         for link_id in set(correct_links) & set(incorrect_links):
#             self._compare_dicts(correct_links[link_id], incorrect_links[link_id], f"Link {link_id}")

#     def _compare_dicts(self, d1: Dict[str, Any], d2: Dict[str, Any], path: str):
#         for key in set(d1.keys()) | set(d2.keys()):
#             v1 = d1.get(key)
#             v2 = d2.get(key)
#             if v1 != v2:
#                 self.differences.append(f"{path} - Field '{key}' mismatch: v1={v1} v2={v2}")

# import json

# with open("CustomerOrderSchema-v1.json") as f:
#     v1 = json.load(f)
# with open("CustomerOrderSchema-v2.json") as f:
#     v2 = json.load(f)

# comparator = JSONSchemaComparator(v1, v2)
# diffs = comparator.compare()

# for d in diffs:
#     print(d)
#-------------------------------------------------------------------------

import json
from deepdiff import DeepDiff
from collections import defaultdict


def load_json(file_path):
    """Load JSON file and return its content."""
    with open(file_path, 'r') as f:
        return json.load(f)

def count_node_types(schema):
    """Count node types in the schema."""
    node_counts = defaultdict(int)
    for node in schema.get('nodes', []):
        node_type = node.get('node_type')
        node_counts[node_type] += 1
    return node_counts

def count_link_types(schema):
    """Count link relationship types in the schema."""
    link_counts = defaultdict(int)
    for link in schema.get('links', []):
        relationship = link.get('relationship')
        link_counts[relationship] += 1
    return link_counts

def compare_schemas(golden_json, test_json):
    """Compare two JSON schemas and return differences and metrics."""
    # Perform deep comparison
    diff = DeepDiff(golden_json, test_json, ignore_order=True, report_repetition=True)
    
    # Initialize metrics
    metrics = {
        'nodes': {
            'data_source': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'tables': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'property': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'nodes': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'node_property': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'node_relationship': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'missing_values': []
        },
        'links': {
            'has_tables': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'has_property': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'Foreign_Key': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'maps_to_target_node_property': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'composite_column': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'has_node_property': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'has_node_relationship': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'maps_to_column': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'maps_to_foreign_key_column': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'customer_id': {'v1': 0, 'v2': 0, 'extra_v2': 0, 'missing_v2': 0},
            'missing_values': []
        }
    }

    # Count nodes
    v1_node_counts = count_node_types(golden_json)
    v2_node_counts = count_node_types(test_json)
    
    # Map node types to metrics keys
    node_type_mapping = {
        'data_source': 'data_source',
        'table': 'tables',
        'property': 'property',
        'Node': 'nodes',
        'Node Property': 'node_property',
        'Node Relationship': 'node_relationship'
    }
    
    for node_type, metric_key in node_type_mapping.items():
        metrics['nodes'][metric_key]['v1'] = v1_node_counts.get(node_type, 0)
        metrics['nodes'][metric_key]['v2'] = v2_node_counts.get(node_type, 0)
        metrics['nodes'][metric_key]['extra_v2'] = max(0, v2_node_counts.get(node_type, 0) - v1_node_counts.get(node_type, 0))
        metrics['nodes'][metric_key]['missing_v2'] = max(0, v1_node_counts.get(node_type, 0) - v2_node_counts.get(node_type, 0))
    
    # Count links
    v1_link_counts = count_link_types(golden_json)
    v2_link_counts = count_link_types(test_json)
    
    for rel_type in metrics['links'].keys():
        if rel_type != 'missing_values':
            metrics['links'][rel_type]['v1'] = v1_link_counts.get(rel_type, 0)
            metrics['links'][rel_type]['v2'] = v2_link_counts.get(rel_type, 0)
            metrics['links'][rel_type]['extra_v2'] = max(0, v2_link_counts.get(rel_type, 0) - v1_link_counts.get(rel_type, 0))
            metrics['links'][rel_type]['missing_v2'] = max(0, v1_link_counts.get(rel_type, 0) - v2_link_counts.get(rel_type, 0))
    
    # Extract missing nodes and links
    if 'iterable_item_removed' in diff:
        for path, value in diff['iterable_item_removed'].items():
            if path.startswith("root['nodes']"):
                metrics['nodes']['missing_values'].append(value)
            elif path.startswith("root['links']"):
                metrics['nodes']['missing_values'].append(value)
    
    return diff, metrics

def generate_report(diff, metrics):
    """Generate a comparison report."""
    report = "# JSON Schema Comparison Report\n\n"
    
    report += "## Node Metrics\n"
    for metric, counts in metrics['nodes'].items():
        if metric != 'missing_values':
            report += f"- {metric.replace('_', ' ').title()}:\n"
            report += f"  - v1 Count: {counts['v1']}\n"
            report += f"  - v2 Count: {counts['v2']}\n"
            report += f"  - Extra in v2: {counts['extra_v2']}\n"
            report += f"  - Missing in v2: {counts['missing_v2']}\n"
    
    report += "\n## Link Metrics\n"
    for metric, counts in metrics['links'].items():
        if metric != 'missing_values':
            report += f"- {metric.replace('_', ' ').title()}:\n"
            report += f"  - v1 Count: {counts['v1']}\n"
            report += f"  - v2 Count: {counts['v2']}\n"
            report += f"  - Extra in v2: {counts['extra_v2']}\n"
            report += f"  - Missing in v2: {counts['missing_v2']}\n"
    
    report += "\n## Missing Values in v2\n"
    if metrics['nodes']['missing_values']:
        report += "### Nodes\n"
        for item in metrics['nodes']['missing_values']:
            report += f"- {json.dumps(item, indent=2)}\n"
    
    if metrics['links']['missing_values']:
        report += "### Links\n"
        for item in metrics['links']['missing_values']:
            report += f"- {json.dumps(item, indent=2)}\n"
    
    return report

def main():
    # Load JSON files
    golden_json = load_json('CustomerOrderSchema-v1.json')
    test_json = load_json('CustomerOrderSchema-v2.json')
    
    # Compare schemas
    diff, metrics = compare_schemas(golden_json, test_json)
    
    # Generate report
    report = generate_report(diff, metrics)
    
    # Save report
    with open('schema_comparison_report.md', 'w') as f:
        f.write(report)
    
    print("Comparison report generated: schema_comparison_report.md")

if __name__ == "__main__":
    main()