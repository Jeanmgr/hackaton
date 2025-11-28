from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import firebase_admin
from firebase_admin import credentials, db
import os

# Inicializar Firebase (solo una vez)
if not firebase_admin._apps:
    # Ruta al archivo de credenciales
    cred_path = os.path.join(os.path.dirname(__file__), "ecoloop-61400-firebase-adminsdk-fbsvc-e2a6a2401d.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://ecoloop-61400-default-rtdb.firebaseio.com/"
    })

router = APIRouter()

# MODELOS --------------------------------------------------

class Sensor(BaseModel):
    distancia_cm: float
    estado_contenedor: str
    luminosidad: float
    toxicidad: str
    respuestas_ia: Optional[str] = ""

class Usuario(BaseModel):
    Nombre: str
    Apellidos: str
    Correo: str
    Contraseña: str
    Rol: str  # Solo 'Admin' o 'Intendencia'

class Residuo(BaseModel):
    tipo: str
    peso: Optional[float] = 0.0
    fecha: Optional[str] = ""
    ubicacion: Optional[str] = ""
    estado: Optional[str] = "Activo"

# ENDPOINTS SENSORES ---------------------------------------

@router.get("/sensores/")
def obtener_sensores():
    ref = db.reference("sensores")
    data = ref.get()
    return data if data else {}


@router.get("/sensores/{sensor_id}")
def obtener_sensor(sensor_id: str):
    ref = db.reference(f"sensores/{sensor_id}")
    data = ref.get()

    if not data:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")

    return data

@router.post("/sensores/{sensor_id}")
def crear_actualizar_sensor(sensor_id: str, sensor: Sensor):
    ref = db.reference(f"sensores/{sensor_id}")
    ref.set(sensor.dict())
    return {"mensaje": "Sensor agregado/actualizado", "id": sensor_id}

@router.put("/sensores/{sensor_id}")
def actualizar_sensor(sensor_id: str, sensor: Sensor):
    ref = db.reference(f"sensores/{sensor_id}")
    if not ref.get():
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    ref.update(sensor.dict())
    return {"mensaje": "Sensor actualizado correctamente"}

@router.delete("/sensores/{sensor_id}")
def eliminar_sensor(sensor_id: str):
    ref = db.reference(f"sensores/{sensor_id}")
    if not ref.get():
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    ref.delete()
    return {"mensaje": "Sensor eliminado correctamente"}

# ENDPOINTS RESIDUOS ---------------------------------------

@router.get("/residuos/")
def obtener_todos_residuos():
    ref = db.reference("Residuos")
    data = ref.get()
    return data if data else {}

# Obtener un residuo específico
@router.get("/residuos/{id}")
def obtener_residuo(id: str):
    ref = db.reference(f"Residuos/{id}")
    data = ref.get()
    if not data:
        return {"error": "Residuo no encontrado"}
    return {"id": id, **data}



# Crear o actualizar un residuo
@router.post("/residuos/{id}")
def crear_actualizar_residuo(id: str, residuo: Residuo):
    ref = db.reference(f"Residuos/{id}")
    ref.set(residuo.dict())
    return {"mensaje": "Residuo agregado/actualizado", "id": id}

@router.put("/residuos/{id}")
def actualizar_residuo(id: str, residuo: Residuo):
    ref = db.reference(f"Residuos/{id}")
    if not ref.get():
        raise HTTPException(status_code=404, detail="Residuo no encontrado")
    ref.update(residuo.dict())
    return {"mensaje": "Residuo actualizado correctamente"}


# Eliminar residuo
@router.delete("/residuos/{id}")
def eliminar_residuo(id: str):
    ref = db.reference(f"Residuos/{id}")
    ref.delete()
    return {"mensaje": "Residuo eliminado"}


# ENDPOINTS USUARIOS ---------------------------------------

@router.get("/usuarios/")
def obtener_usuarios():
    ref = db.reference("usuarios")
    data = ref.get()
    return data if data else {}


@router.get("/usuarios/{user_id}")
def obtener_usuario(user_id: str):
    ref = db.reference(f"usuarios/{user_id}")
    data = ref.get()
    if not data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return data


@router.post("/usuarios/{user_id}")
def crear_usuario(user_id: str, usuario: Usuario):
    rol_norm = (usuario.Rol or '').lower()
    if rol_norm not in ('admin', 'intendencia', 'usuario'):
        raise HTTPException(status_code=400, detail="Rol inválido. Solo 'Admin', 'Intendencia' o 'Usuario'.")
    # Normalizar a título
    if rol_norm == 'admin':
        usuario.Rol = 'Admin'
    elif rol_norm == 'intendencia':
        usuario.Rol = 'Intendencia'
    else:
        usuario.Rol = 'Usuario'
    ref = db.reference(f"usuarios/{user_id}")
    ref.set(usuario.dict())
    return {"mensaje": "Usuario creado correctamente"}


