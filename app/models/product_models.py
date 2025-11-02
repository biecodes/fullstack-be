from pydantic import BaseModel
from typing import Optional, List


class ProductModel(BaseModel):
    image: Optional[List[str]] = None
    nama: str
    kategori: str
    stokAwal: int
    discount: float
    rating: float
    terjual: float
    stokPengurangan: int
    stokPenambahan: int
    stokMenipis: int
    units: str
    harga: float
    status: str
    deskripsi: Optional[str] = None
