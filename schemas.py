from pydantic import BaseModel
from typing import Optional, List

# --- ESQUEMAS PARA CUENTAS PUC ---
class CuentaPUCCreate(BaseModel):
    codigo: str
    nombre: str
    tipo: str

class CuentaPUCResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    tipo: str

    class Config:
        from_attributes = True


# --- ESQUEMAS PARA PRODUCTOS ---
class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    costo: float
    stock: int = 0

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    costo: float
    stock: int

    class Config:
        from_attributes = True


# --- ESQUEMAS PARA VENTAS ---
class VentaCreate(BaseModel):
    producto_id: int
    cantidad: int
    cliente_nombre: Optional[str] = None