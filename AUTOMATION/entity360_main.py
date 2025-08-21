# from Entity_360.E360_validator import validate_schema

# def save_report(schema_file, output_file):
#     results = validate_schema(schema_file)

#     with open(output_file, "w") as f:
#         f.write("Entity 360 Path Validation Report\n" + "-"*40 + "\n")
#         for pid, info in results.items():
#             f.write(f"PathId: {pid}\n")
#             f.write(f"  Total Nodes       : {info['total_nodes']}\n")
#             f.write(f"  Total Edges       : {info['total_edges']}\n")
#             f.write(f"  Connected         : {info['connected']}\n")
#             f.write(f"  Dangling          : {info['dangling']}\n")
#             if info["missing_nodes"]:
#                 f.write(f"  Missing Nodes     : {info['missing_nodes']}\n")
#             if info["dangling_nodes"]:
#                 f.write(f"  Dangling Nodes    : {info['dangling_nodes']}\n")
#             if info["disconnected_nodes"]:
#                 f.write(f"  Disconnected Nodes: {info['disconnected_nodes']}\n")
#             f.write("\n")

#         # Summary
#         total_paths = len(results)
#         dangling_count = sum(1 for r in results.values() if r["dangling"])
#         connected_count = sum(1 for r in results.values() if r["connected"])
#         f.write("Summary\n" + "-"*20 + "\n")
#         f.write(f"Total Paths   : {total_paths}\n")
#         f.write(f"Connected     : {connected_count}\n")
#         f.write(f"Dangling      : {dangling_count}\n")

#     print(f"Report saved to {output_file}")

# if __name__ == "__main__":
#     schema_file = "downloads/e360test1schema.json" 
#     output_file = "reports/e360test1_report.txt"
#     save_report(schema_file, output_file)

#--------------------------------------------------------------------------------------------

from Entity_360.E360_validator import validate_schema


def save_report(schema_file, output_file):
    results = validate_schema(schema_file)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Entity 360 Path Validation Report\n")
        f.write("=" * 50 + "\n\n")

        for pid, info in results.items():
            f.write(f"PathId: {pid}\n")
            f.write(f"  - Total Nodes   : {info['total_nodes']}\n")
            f.write(f"  - Total Edges   : {info['total_edges']}\n")

            if info["dangling"]:
                f.write("  - Status        : Dangling path (no edges)\n")
                f.write(f"    Nodes with no connections: {info['dangling_nodes']}\n")
            elif info["disconnected_nodes"]:
                f.write("  - Status        : Broken path\n")
                f.write(f"    Unreachable nodes: {info['disconnected_nodes']}\n")
            elif info["missing_nodes"]:
                f.write("  - Status        : Missing nodes in schema\n")
                f.write(f"    Missing: {info['missing_nodes']}\n")
            else:
                f.write("  - Status        : Fully connected path\n")

            f.write("\n")

    print(f" Human-readable report saved to {output_file}")


if __name__ == "__main__":
    schema_file = "downloads/e360_case3_partial_disconnect.json"
    output_file = "reports/e360test1_report.txt"
    save_report(schema_file, output_file)
