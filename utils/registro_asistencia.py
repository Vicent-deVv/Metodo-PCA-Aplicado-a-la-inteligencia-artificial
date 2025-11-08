import cv2
import time 
import os
from .file_manager import crear_directorio_alumno, guardar_foto

NUM_FOTOS_POR_ALUMNO = 20
INTERVALO_TOMA = 0.1 

def capturar_y_registrar_fotos(codigo_alumno):
    if not codigo_alumno:
        print("El codigo de alumno no puede estar vacio.")
        return

    ruta_alumno = crear_directorio_alumno(codigo_alumno)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("No se pudo acceder a la camara.")
        return

    print(f"\n Preparando el registro para {codigo_alumno}")
    
    # --- CUENTA REGRESIVA ---
    duracion_cuenta_regresiva = 3
    tiempo_inicio = time.time()
    tiempo_finalizar = tiempo_inicio + duracion_cuenta_regresiva
    
    print(f"Posiciona tu rostro. El registro inicia en {duracion_cuenta_regresiva} segundos")
    
    # Bucle para mostrar la cámara y la cuenta regresiva
    while time.time() < tiempo_finalizar:
        ret, frame = cap.read()
        if not ret: break

        tiempo_restante = int(tiempo_finalizar - time.time())
        
        # Muestra la cuenta regresiva en el centro de la imagen
        cv2.putText(frame, f"INICIO EN: {tiempo_restante}", (50, 200), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
        cv2.imshow('Registro Facial', frame)

        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q'): 
            cap.release(); cv2.destroyAllWindows(); return
    
    print("\n INICIANDO CAPTURA AUTOMÁTICA")
    
    # --- CAPTURA AUTOMÁTICA ---
    contador = 1
    tiempo_ultima_captura = time.time() # Registra el momento de la primera captura

    while contador <= NUM_FOTOS_POR_ALUMNO:
        ret, frame = cap.read()
        if not ret: break

        tiempo_actual = time.time()
        
        # Condición para tomar la foto
        if tiempo_actual - tiempo_ultima_captura >= INTERVALO_TOMA:
            
            ruta_guardado = guardar_foto(ruta_alumno, contador, frame)
            print(f" Foto {contador} guardada en: {ruta_guardado}")
            
            contador += 1
            tiempo_ultima_captura = tiempo_actual # Actualiza el tiempo de la última captura

        # Muestra el progreso en la pantalla
        cv2.putText(frame, f"Capturando... {contador - 1}/{NUM_FOTOS_POR_ALUMNO}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('Registro Facial', frame)

        # Mantiene la ventana activa y permite presionar 'q' para salir
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q'): 
            print("\nCaptura cancelada.")
            break

    # --- FINALIZACIÓN ---
    cap.release()
    cv2.destroyAllWindows()
    
    if contador > NUM_FOTOS_POR_ALUMNO:
        print(f"\n🎉 ¡Registro de {codigo_alumno} completado con éxito! ({NUM_FOTOS_POR_ALUMNO} fotos tomadas)")

def menu_principal():
    # Limpia la terminal para que el menú siempre se vea limpio.
    os.system('cls' if os.name == 'nt' else 'clear') 

    print("=" * 40)
    print("      Sistema de toma de asistencia mediante metodo PCA")
    print("=" * 40)
    print("1.Registrar Nuevo Alumno (Capturar Fotos)")
    print("2.Realizar Asistencia (Todavia no incluido)")
    print("3.Salir")
    print("=" * 40)

    opcion = input("Elige una opción: ").strip()
    return opcion

# utils/registro_asistencia.py (Añadir esta función)

def ejecutar_menu():
    while True:
        opcion = menu_principal() 

        if opcion == '1':
            codigo = input("Ingresa el código del alumno (ej: 123456): ").strip().upper()
            
            if codigo:
                capturar_y_registrar_fotos(codigo)
            else:
                print("El codigo de alumno no puede estar vacio.")
            
            input("\nPresiona ENTER para volver al menu")

        elif opcion == '2':
            print("Esta funcion se implementará en la entrega final.")
            input("\nPresiona ENTER para volver al menú")

        elif opcion == '3':
            print("Saliendo del programa.")
            break

        else:
            print("Opcion no válida. Intentalo de nuevo.")
            time.sleep(1) 