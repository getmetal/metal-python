from enum import Enum
from typing import TypedDict, Optional


class TuneLabel(Enum):
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1

class IndexPayload(TypedDict):
    imageBase64: Optional[str]
    imageUrl: Optional[str]
    text: Optional[str]
    embedding: Optional[list[float]]
    
class SearchPayload(TypedDict):
    imageBase64: Optional[str]
    imageUrl: Optional[str]
    text: Optional[str]
    embedding: Optional[list[float]]

class TunePayload(TypedDict):
    idA: Optional[str]
    idB: Optional[str]
    label: TuneLabel
