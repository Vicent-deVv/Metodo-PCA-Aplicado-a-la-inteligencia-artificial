import os
import cv2
import numpy as np

data_dir = 'dataset_alumnos'

def asegurar_directorio_principal():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Directorio creado: {data_dir}")

def crear_directorio_alumno(codigo_alumno):
    ruta_alumno = os.path.join(data_dir, codigo_alumno)
    if not os.path.exists(ruta_alumno):
        os.makedirs(ruta_alumno)
    return ruta_alumno

def guardar_foto(ruta_alumno, contador, rostro_procesado):
    nombre_archivo = f"{str(contador).zfill(2)}.png"
    ruta_guardado = os.path.join(ruta_alumno, nombre_archivo)
    cv2.imwrite(ruta_guardado, rostro_procesado)
    return ruta_guardado

def cargar_dataset_entrenamiento():
    #Recorre todas las carpetas de alumnos, carga las imágenes, las aplana y devuelve los datos para el PCA.
    
    imagenes = []
    etiquetas = []
    nombres_codigos = {}
    
    if not os.path.exists(data_dir):
        print("No existe el dataset.")
        return None, None, None

    carpetas_alumnos = os.listdir(data_dir)
    label_id = 0
    
    print("Cargando base de datos de rostros")
    
    for codigo in carpetas_alumnos:
        ruta_carpeta = os.path.join(data_dir, codigo)
        if not os.path.isdir(ruta_carpeta):
            continue
            
        nombres_codigos[label_id] = codigo
        
        for nombre_foto in os.listdir(ruta_carpeta):
            if nombre_foto.endswith('.png') or nombre_foto.endswith('.jpg'):
                ruta_foto = os.path.join(ruta_carpeta, nombre_foto)
                
                # Leemos en escala de grises
                img = cv2.imread(ruta_foto, cv2.IMREAD_GRAYSCALE)
                
                # Aseguramos que sea del tamaño correcto (ej. 100x100) por seguridad
                if img is not None:
                    img = cv2.resize(img, (100, 100))
                    imagenes.append(img)
                    etiquetas.append(label_id)
        
        label_id += 1
        
    return imagenes, np.array(etiquetas), nombres_codigos