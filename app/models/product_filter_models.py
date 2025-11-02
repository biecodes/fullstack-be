from pydantic import BaseModel
from typing import Optional, List


class ProductFilterModel(BaseModel):
    page: int = 1
    limit: int = 10
    search: Optional[str] = None
    searchBy: Optional[List[str]] = None
    order: str = "asc"
    orderBy: str = "created_at"
    operator: Optional[str] = "or"
