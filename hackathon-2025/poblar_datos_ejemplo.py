#!/usr/bin/env python3
"""Script para poblar datos de ejemplo en Firebase"""

import firebase_admin
from firebase_admin import credentials, db
import os
from datetime import datetime, timedelta
import random

# Inicializar Firebase
if not firebase_admin._apps:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cred_path = os.path.join(script_dir, "routers", "ecoloop-61400-firebase-adminsdk-fbsvc-e2a6a2401d.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ecoloop-61400-default-rtdb.firebaseio.com/'
    })

print("🔥 Conectado a Firebase")
print("=" * 60)

# Datos de ejemplo
zonas = ["Cafetería Central", "Biblioteca", "Edificio A", "Laboratorios", "Campus UTTT"]
tipos_residuo = ["PET/Plástico", "Cartón", "Papel", "Vidrio", "Metal/Aluminio", "Orgánico"]
sensores = ["sensor_01", "sensor_02", "sensor_03", "sensor_04", "sensor_05"]
estados = ["Completado", "Procesando", "Pendiente"]
toxicidades = ["Normal", "Moderado", "Alto"]

# 1. Generar registros de historial (últimos 7 días)
print("\n📋 Generando registros de historial...")
historial_ref = db.reference("historial_recolecciones")

for i in range(15):  # 15 registros de ejemplo
    dias_atras = random.randint(0, 7)
    fecha_registro = datetime.now() - timedelta(days=dias_atras)
    
    registro_id = f"REC-{fecha_registro.strftime('%Y%m%d')}{str(i).zfill(3)}"
    
    registro = {
        "fecha": fecha_registro.strftime("%Y-%m-%d"),
        "hora": f"{random.randint(8, 18):02d}:{random.randint(0, 59):02d}",
        "sensor_id": random.choice(sensores),
        "zona": random.choice(zonas),
        "tipo_residuo": random.choice(tipos_residuo),
        "peso_kg": round(random.uniform(0.5, 50.0), 2),
        "estado": random.choice(estados),
        "nivel_llenado": random.randint(50, 100),
        "toxicidad": random.choice(toxicidades)
    }
    
    historial_ref.child(registro_id).set(registro)
    print(f"  ✅ {registro_id}: {registro['zona']} - {registro['tipo_residuo']} ({registro['peso_kg']} kg)")

# 2. Generar reportes semanales (últimas 4 semanas)
print("\n📊 Generando reportes semanales...")
reportes_ref = db.reference("reportes_semanales")

for semana_num in range(4):
    fecha_base = datetime.now() - timedelta(weeks=semana_num)
    semana_str = fecha_base.strftime("%Y-W%U")
    
    # Calcular inicio y fin de semana
    inicio_semana = fecha_base - timedelta(days=fecha_base.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    
    reporte = {
        "semana": semana_str,
        "fecha_inicio": inicio_semana.strftime("%Y-%m-%d"),
        "fecha_fin": fin_semana.strftime("%Y-%m-%d"),
        "total_sensores": random.randint(3, 8),
        "total_recolecciones": random.randint(15, 45),
        "peso_total_kg": round(random.uniform(100, 500), 2),
        "contenedores_llenos": random.randint(0, 3),
        "alertas_toxicidad": random.randint(0, 2),
        "zonas_activas": random.sample(zonas, k=random.randint(2, 4)),
        "resumen": f"Semana del {inicio_semana.strftime('%d/%m')} al {fin_semana.strftime('%d/%m')}: "
                   f"{random.randint(15, 45)} recolecciones realizadas, "
                   f"{round(random.uniform(100, 500), 2)} kg de material reciclado."
    }
    
    reportes_ref.child(semana_str).set(reporte)
    print(f"  ✅ {semana_str}: {reporte['fecha_inicio']} al {reporte['fecha_fin']} - {reporte['peso_total_kg']} kg")

# 3. Agregar más sensores de ejemplo
print("\n📍 Agregando sensores adicionales...")
sensores_ref = db.reference("sensores")

sensores_ejemplos = [
    {
        "id": "sensor_02",
        "data": {
            "distancia_cm": 85.3,
            "estado_contenedor": "MEDIO",
            "luminosidad": 145.5,
            "toxicidad": "Normal"
        }
    },
    {
        "id": "sensor_03",
        "data": {
            "distancia_cm": 45.8,
            "estado_contenedor": "VACIO",
            "luminosidad": 320.0,
            "toxicidad": "Normal"
        }
    },
    {
        "id": "sensor_04",
        "data": {
            "distancia_cm": 168.2,
            "estado_contenedor": "LLENO",
            "luminosidad": 88.4,
            "toxicidad": "Moderado"
        }
    }
]

for sensor in sensores_ejemplos:
    sensores_ref.child(sensor["id"]).set(sensor["data"])
    print(f"  ✅ {sensor['id']}: {sensor['data']['estado_contenedor']} - {sensor['data']['toxicidad']}")

print("\n" + "=" * 60)
print("✅ Datos de ejemplo generados correctamente")
print("\n📌 Resumen:")
print(f"  - 15 registros de historial")
print(f"  - 4 reportes semanales")
print(f"  - 4 sensores activos")
print("\n🌐 Visita http://localhost:8000 y haz login con:")
print("   Email: example@gmail.com")
print("   Contraseña: 1234")
print("=" * 60)
