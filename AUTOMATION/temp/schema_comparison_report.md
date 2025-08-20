# JSON Schema Comparison Report

## Node Metrics
- Data Source:
  - v1 Count: 1
  - v2 Count: 1
  - Extra in v2: 0
  - Missing in v2: 0
- Tables:
  - v1 Count: 2
  - v2 Count: 2
  - Extra in v2: 0
  - Missing in v2: 0
- Property:
  - v1 Count: 10
  - v2 Count: 9
  - Extra in v2: 0
  - Missing in v2: 1
- Nodes:
  - v1 Count: 2
  - v2 Count: 2
  - Extra in v2: 0
  - Missing in v2: 0
- Node Property:
  - v1 Count: 9
  - v2 Count: 9
  - Extra in v2: 0
  - Missing in v2: 0
- Node Relationship:
  - v1 Count: 1
  - v2 Count: 1
  - Extra in v2: 0
  - Missing in v2: 0

## Link Metrics
- Has Tables:
  - v1 Count: 2
  - v2 Count: 2
  - Extra in v2: 0
  - Missing in v2: 0
- Has Property:
  - v1 Count: 10
  - v2 Count: 9
  - Extra in v2: 0
  - Missing in v2: 1
- Foreign Key:
  - v1 Count: 1
  - v2 Count: 1
  - Extra in v2: 0
  - Missing in v2: 0
- Maps To Target Node Property:
  - v1 Count: 1
  - v2 Count: 1
  - Extra in v2: 0
  - Missing in v2: 0
- Composite Column:
  - v1 Count: 2
  - v2 Count: 2
  - Extra in v2: 0
  - Missing in v2: 0
- Has Node Property:
  - v1 Count: 10
  - v2 Count: 10
  - Extra in v2: 0
  - Missing in v2: 0
- Has Node Relationship:
  - v1 Count: 1
  - v2 Count: 1
  - Extra in v2: 0
  - Missing in v2: 0
- Maps To Column:
  - v1 Count: 10
  - v2 Count: 10
  - Extra in v2: 0
  - Missing in v2: 0
- Maps To Foreign Key Column:
  - v1 Count: 1
  - v2 Count: 1
  - Extra in v2: 0
  - Missing in v2: 0
- Customer Id:
  - v1 Count: 1
  - v2 Count: 1
  - Extra in v2: 0
  - Missing in v2: 0

## Missing Values in v2
### Nodes
- {
  "id": "urn:li:dataset:postgres:automation_test:public:dataset:customers:first_name",
  "node_type": "property",
  "label": "first_name",
  "data_type": "VARCHAR(50)",
  "nullable": false,
  "primary_key": false,
  "unique_key": false,
  "foreign_key": false,
  "composite_key": null,
  "identity": "d32ea8b8-43cf-4517-afe4-d1da55ebdb6d"
}
- {
  "source": "urn:li:dataset:postgres:automation_test:public:dataset:customers",
  "target": "urn:li:dataset:postgres:automation_test:public:dataset:customers:customer_id",
  "relationship": "has_property",
  "node_uri": "urn:li:dataset:postgres:automation_test:public:dataset:customers",
  "rel_uri": "",
  "prefLabel": false,
  "altLabel": false,
  "primaryKey": false,
  "uniqueKey": false,
  "identity": "9a94ce4b-8bba-4af9-8405-1dae20580bb3",
  "target_node_uri": "",
  "pathIds": [],
  "metrics": {},
  "target_column": "",
  "dashed": false
}
