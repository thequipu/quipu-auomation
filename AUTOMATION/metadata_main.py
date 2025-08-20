from comparators.metadata_comparator import MetadataComparator
from utils import load_metadata_file

def main():
    # Load JSON files (adjust paths if in downloads/)
    correct_metadata = load_metadata_file('downloads/hetionet_d.json')
    incorrect_metadata = load_metadata_file('downloads/hetionet_d-1.json')

    # Compare JSONs
    comparator = MetadataComparator(correct_metadata, incorrect_metadata)
    differences, metrics = comparator.compare()

    # Prepare report content
    report_lines = ["JSON Comparison Report"]
    report_lines.append("=" * 50)
    report_lines.append("\nMetrics:")
    report_lines.append(f"- Number of datasets (Golden Metadata): {metrics['dataset_count_correct']}")
    report_lines.append(f"- Number of datasets (New Metadata): {metrics['dataset_count_incorrect']}")
    report_lines.append(f"- Number of properties (Golden Metadata): {metrics['properties_count_correct']}")
    report_lines.append(f"- Number of properties (New Metadata): {metrics['properties_count_incorrect']}")
    report_lines.append(f"- Number of relationships (Golden Metadata): {metrics['relationships_count_correct']}")
    report_lines.append(f"- Number of relationships (New Metadata): {metrics['relationships_count_incorrect']}")
    report_lines.append(f"- Number of extra properties: {metrics['extra_properties_count']}")
    report_lines.append(f"- Number of extra datasets: {metrics['extra_datasets_count']}")
    report_lines.append(f"- Number of extra relationships: {metrics['extra_relationships_count']}")
    report_lines.append(f"- Number of missing values: {metrics['missing_values_count']}")
    report_lines.append("\nDifferences found between correct and incorrect JSON:")
    if differences:
        for diff in differences:
            report_lines.append(f"- {diff}")
    else:
        report_lines.append("- No differences found.")

    # Write to file (output to downloads/)
    output_path = "reports/Comparison_hetionet_metadata.txt"
    with open(output_path, 'w') as f:
        f.write("\n".join(report_lines))

    print(f"Comparison report generated in '{output_path}'.")

if __name__ == "__main__":
    main()