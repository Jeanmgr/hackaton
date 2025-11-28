#!/usr/bin/env python3
"""Script para agregar usuarios de prueba"""

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

print("🔥 Conectado a Firebase")
print("=" * 60)

# Obtener usuarios actuales
ref = db.reference('usuarios')
usuarios_actuales = ref.get()

print("\n📋 USUARIOS ACTUALES:")
if usuarios_actuales:
    if isinstance(usuarios_actuales, list):
        for idx, usuario in enumerate(usuarios_actuales):
            if usuario:
                print(f"  [{idx}] {usuario.get('Nombre', 'Sin nombre')} - {usuario.get('Correo', 'Sin correo')} ({usuario.get('Rol', 'Sin rol')})")
    else:
        for user_id, usuario in usuarios_actuales.items():
            if usuario:
                print(f"  [{user_id}] {usuario.get('Nombre', 'Sin nombre')} - {usuario.get('Correo', 'Sin correo')} ({usuario.get('Rol', 'Sin rol')})")

# Agregar usuarios de prueba
print("\n➕ AGREGANDO USUARIOS DE PRUEBA:")

usuarios_prueba = [
    {
        "Nombre": "Admin",
        "Apellidos": "Sistema",
        "Correo": "admin@ecoloop.com",
        "Contraseña": "admin123",
        "Rol": "Admin"
    },
    {
        "Nombre": "María",
        "Apellidos": "García López",
        "Correo": "maria.garcia@uttt.edu.mx",
        "Contraseña": "alumno123",
        "Rol": "Alumno"
    },
    {
        "Nombre": "Carlos",
        "Apellidos": "Ramírez Pérez",
        "Correo": "carlos.ramirez@uttt.edu.mx",
        "Contraseña": "docente123",
        "Rol": "Docente"
    }
]

if isinstance(usuarios_actuales, list):
    # Si es array, agregar al final
    inicio_idx = len(usuarios_actuales)
    for idx, usuario in enumerate(usuarios_prueba):
        new_idx = inicio_idx + idx
        ref.child(str(new_idx)).set(usuario)
        print(f"  ✅ [{new_idx}] {usuario['Nombre']} {usuario['Apellidos']} ({usuario['Rol']})")
else:
    # Si es objeto, usar IDs únicos
    for idx, usuario in enumerate(usuarios_prueba):
        user_id = f"user_{idx + 2}"
        ref.child(user_id).set(usuario)
        print(f"  ✅ [{user_id}] {usuario['Nombre']} {usuario['Apellidos']} ({usuario['Rol']})")

print("\n" + "=" * 60)
print("✅ Usuarios de prueba agregados correctamente")
print("\n📝 CREDENCIALES PARA PROBAR:")
print("-" * 60)
for usuario in usuarios_prueba:
    print(f"  📧 {usuario['Correo']}")
    print(f"  🔑 {usuario['Contraseña']}")
    print(f"  👤 Rol: {usuario['Rol']}")
    print()
print("=" * 60)
