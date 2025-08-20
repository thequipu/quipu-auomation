from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Node(BaseModel):
    id: str
    node_type: str
    label: str
    identity: str
    uri: Optional[str] = None
    dataSourceID: Optional[int] = None
    data_type: Optional[str] = None
    nullable: Optional[bool] = None
    primary_key: Optional[bool] = None
    unique_key: Optional[bool] = None
    foreign_key: Optional[bool] = None
    composite_key: Optional[bool] = None
    composite_key_columns: Optional[List[str]] = None
    named_entity: Optional[bool] = None
    prefered_label: Optional[bool] = None
    alternate_label: Optional[bool] = None

class Relationship(BaseModel):
    source: str
    target: str
    relationship: str
    node_uri: str
    identity: str
    rel_uri: Optional[str] = None
    prefLabel: Optional[bool] = None
    altLabel: Optional[bool] = None
    primaryKey: Optional[bool] = None
    uniqueKey: Optional[bool] = None
    target_node_uri: Optional[str] = None
    pathIds: Optional[List[Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    target_column: Optional[str] = None
    dashed: Optional[bool] = None

class Schema(BaseModel):
    prefix: str
    nodes: List[Node]
    links: List[Relationship]
