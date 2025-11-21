import cv2
import time 
import os
import numpy as np
from .file_manager import crear_directorio_alumno, guardar_foto, cargar_dataset_entrenamiento
from .database_manager import registrar_asistencia
from .PCA import ModeloPCA

NUM_FOTOS_POR_ALUMNO = 20
INTERVALO_TOMA = 0.5 
SIZE_FACE = (100, 100) # Tamaño estándar para PCA

# Cargar el detector de rostros pre-entrenado de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detectar_y_procesar_rostro(frame):
    #Detecta rostro, lo recorta, convierte a gris y redimensiona
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) > 0:
        # Tomamos el rostro más grande encontrado
        (x, y, w, h) = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)[0]
        rostro = gray[y:y+h, x:x+w]
        rostro_resized = cv2.resize(rostro, SIZE_FACE)
        return rostro_resized, (x, y, w, h)
    return None, None

def capturar_y_registrar_fotos(codigo_alumno):
    if not codigo_alumno:
        print("El codigo no puede estar vacio.")
        return

    ruta_alumno = crear_directorio_alumno(codigo_alumno)
    cap = cv2.VideoCapture(0)
    
    print(f"Posiciona tu rostro. Buscando cara")
    
    contador = 1
    tiempo_ultima_captura = time.time()

    while contador <= NUM_FOTOS_POR_ALUMNO:
        ret, frame = cap.read()
        if not ret: break
        
        # Copia para dibujar rectangulo sin manchar la foto original
        display_frame = frame.copy()
        
        # Detectar rostro
        rostro_procesado, rect = detectar_y_procesar_rostro(frame)
        
        mensaje = "Buscando rostro..."
        color = (0, 0, 255) # Rojo

        if rostro_procesado is not None:
            (x, y, w, h) = rect
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            tiempo_actual = time.time()
            if tiempo_actual - tiempo_ultima_captura >= INTERVALO_TOMA:
                guardar_foto(ruta_alumno, contador, rostro_procesado)
                print(f"Foto {contador} guardada.")
                contador += 1
                tiempo_ultima_captura = tiempo_actual
            
            mensaje = f"Capturando: {contador-1}/{NUM_FOTOS_POR_ALUMNO}"
            color = (0, 255, 0)

        cv2.putText(display_frame, mensaje, (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        cv2.imshow('Registro Nuevo Alumno', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\nRegistro completado para {codigo_alumno}")

def proceso_tomar_asistencia():
    # 1. Entrenar modelo
    modelo = ModeloPCA()
    imagenes, etiquetas, nombres = cargar_dataset_entrenamiento()
    
    if imagenes is None or len(imagenes) == 0:
        print("No hay datos para entrenar. Registra alumnos primero.")
        return

    exito = modelo.entrenar(imagenes, etiquetas, nombres)
    if not exito: return

    # 2. Iniciar Reconocimiento
    cap = cv2.VideoCapture(0)
    print("\n--- MODO ASISTENCIA ---")
    print("Presiona 'SPACE' para confirmar asistencia cuando te reconozca.")
    print("Presiona 'Q' para salir.")

    ultimo_mensaje = ""
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        rostro_procesado, rect = detectar_y_procesar_rostro(frame)
        
        nombre_detectado = "Desconocido"
        confianza = 0.0
        color_rect = (0, 0, 255) # Rojo por defecto

        if rostro_procesado is not None:
            (x, y, w, h) = rect
            
            # PREDECIR
            nombre_detectado, confianza = modelo.predecir(rostro_procesado)
            
            # Umbral de confianza (Ajustar segun luz: menor es mejor. < 3000 es decente)
            if confianza < 4000:
                color_rect = (0, 255, 0) # Verde
                texto_pantalla = f"{nombre_detectado} ({int(confianza)})"
            else:
                nombre_detectado = "Desconocido"
                color_rect = (0, 0, 255)
                texto_pantalla = f"Desconocido ({int(confianza)})"

            cv2.rectangle(frame, (x, y), (x+w, y+h), color_rect, 2)
            cv2.putText(frame, texto_pantalla, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_rect, 2)

        # UI Inferior
        cv2.putText(frame, "SPACE: Registrar | Q: Salir", (20, 450), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        if ultimo_mensaje:
            cv2.putText(frame, ultimo_mensaje, (20, 400), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow('Toma de Asistencia', frame)
        
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        elif k == ord(' ') and nombre_detectado != "Desconocido":
            # REGISTRAR EN CSV
            ultimo_mensaje = registrar_asistencia(nombre_detectado)
            print(ultimo_mensaje)

    cap.release()
    cv2.destroyAllWindows()

def menu_principal():
    os.system('cls' if os.name == 'nt' else 'clear') 
    print("=" * 40)
    print("   Sistema de Asistencia PCA")
    print("=" * 40)
    print("1. Registrar Nuevo Alumno (Captura Facial)")
    print("2. Realizar Asistencia (Reconocimiento)")
    print("3. Salir")
    print("=" * 40)
    return input("Elige una opción: ").strip()

def ejecutar_menu():
    while True:
        opcion = menu_principal() 
        if opcion == '1':
            codigo = input("Código del alumno: ").strip().upper()
            capturar_y_registrar_fotos(codigo)
        elif opcion == '2':
            proceso_tomar_asistencia()
        elif opcion == '3':
            break
        else:
            print("Opción no válida.")
            time.sleep(1)