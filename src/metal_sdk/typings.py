from __future__ import annotations
from enum import Enum
from typing import List
from typing_extensions import TypedDict, NotRequired


class TuneLabel(Enum):
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1


class IndexPayload(TypedDict):
    id: NotRequired[str]
    imageBase64: NotRequired[str]
    imageUrl: NotRequired[str]
    text: NotRequired[str]
    embedding: NotRequired[List[float]]
    metadata: NotRequired[dict]


class SearchFilter(TypedDict):
    field: str
    value: str | int | float


class SearchPayload(TypedDict):
    imageBase64: NotRequired[str]
    imageUrl: NotRequired[str]
    text: NotRequired[str]
    embedding: NotRequired[List[float]]
    filters: NotRequired[List[SearchFilter]]


class TunePayload(TypedDict):
    idA: str
    idB: str
    label: TuneLabel
