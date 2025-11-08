import os
import cv2

# Base de datos local de las imagenes de alumnos
DATA_DIR = 'dataset_alumnos'

def asegurar_directorio_principal():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Directorio de datos listo: {DATA_DIR}")

def crear_directorio_alumno(codigo_alumno):
    #Creamos la carpeta del alumno
    ruta_alumno = os.path.join(DATA_DIR, codigo_alumno)
    os.makedirs(ruta_alumno, exist_ok=True)
    return ruta_alumno

def guardar_foto(ruta_alumno, contador, frame):
    # Guardamos la foto en la carpeta del alumno correspondiente (Por codigo de alumno)
    nombre_archivo = f"{str(contador).zfill(2)}.png"
    ruta_guardado = os.path.join(ruta_alumno, nombre_archivo)
    
    cv2.imwrite(ruta_guardado, frame)
    return ruta_guardado