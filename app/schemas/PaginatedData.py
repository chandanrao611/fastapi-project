from typing import List, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedData(BaseModel, Generic[T]):
    items: List[T]
    page: int
    size: int
    total: int