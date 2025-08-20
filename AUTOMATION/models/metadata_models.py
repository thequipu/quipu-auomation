from pydantic import BaseModel
from typing import List, Optional

class Name(BaseModel):
    name: str
    dataCatalogName: str

class Property(BaseModel):
    name: Name
    type: str
    nullable: bool
    primaryKey: Optional[bool] = None
    uniqueKey: Optional[bool] = None
    compositeKey: Optional[bool] = None
    compositeKeyColumns: Optional[List[str]] = None

class Relationship(BaseModel):
    relationshipName: Name
    sourceDataset: Name
    targetDataset: Name
    sourceFields: List[Name]
    targetFields: List[Name]

class DataSet(BaseModel):
    name: Name
    type: Optional[str]
    properties: List[Property]
    dataSetRelationShips: List[Relationship]

class Metadata(BaseModel):
    name: Name
    dataSets: List[DataSet]