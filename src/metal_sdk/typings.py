from enum import Enum
from typing import TypedDict, Optional, List


class TuneLabel(Enum):
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1


class IndexPayload(TypedDict):
    id: Optional[str] = None
    imageBase64: Optional[str] = None
    imageUrl: Optional[str] = None
    text: Optional[str] = None
    embedding: Optional[List[float]] = None


class SearchPayload(TypedDict):
    imageBase64: Optional[str] = None
    imageUrl: Optional[str] = None
    text: Optional[str] = None
    embedding: Optional[List[float]] = None


class TunePayload(TypedDict):
    idA: Optional[str]
    idB: Optional[str]
    label: TuneLabel
