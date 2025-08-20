from comparators.schema_comparator import SchemaComparator
from utils import load_schema_file
import os

def main():
    # Load JSON files
    correct_schema = load_schema_file('downloads/hetionet.json')
    incorrect_schema = load_schema_file('downloads/hetionet-1.json')

    # Compare JSONs
    comparator = SchemaComparator(correct_schema, incorrect_schema)
    differences, metrics = comparator.compare()

    # Prepare report
    report_lines = ["Schema JSON Comparison Report", "=" * 50, "\nNode Metrics:"]
    node_metrics_keys = [
        "count_datasource", "count_tables", "count_property", "count_nodes",
        "count_node_property", "count_node_relationship",
        "count_extra_datasource", "count_extra_tables", "count_extra_property",
        "count_extra_nodes", "count_extra_node_property", "count_extra_node_relationship"
    ]
    for key in node_metrics_keys:
        report_lines.append(f"- {key}: {metrics[key]}")

    report_lines.append("\nLink Metrics:")
    link_metrics_keys = [
        "count_has_tables", "count_has_property", "count_foreign_key",
        "count_maps_to_target_node_property", "count_composite_column",
        "count_has_node_relationship", "count_maps_to_column",
        "count_maps_to_foreign_key_column",
        "count_extra_has_tables", "count_extra_has_property", "count_extra_foreign_key",
        "count_extra_maps_to_target_node_property", "count_extra_composite_column",
        "count_extra_has_node_relationship", "count_extra_maps_to_column",
        "count_extra_maps_to_foreign_key_column"
    ]
    for key in link_metrics_keys:
        report_lines.append(f"- {key}: {metrics[key]}")

    report_lines.append(f"\nMissing Values Count: {metrics['missing_values']}")

    report_lines.append("\nDifferences found between correct and incorrect schema JSON:")
    if differences:
        for diff in differences:
            report_lines.append(f"- {diff}")
    else:
        report_lines.append("- No differences found.")

    # Ensure output directory exists
    os.makedirs('reports', exist_ok=True)
    output_path = 'reports/Comparison_hetionet_schema.txt'
    with open(output_path, 'w') as f:
        f.write("\n".join(report_lines))

    print(f"Schema comparison report generated at '{output_path}'.")

if __name__ == "__main__":
    main()
