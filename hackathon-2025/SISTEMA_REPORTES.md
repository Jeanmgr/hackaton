# 📊 Sistema de Reportes Semanales - EcoLoop

## ✅ Cambios Implementados

### 1. **Login Redirect Actualizado**
- ✅ Al iniciar sesión, ahora redirige a `/resumen` en lugar de `/dashboard`
- ✅ Si ya hay sesión activa, redirige automáticamente a `/resumen`

### 2. **Nuevos Endpoints API en `/api/`**

#### Reportes Semanales:
- `GET /api/reportes/` - Obtener todos los reportes semanales
- `GET /api/reportes/{semana}` - Obtener reporte específico (ej: 2025-W47)
- `POST /api/reportes/{semana}` - Crear/actualizar reporte semanal
- `GET /api/reportes/generar/actual` - Generar reporte automático de la semana actual

#### Historial de Recolecciones:
- `GET /api/historial/` - Obtener todo el historial
- `POST /api/historial/` - Agregar nuevo registro al historial
- `GET /api/historial/{registro_id}` - Obtener registro específico

### 3. **Vista de Resumen (`/resumen`)**

#### Características:
- ✅ Muestra estadísticas en tiempo real:
  - Total de contenedores activos
  - Contenedores llenos (alerta)
  - Alertas de toxicidad
  - Usuarios registrados
  
- ✅ Lista de sensores con su estado actual:
  - Estado del contenedor (LLENO/MEDIO/VACIO)
  - Nivel de toxicidad
  - Distancia y luminosidad
  
- ✅ Reporte de la semana actual:
  - Número de semana (ej: 2025-W47)
  - Período (fecha inicio - fecha fin)
  - Resumen ejecutivo
  
- ✅ Botones de acción:
  - "Generar Reporte Semanal" - Guarda snapshot de la semana en Firebase
  - "Ver Historial Completo" - Navega a la página de historial
  - "Descargar PDF" - (En desarrollo)

- ✅ Actualización automática cada 30 segundos

### 4. **Vista de Historial (`/historial`)**

#### Características:
- ✅ Tabla de reportes semanales con:
  - Semana y período
  - Total de sensores
  - Contenedores llenos
  - Alertas de toxicidad
  - Total de recolecciones
  - Peso total recolectado (kg)
  
- ✅ Tabla de registros detallados con:
  - ID de recolección
  - Fecha y hora
  - Sensor y zona
  - Tipo de residuo
  - Peso (kg)
  - Nivel de llenado
  - Toxicidad
  - Estado
  
- ✅ Botón "Agregar Registro" - Permite agregar manualmente registros al historial
- ✅ Actualización automática cada minuto
- ✅ Badges de colores para estados y alertas

### 5. **Estructura de Datos en Firebase**

#### `reportes_semanales/{semana}/`:
```json
{
  "semana": "2025-W47",
  "fecha_inicio": "2025-11-24",
  "fecha_fin": "2025-11-30",
  "total_sensores": 4,
  "total_recolecciones": 32,
  "peso_total_kg": 148.85,
  "contenedores_llenos": 2,
  "alertas_toxicidad": 1,
  "zonas_activas": ["Cafetería", "Biblioteca"],
  "resumen": "Descripción del reporte..."
}
```

#### `historial_recolecciones/{id}/`:
```json
{
  "fecha": "2025-11-27",
  "hora": "14:30",
  "sensor_id": "sensor_01",
  "zona": "Cafetería Central",
  "tipo_residuo": "PET/Plástico",
  "peso_kg": 22.16,
  "estado": "Completado",
  "nivel_llenado": 85,
  "toxicidad": "Normal"
}
```

## 📝 Modelos Pydantic

### ReporteSemanal:
```python
class ReporteSemanal(BaseModel):
    semana: str
    fecha_inicio: str
    fecha_fin: str
    total_sensores: int
    total_recolecciones: int
    peso_total_kg: float
    contenedores_llenos: int
    alertas_toxicidad: int
    zonas_activas: list
    resumen: str
```

### RegistroHistorial:
```python
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
```

## 🚀 Uso del Sistema

### 1. Iniciar Sesión:
```
Email: example@gmail.com
Contraseña: 1234
```

### 2. Página Principal (Resumen):
- Visualiza estadísticas en tiempo real
- Revisa el estado de todos los sensores
- Genera reportes semanales con un clic

### 3. Generar Reporte Semanal:
1. Ir a `/resumen`
2. Clic en "📊 Generar Reporte Semanal"
3. Confirmar la acción
4. El reporte se guarda automáticamente en Firebase

### 4. Ver Historial:
1. Ir a `/historial`
2. Visualizar todos los reportes semanales guardados
3. Ver registros detallados de recolecciones
4. Agregar registros manualmente si es necesario

## 🔄 Flujo de Trabajo Semanal

1. **Durante la semana**: 
   - El sistema monitorea sensores en tiempo real
   - Los datos se actualizan automáticamente en `/resumen`

2. **Al final de la semana** (ej: Domingo):
   - Ir a `/resumen`
   - Clic en "Generar Reporte Semanal"
   - El sistema toma un snapshot de las estadísticas actuales
   - Guarda el reporte en `reportes_semanales/{semana}`

3. **Consultar histórico**:
   - Ir a `/historial`
   - Ver todos los reportes semanales guardados
   - Comparar tendencias entre semanas

## 📊 Datos de Ejemplo Generados

El script `poblar_datos_ejemplo.py` creó:
- ✅ 15 registros de historial (últimos 7 días)
- ✅ 4 reportes semanales (últimas 4 semanas)
- ✅ 4 sensores activos en diferentes estados

## 🛠️ Scripts Disponibles

### `poblar_datos_ejemplo.py`:
Genera datos de prueba en Firebase para demostración.

```bash
python poblar_datos_ejemplo.py
```

### `verificar_usuarios.py`:
Verifica la estructura de usuarios en Firebase.

```bash
python verificar_usuarios.py
```

### `test_firebase.py`:
Verifica la conexión con Firebase.

```bash
python test_firebase.py
```

## 📱 URLs Principales

- `/` - Login (página de inicio)
- `/resumen` - Dashboard principal con estadísticas
- `/historial` - Historial completo de reportes y recolecciones
- `/monitoreo` - Mapa con sensores en tiempo real
- `/usuarios` - Gestión de usuarios

## 🎨 Características de la UI

- ✅ Badges de colores para estados (éxito, advertencia, peligro)
- ✅ Actualización automática de datos
- ✅ Interfaz responsive
- ✅ Cards informativos con iconos
- ✅ Tablas ordenadas cronológicamente
- ✅ Botones de acción claros

## 🔐 Seguridad

- ✅ Validación de sesión con localStorage
- ✅ Redirección automática a login si no hay sesión
- ✅ Protección de rutas (excepto páginas públicas)
- ✅ Verificación de datos en el backend con Pydantic

---

**¡Sistema completamente funcional! 🎉**

Ahora puedes:
1. Hacer login con las credenciales
2. Ver el resumen en tiempo real
3. Generar reportes semanales
4. Consultar el historial completo
