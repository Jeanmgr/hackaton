# 🔥 Conexión Firebase - EcoLoop

## ✅ Cambios Realizados

### 1. Backend (Python/FastAPI)

#### `app.py` - Corregido
- ✅ Cambio de `from routers.api import api` → `from routers.api import router as api_router`
- ✅ Agregado prefijo `/api` a todos los endpoints de la API
- ✅ Inicialización correcta de FastAPI

#### `routers/api.py` - Completamente Refactorizado
- ✅ Cambio de `app = FastAPI()` → `router = APIRouter()`
- ✅ Ruta de credenciales corregida usando `os.path.join()`
- ✅ Protección contra múltiples inicializaciones de Firebase con `if not firebase_admin._apps:`
- ✅ Todos los decoradores cambiados de `@app` a `@router`

#### Nuevos Endpoints Agregados:
```python
# SENSORES
GET    /api/sensores/           # Listar todos
GET    /api/sensores/{id}       # Obtener uno
POST   /api/sensores/{id}       # Crear/Actualizar
PUT    /api/sensores/{id}       # Actualizar
DELETE /api/sensores/{id}       # Eliminar

# USUARIOS
GET    /api/usuarios/           # Listar todos
GET    /api/usuarios/{id}       # Obtener uno
POST   /api/usuarios/{id}       # Crear
PUT    /api/usuarios/{id}       # Actualizar
DELETE /api/usuarios/{id}       # Eliminar

# RESIDUOS
GET    /api/residuos/           # Listar todos ⭐ NUEVO
GET    /api/residuos/{id}       # Obtener uno
POST   /api/residuos/{id}       # Crear
PUT    /api/residuos/{id}       # Actualizar ⭐ NUEVO
DELETE /api/residuos/{id}       # Eliminar
```

#### Modelos Pydantic Agregados:
```python
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
    Rol: str

class Residuo(BaseModel):  # ⭐ NUEVO
    tipo: str
    peso: Optional[float] = 0.0
    fecha: Optional[str] = ""
    ubicacion: Optional[str] = ""
    estado: Optional[str] = "Activo"
```

### 2. Frontend (JavaScript)

#### `static/js/usuarios.js` - Completamente Reescrito
- ✅ Conectado a Firebase API
- ✅ Función `loadUsers()` para cargar usuarios desde `/api/usuarios/`
- ✅ Función `saveModal` con `fetch()` para POST/PUT
- ✅ Función `confirmDelete` con `fetch()` para DELETE
- ✅ Función `openEdit()` precarga datos del usuario en el formulario
- ✅ Validación de campos requeridos
- ✅ Manejo de errores con try/catch

#### `static/js/map-monitoreo.js` - Mejorado
- ✅ Función `cargarSensores()` conectada a `/api/sensores/`
- ✅ Popups dinámicos con datos reales del sensor:
  - Estado del contenedor
  - Distancia en cm
  - Luminosidad
  - Toxicidad
- ✅ Fallback a coordenadas predefinidas si no hay sensores
- ✅ Función `mostrarMarcadoresPorDefecto()` como respaldo

#### `templates/usuarios.html` - Actualizado
- ✅ Campo de contraseña agregado al modal

### 3. Archivos de Utilidad

#### `test_firebase.py` - Script de Prueba
Script Python para verificar la conexión con Firebase:
- ✅ Verifica credenciales
- ✅ Lee sensores, usuarios y residuos
- ✅ Crea datos de prueba si no existen
- ✅ Muestra resumen de datos

## 🚀 Cómo Usar

### 1. Verificar Conexión Firebase

```bash
# Probar conexión
python test_firebase.py
```

Deberías ver:
```
🔥 Probando conexión con Firebase...
✓ Archivo de credenciales encontrado
✓ Firebase inicializado correctamente
✅ ¡Conexión con Firebase exitosa!
```

### 2. Iniciar el Servidor

