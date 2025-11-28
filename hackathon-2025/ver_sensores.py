#!/usr/bin/env python3
"""Script para ver estados de sensores en Firebase"""

from routers.api import db

ref = db.reference('sensores')
sensores = ref.get()

if sensores:
    print("\n=== ESTADOS DE SENSORES ===\n")
    for sensor_id, datos in sensores.items():
        estado = datos.get('estado_contenedor', 'N/A')
        print(f"{sensor_id}: {estado}")
else:
    print("No hay sensores en Firebase")
