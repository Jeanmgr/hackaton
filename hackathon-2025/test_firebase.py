#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con Firebase Realtime Database
"""
import firebase_admin
from firebase_admin import credentials, db
import os

def test_firebase_connection():
    print("🔥 Probando conexión con Firebase...\n")
    
    try:
        # Inicializar Firebase
        cred_path = os.path.join("routers", "ecoloop-61400-firebase-adminsdk-fbsvc-e2a6a2401d.json")
        
        if not os.path.exists(cred_path):
            print(f"❌ ERROR: No se encontró el archivo de credenciales en {cred_path}")
            return False
        
        print(f"✓ Archivo de credenciales encontrado: {cred_path}")
        
        # Inicializar app
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                "databaseURL": "https://ecoloop-61400-default-rtdb.firebaseio.com/"
            })
            print("✓ Firebase inicializado correctamente")
        
        # Probar lectura de sensores
        print("\n📡 Probando lectura de sensores...")
        ref_sensores = db.reference("sensores")
        sensores = ref_sensores.get()
        
        if sensores:
            print(f"✓ Se encontraron {len(sensores)} sensores:")
            for sensor_id, data in sensores.items():
                print(f"  - Sensor {sensor_id}: {data.get('estado_contenedor', 'N/A')}")
        else:
            print("⚠️  No hay sensores en la base de datos")
            
            # Crear sensor de prueba
            print("\n📝 Creando sensor de prueba...")
            ref_sensores.child("sensor_test_001").set({
                "distancia_cm": 25.5,
                "estado_contenedor": "Medio lleno",
                "luminosidad": 450.0,
                "toxicidad": "Normal",
                "respuestas_ia": "Contenedor en buen estado"
            })
            print("✓ Sensor de prueba creado")
        
        # Probar lectura de usuarios
        print("\n👥 Probando lectura de usuarios...")
        ref_usuarios = db.reference("usuarios")
        usuarios = ref_usuarios.get()
        
        if usuarios:
            print(f"✓ Se encontraron {len(usuarios)} usuarios")
        else:
            print("⚠️  No hay usuarios en la base de datos")
            
            # Crear usuario de prueba
            print("\n📝 Creando usuario de prueba...")
            ref_usuarios.child("user_admin_001").set({
                "Nombre": "Jonathan",
                "Apellidos": "Cruz",
                "Correo": "admin@ecoloop.com",
                "Contraseña": "admin123",
                "Rol": "Admin"
            })
            print("✓ Usuario de prueba creado")
        
        # Probar lectura de residuos
        print("\n🗑️  Probando lectura de residuos...")
        ref_residuos = db.reference("Residuos")
        residuos = ref_residuos.get()
        
        if residuos:
            print(f"✓ Se encontraron {len(residuos)} residuos")
        else:
            print("⚠️  No hay residuos en la base de datos")
            
            # Crear residuo de prueba
            print("\n📝 Creando residuo de prueba...")
            ref_residuos.child("residuo_001").set({
                "tipo": "Plástico",
                "peso": 2.5,
                "fecha": "2025-11-28",
                "ubicacion": "Campus UTTT",
                "estado": "Activo"
            })
            print("✓ Residuo de prueba creado")
        
        print("\n✅ ¡Conexión con Firebase exitosa!")
        print("\n📊 Resumen:")
        print(f"   Sensores: {len(sensores) if sensores else 0}")
        print(f"   Usuarios: {len(usuarios) if usuarios else 0}")
        print(f"   Residuos: {len(residuos) if residuos else 0}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_firebase_connection()