@router.put("/usuarios/{user_id}")
def actualizar_usuario(user_id: str, usuario: Usuario):
    ref = db.reference(f"usuarios/{user_id}")
    if not ref.get():
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    rol_norm = (usuario.Rol or '').lower()
    if rol_norm not in ('admin', 'intendencia', 'usuario'):
        raise HTTPException(status_code=400, detail="Rol inválido. Solo 'Admin', 'Intendencia' o 'Usuario'.")
    if rol_norm == 'admin':
        usuario.Rol = 'Admin'
    elif rol_norm == 'intendencia':
        usuario.Rol = 'Intendencia'
    else:
        usuario.Rol = 'Usuario'
    ref.update(usuario.dict())
    return {"mensaje": "Usuario actualizado correctamente"}


@router.delete("/usuarios/{user_id}")
def eliminar_usuario(user_id: str):
    ref = db.reference(f"usuarios/{user_id}")
    if not ref.get():
        
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    ref.delete()
    return {"mensaje": "Usuario eliminado correctamente"}

# ENDPOINTS REPORTES SEMANALES ---------------------------------------

class ReporteSemanal(BaseModel):
    semana: str  # Formato: "2025-W48" (año-semana)
    fecha_inicio: str
    fecha_fin: str
    total_sensores: int
    total_recolecciones: int
    peso_total_kg: float
    contenedores_llenos: int
    alertas_toxicidad: int
    zonas_activas: list
    resumen: str

@router.get("/reportes/")
def obtener_reportes():
    """Obtener todos los reportes semanales"""
    ref = db.reference("reportes_semanales")
    data = ref.get()
    return data if data else {}

@router.get("/reportes/{semana}")
def obtener_reporte_semana(semana: str):
    """Obtener reporte de una semana específica (ej: 2025-W48)"""
    ref = db.reference(f"reportes_semanales/{semana}")
    data = ref.get()
    if not data:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return data

@router.post("/reportes/{semana}")
def crear_reporte_semanal(semana: str, reporte: ReporteSemanal):
    """Crear o actualizar reporte semanal"""
    ref = db.reference(f"reportes_semanales/{semana}")
    ref.set(reporte.dict())
    return {"mensaje": "Reporte semanal guardado", "semana": semana}

@router.get("/reportes/generar/actual")
def generar_reporte_actual():
    """Generar reporte de la semana actual basado en datos de sensores"""
    from datetime import datetime, timedelta
    
    # Obtener datos actuales de sensores
    sensores_ref = db.reference("sensores")
    sensores = sensores_ref.get()
    
    if not sensores:
        return {"error": "No hay datos de sensores"}
    
    # Calcular estadísticas
    total_sensores = len(sensores) if isinstance(sensores, dict) else 0
    contenedores_llenos = 0
    alertas_toxicidad = 0
    
    for sensor_id, sensor_data in (sensores.items() if isinstance(sensores, dict) else []):
        if sensor_data.get('estado_contenedor') == 'LLENO':
            contenedores_llenos += 1
        if sensor_data.get('toxicidad', '').lower() in ['alto', 'crítico']:
            alertas_toxicidad += 1
    
    # Generar semana actual
    now = datetime.now()
    semana = now.strftime("%Y-W%U")
    fecha_inicio = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
    fecha_fin = (now + timedelta(days=6-now.weekday())).strftime("%Y-%m-%d")
    
    reporte = {
        "semana": semana,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "total_sensores": total_sensores,
        "total_recolecciones": 0,  # Se actualizará con datos reales
        "peso_total_kg": 0.0,
        "contenedores_llenos": contenedores_llenos,
        "alertas_toxicidad": alertas_toxicidad,
        "zonas_activas": [],
        "resumen": f"Reporte generado automáticamente. {contenedores_llenos} contenedores llenos, {alertas_toxicidad} alertas de toxicidad."
    }
    
    # Guardar en Firebase
    ref = db.reference(f"reportes_semanales/{semana}")
    ref.set(reporte)
    
    return reporte

# ENDPOINTS HISTORIAL ---------------------------------------

class RegistroHistorial(BaseModel):
    fecha: str
    hora: str
    sensor_id: str
    zona: str
    tipo_residuo: str
    peso_kg: float
    estado: str
    nivel_llenado: float
    toxicidad: str

@router.get("/historial/")
def obtener_historial():
    """Obtener todo el historial de recolecciones"""
    ref = db.reference("historial_recolecciones")
    data = ref.get()
    return data if data else {}

@router.post("/historial/")
def agregar_registro_historial(registro: RegistroHistorial):
    """Agregar nuevo registro al historial"""
    from datetime import datetime
    ref = db.reference("historial_recolecciones")
    
    # Generar ID único basado en timestamp
    nuevo_id = f"REC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    ref.child(nuevo_id).set(registro.dict())
    return {"mensaje": "Registro agregado al historial", "id": nuevo_id}

@router.get("/historial/{registro_id}")
def obtener_registro(registro_id: str):
    """Obtener un registro específico del historial"""
    ref = db.reference(f"historial_recolecciones/{registro_id}")
    data = ref.get()
    if not data:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return data

# ROOT ------------------------------------------------------

@router.get("/")
def root():
    return {"mensaje": "API FastAPI conectada a Firebase correctamente"}
