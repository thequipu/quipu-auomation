from typing import List, Dict, Any
from models.metadata_models import Metadata, DataSet, Property, Relationship, BaseModel

class MetadataComparator:
    def __init__(self, correct: Metadata, incorrect: Metadata):
        self.correct = correct
        self.incorrect = incorrect
        self.differences = []
        self.metrics = {
            "dataset_count_correct": 0,
            "dataset_count_incorrect": 0,
            "properties_count_correct": 0,
            "properties_count_incorrect": 0,
            "relationships_count_correct": 0,
            "relationships_count_incorrect": 0,
            "extra_properties_count": 0,
            "extra_datasets_count": 0,
            "extra_relationships_count": 0,
            "missing_values_count": 0
        }

    def compare(self) -> tuple[List[str], Dict[str, int]]:
        self.differences = []
        self.metrics = {
            "dataset_count_correct": len(self.correct.dataSets),
            "dataset_count_incorrect": len(self.incorrect.dataSets),
            "properties_count_correct": sum(len(ds.properties) for ds in self.correct.dataSets),
            "properties_count_incorrect": sum(len(ds.properties) for ds in self.incorrect.dataSets),
            "relationships_count_correct": sum(len(ds.dataSetRelationShips) for ds in self.correct.dataSets),
            "relationships_count_incorrect": sum(len(ds.dataSetRelationShips) for ds in self.incorrect.dataSets),
            "extra_properties_count": 0,
            "extra_datasets_count": 0,
            "extra_relationships_count": 0,
            "missing_values_count": 0
        }
        self._compare_name()
        self._compare_datasets()
        return self.differences, self.metrics

    def _to_dict(self, val: Any) -> Any:
        if isinstance(val, BaseModel):
            return val.dict()
        elif isinstance(val, list):
            return [self._to_dict(item) for item in val]
        else:
            return val

    def _compare_name(self):
        if self.correct.name != self.incorrect.name:
            self.differences.append(
                f"Name mismatch: Correct name={self._to_dict(self.correct.name)}, Incorrect name={self._to_dict(self.incorrect.name)}"
            )
            self.metrics["missing_values_count"] += 1

    def _compare_datasets(self):
        correct_datasets = {ds.name.name: ds for ds in self.correct.dataSets}
        incorrect_datasets = {ds.name.name: ds for ds in self.incorrect.dataSets}

        # Check for missing or extra datasets
        for ds_name in correct_datasets:
            if ds_name not in incorrect_datasets:
                self.differences.append(f"Dataset '{ds_name}' missing in incorrect JSON")
                self.metrics["missing_values_count"] += 1
        for ds_name in incorrect_datasets:
            if ds_name not in correct_datasets:
                self.differences.append(f"Extra dataset '{ds_name}' in incorrect JSON")
                self.metrics["extra_datasets_count"] += 1

        # Compare common datasets
        for ds_name in set(correct_datasets.keys()) & set(incorrect_datasets.keys()):
            self._compare_dataset(correct_datasets[ds_name], incorrect_datasets[ds_name], ds_name)

    def _compare_dataset(self, correct_ds: DataSet, incorrect_ds: DataSet, ds_name: str):
        # Compare dataset name and type
        if correct_ds.name != incorrect_ds.name:
            self.differences.append(
                f"Dataset '{ds_name}' name mismatch: Correct_value={self._to_dict(correct_ds.name)}, Current_value={self._to_dict(incorrect_ds.name)}"
            )
            self.metrics["missing_values_count"] += 1
        if correct_ds.type != incorrect_ds.type:
            self.differences.append(
                f"Dataset '{ds_name}' type mismatch: Correct_value={correct_ds.type}, Current_value={incorrect_ds.type}"
            )
            self.metrics["missing_values_count"] += 1

        # Compare properties
        self._compare_properties(correct_ds.properties, incorrect_ds.properties, ds_name)

        # Compare relationships
        self._compare_relationships(correct_ds.dataSetRelationShips, incorrect_ds.dataSetRelationShips, ds_name)

    def _compare_properties(self, correct_props: List[Property], incorrect_props: List[Property], ds_name: str):
        correct_props_dict = {prop.name.name: prop for prop in correct_props}
        incorrect_props_dict = {prop.name.name: prop for prop in incorrect_props}

        # Check for missing or extra properties
        for prop_name in correct_props_dict:
            if prop_name not in incorrect_props_dict:
                self.differences.append(f"Property '{prop_name}' missing in dataset '{ds_name}' of newly generated metadata JSON")
                self.metrics["missing_values_count"] += 1
        for prop_name in incorrect_props_dict:
            if prop_name not in correct_props_dict:
                self.differences.append(f"Extra property '{prop_name}' in dataset '{ds_name}' of newly generated metadata JSON")
                self.metrics["extra_properties_count"] += 1

        # Compare common properties
        for prop_name in set(correct_props_dict.keys()) & set(incorrect_props_dict.keys()):
            self._compare_property(correct_props_dict[prop_name], incorrect_props_dict[prop_name], ds_name, prop_name)

    def _compare_property(self, correct_prop: Property, incorrect_prop: Property, ds_name: str, prop_name: str):
        for field in ['type', 'nullable', 'primaryKey', 'uniqueKey', 'compositeKey']:
            correct_val = getattr(correct_prop, field)
            incorrect_val = getattr(incorrect_prop, field)
            if correct_val != incorrect_val:
                self.differences.append(
                    f"Property '{prop_name}' in dataset '{ds_name}', {field} mismatch: Correct_value={correct_val}, current_value={incorrect_val}"
                )
                self.metrics["missing_values_count"] += 1
        if correct_prop.compositeKeyColumns != incorrect_prop.compositeKeyColumns:
            self.differences.append(
                f"Property '{prop_name}' in dataset '{ds_name}', compositeKeyColumns mismatch: Correct_value={correct_prop.compositeKeyColumns}, current_value={incorrect_prop.compositeKeyColumns}"
            )
            self.metrics["missing_values_count"] += 1

    def _compare_relationships(self, correct_rels: List[Relationship], incorrect_rels: List[Relationship], ds_name: str):
        correct_rels_dict = {rel.relationshipName.name: rel for rel in correct_rels}
        incorrect_rels_dict = {rel.relationshipName.name: rel for rel in incorrect_rels}

        # Check for missing or extra relationships
        for rel_name in correct_rels_dict:
            if rel_name not in incorrect_rels_dict:
                self.differences.append(f"Relationship '{rel_name}' missing in dataset '{ds_name}' of newly generated metadata JSON")
                self.metrics["missing_values_count"] += 1
        for rel_name in incorrect_rels_dict:
            if rel_name not in correct_rels_dict:
                self.differences.append(f"Extra relationship '{rel_name}' in dataset '{ds_name}' of newly generated metadata JSON")
                self.metrics["extra_relationships_count"] += 1

        # Compare common relationships
        for rel_name in set(correct_rels_dict.keys()) & set(incorrect_rels_dict.keys()):
            self._compare_relationship(correct_rels_dict[rel_name], incorrect_rels_dict[rel_name], ds_name, rel_name)

    def _compare_relationship(self, correct_rel: Relationship, incorrect_rel: Relationship, ds_name: str, rel_name: str):
        for field in ['relationshipName', 'sourceDataset', 'targetDataset', 'sourceFields', 'targetFields']:
            correct_val = getattr(correct_rel, field)
            incorrect_val = getattr(incorrect_rel, field)
            if correct_val != incorrect_val:
                correct_repr = self._to_dict(correct_val)
                incorrect_repr = self._to_dict(incorrect_val)
                self.differences.append(
                    f"Relationship '{rel_name}' in dataset '{ds_name}' {field} mismatch: Correct_value={correct_repr}, current_value={incorrect_repr}"
                )
                self.metrics["missing_values_count"] += 1