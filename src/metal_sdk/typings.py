from __future__ import annotations
from enum import Enum
from typing import List
from typing_extensions import TypedDict, NotRequired


class TuneLabel(Enum):
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1


class IndexStatus(Enum):
    DEACTIVATING = "DEACTIVATING"
    UNARCHIVED = "UNARCHIVED"


class IndexPayload(TypedDict):
    id: NotRequired[str]
    imageBase64: NotRequired[str]
    imageUrl: NotRequired[str]
    text: NotRequired[str]
    embedding: NotRequired[List[float]]
    metadata: NotRequired[dict]


class BulkIndexItem(TypedDict):
    id: NotRequired[str]
    index: str
    imageBase64: NotRequired[str]
    imageUrl: NotRequired[str]
    text: NotRequired[str]
    embedding: NotRequired[List[float]]
    metadata: NotRequired[dict]


class BulkIndexPayload(TypedDict):
    data: List[BulkIndexItem]


class SearchClause(TypedDict):
    field: str
    value: str | int | float
    operator: str


SearchFilter = TypedDict('SearchFilter', {'and': List[SearchClause], 'or': List[SearchClause]})


class SearchPayload(TypedDict):
    imageBase64: NotRequired[str]
    imageUrl: NotRequired[str]
    text: NotRequired[str]
    embedding: NotRequired[List[float]]
    filters: NotRequired[SearchFilter]


class TunePayload(TypedDict):
    idA: str
    idB: str
    label: TuneLabel


class MotorheadPayload(TypedDict):
    api_key: NotRequired[str]
    client_id: NotRequired[str]
    base_url: NotRequired[str]


class MetadataField(TypedDict):
    name: NotRequired[str]
    type: NotRequired[str]
    description: NotRequired[str]


class DataSourcePayload(TypedDict):
    name: NotRequired[str]
    metadataFields: NotRequired[List[MetadataField]]
    sourcetype: NotRequired[str]
    autoExtract: NotRequired[bool]


class FiltersField(TypedDict):
    field: NotRequired[str]
    type: NotRequired[str]


class CreateIndexPayload(TypedDict):
    model: NotRequired[str]
    datasource: NotRequired[str]
    name: NotRequired[str]
    filters: NotRequired[List[FiltersField]]


class UpdateIndexPayload(TypedDict):
    status: IndexStatus
