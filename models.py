from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class CuentaPUC(Base):
    __tablename__ = "cuentas_puc"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # Activo, Pasivo, Patrimonio, Ingreso, Gasto, Costo


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Float, nullable=False)
    costo = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    ventas = relationship("Venta", back_populates="producto")


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)
    iva = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    cliente_nombre = Column(String, nullable=True)

    producto = relationship("Producto", back_populates="ventas")