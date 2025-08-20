import json

with open("CustomerOrderSchema-v1.json") as f:
    v1 = json.load(f)
with open("CustomerOrderSchema-v2.json") as f:
    v2 = json.load(f)

comparator = JSONSchemaComparator(v1, v2)
diffs = comparator.compare()

for d in diffs:
    print(d)
