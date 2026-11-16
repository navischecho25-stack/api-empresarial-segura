from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, SessionLocal
import models
import schemas

# Crear las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Empresarial Segura", version="1.0")


# --- INICIALIZACIÓN AUTOMÁTICA DEL PUC ---
def inicializar_cuentas_puc():
    db = SessionLocal()
    cuentas_obligatorias = [
        {"codigo": "1105", "nombre": "Caja general", "tipo": "Activo"},
        {"codigo": "1435", "nombre": "Mercancías no fabricadas", "tipo": "Activo"},
        {"codigo": "2408", "nombre": "IVA generado", "tipo": "Pasivo"},
        {"codigo": "4135", "nombre": "Comercio al por mayor y menor", "tipo": "Ingreso"},
        {"codigo": "6135", "nombre": "Costo de ventas", "tipo": "Costo"}
    ]
    
    for c in cuentas_obligatorias:
        existe = db.query(models.CuentaPUC).filter(models.CuentaPUC.codigo == c["codigo"]).first()
        if not existe:
            nueva_cuenta = models.CuentaPUC(
                codigo=c["codigo"],
                nombre=c["nombre"],
                tipo=c["tipo"]
            )
            db.add(nueva_cuenta)
    db.commit()
    db.close()

# Ejecutar la carga automática al arrancar la aplicación
inicializar_cuentas_puc()


# --- RUTAS DE LA API ---

@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido a la API Empresarial Segura con Contabilidad Automática"}


@app.post("/puc/", response_model=schemas.CuentaPUCResponse)
def crear_cuenta_puc(cuenta: schemas.CuentaPUCCreate, db: Session = Depends(get_db)):
    db_cuenta = db.query(models.CuentaPUC).filter(models.CuentaPUC.codigo == cuenta.codigo).first()
    if db_cuenta:
        raise HTTPException(status_code=400, detail="La cuenta PUC ya existe")
    nueva_cuenta = models.CuentaPUC(**cuenta.dict())
    db.add(nueva_cuenta)
    db.commit()
    db.refresh(nueva_cuenta)
    return nueva_cuenta


@app.post("/productos/", response_model=schemas.ProductoResponse)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    nuevo_producto = models.Producto(**producto.dict())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto


@app.get("/productos/", response_model=List[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    """Consulta el inventario actual con el stock actualizado de cada producto."""
    productos = db.query(models.Producto).all()
    return productos


@app.post("/ventas/")
def realizar_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    # 1. Validar cuentas obligatorias del PUC
    cuentas_requeridas = ["1105", "1435", "2408", "4135", "6135"]
    for codigo in cuentas_requeridas:
        cuenta = db.query(models.CuentaPUC).filter(models.CuentaPUC.codigo == codigo).first()
        if not cuenta:
            raise HTTPException(
                status_code=400, 
                detail=f"Falta configurar en el PUC la cuenta obligatoria '{codigo}'."
            )

    # 2. Buscar el producto
    producto = db.query(models.Producto).filter(models.Producto.id == venta.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # 3. Validar stock
    if producto.stock < venta.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente para realizar la venta")

    # 4. Calcular totales e IVA (19%)
    subtotal = producto.precio * venta.cantidad
    iva = subtotal * 0.19
    total = subtotal + iva
    costo_total = producto.costo * venta.cantidad

    # 5. Descontar stock
    producto.stock -= venta.cantidad

    # 6. Registrar la venta
    nueva_venta = models.Venta(
        producto_id=producto.id,
        cantidad=venta.cantidad,
        subtotal=subtotal,
        iva=iva,
        total=total,
        cliente_nombre=venta.cliente_nombre
    )
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)

    return {
        "mensaje": "Venta realizada y contabilizada con éxito",
        "venta_id": nueva_venta.id,
        "subtotal": subtotal,
        "iva": iva,
        "total": total,
        "costo_registrado": costo_total
    }