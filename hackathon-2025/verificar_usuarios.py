#!/usr/bin/env python3
"""Script para verificar y limpiar usuarios en Firebase"""

import firebase_admin
from firebase_admin import credentials, db
import os

# Inicializar Firebase
if not firebase_admin._apps:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cred_path = os.path.join(script_dir, "routers", "ecoloop-61400-firebase-adminsdk-fbsvc-e2a6a2401d.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ecoloop-61400-default-rtdb.firebaseio.com/'
    })

# Obtener referencia a usuarios
ref = db.reference('usuarios')
usuarios = ref.get()

print("=" * 60)
print("USUARIOS EN FIREBASE:")
print("=" * 60)

if usuarios:
    if isinstance(usuarios, list):
        print(f"Tipo: Array con {len(usuarios)} elementos\n")
        for idx, usuario in enumerate(usuarios):
            if usuario is None:
                print(f"[{idx}] = NULL")
            else:
                print(f"[{idx}] = {usuario}")
    elif isinstance(usuarios, dict):
        print(f"Tipo: Objeto con {len(usuarios)} claves\n")
        for key, usuario in usuarios.items():
            if usuario is None:
                print(f"'{key}' = NULL")
            else:
                print(f"'{key}' = {usuario}")
else:
    print("No hay usuarios en la base de datos")

print("\n" + "=" * 60)
print("SOLUCIÓN:")
print("=" * 60)

if usuarios and isinstance(usuarios, list):
    print("\n⚠️  Los usuarios están en formato ARRAY (no recomendado)")
    print("✅ Mejor práctica: usar OBJETOS con IDs únicos")
    print("\n¿Quieres convertir a formato objeto? (s/n): ", end="")
    
    # Mostrar cómo se vería la conversión
    print("\n\nASÍ QUEDARÍA LA ESTRUCTURA:")
    print("-" * 60)
    for idx, usuario in enumerate(usuarios):
        if usuario and isinstance(usuario, dict):
            user_id = f"user_{idx}"
            print(f"'{user_id}': {usuario}")