```bash
# Asegúrate de tener las dependencias instaladas
pip install -r requirements.txt

# Iniciar servidor con uvicorn
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 3. Probar Endpoints

#### Desde el navegador:
- **Documentación API**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8000/dashboard
- **Usuarios**: http://localhost:8000/usuarios
- **Monitoreo**: http://localhost:8000/monitoreo

#### Desde curl/Postman:

```bash
# Listar sensores
curl http://localhost:8000/api/sensores/

# Crear sensor
curl -X POST http://localhost:8000/api/sensores/sensor_001 \
  -H "Content-Type: application/json" \
  -d '{
    "distancia_cm": 30.5,
    "estado_contenedor": "Medio lleno",
    "luminosidad": 500.0,
    "toxicidad": "Normal",
    "respuestas_ia": "Estado normal"
  }'

# Listar usuarios
curl http://localhost:8000/api/usuarios/

# Crear usuario
curl -X POST http://localhost:8000/api/usuarios/user_001 \
  -H "Content-Type: application/json" \
  -d '{
    "Nombre": "Ana",
    "Apellidos": "García",
    "Correo": "ana@example.com",
    "Contraseña": "pass123",
    "Rol": "User"
  }'
```

## 📊 Estructura de Datos en Firebase

```
firebase-realtime-database/
├── sensores/
│   ├── sensor_001/
│   │   ├── distancia_cm: 30.5
│   │   ├── estado_contenedor: "Medio lleno"
│   │   ├── luminosidad: 500.0
│   │   ├── toxicidad: "Normal"
│   │   └── respuestas_ia: "Estado normal"
│   └── sensor_002/
│       └── ...
├── usuarios/
│   ├── user_001/
│   │   ├── Nombre: "Jonathan"
│   │   ├── Apellidos: "Cruz"
│   │   ├── Correo: "admin@ecoloop.com"
│   │   ├── Contraseña: "admin123"
│   │   └── Rol: "Admin"
│   └── user_002/
│       └── ...
└── Residuos/
    ├── residuo_001/
    │   ├── tipo: "Plástico"
    │   ├── peso: 2.5
    │   ├── fecha: "2025-11-28"
    │   ├── ubicacion: "Campus UTTT"
    │   └── estado: "Activo"
    └── residuo_002/
        └── ...
```

## 🔧 Solución de Problemas

### Error: "Module 'firebase_admin' has no attribute '_apps'"
**Solución**: Actualiza firebase-admin
```bash
pip install --upgrade firebase-admin
```

### Error: "No module named 'firebase_admin'"
**Solución**: Instala firebase-admin
```bash
pip install firebase-admin
```

### Error 404 en endpoints
**Problema**: No agregaste el prefijo `/api`
**Solución**: Usa `/api/sensores/` en lugar de `/sensores/`

### No se cargan usuarios/sensores en el frontend
**Solución**: 
1. Abre la consola del navegador (F12)
2. Revisa errores de red
3. Verifica que el servidor esté corriendo
4. Confirma que los datos existen en Firebase

## 📝 Próximos Pasos

- [ ] Agregar autenticación JWT
- [ ] Implementar paginación en endpoints
- [ ] Agregar filtros y búsqueda
- [ ] Crear dashboard con gráficas
- [ ] Implementar WebSockets para updates en tiempo real
- [ ] Agregar validación de datos más robusta
- [ ] Implementar caché con Redis

## 🎯 Estado Actual

✅ **Conexión Firebase**: Funcionando  
✅ **Endpoints API**: Todos operativos  
✅ **Frontend Usuarios**: Conectado y funcional  
✅ **Frontend Monitoreo**: Conectado con marcadores dinámicos  
✅ **Modelos Pydantic**: Implementados y validando  
✅ **CRUD Completo**: Sensores, Usuarios y Residuos  

---

**¡Tu aplicación está lista para enviar y recibir datos de Firebase! 🎉**
