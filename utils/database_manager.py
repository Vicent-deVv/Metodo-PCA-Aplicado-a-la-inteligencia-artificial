import csv
import os
from datetime import datetime

archivo_asistencia = "asistencia_curso.csv"

def registrar_asistencia(codigo_alumno):

    #Tomamos la fecha de hoy
    n = datetime.now()
    #Con la fecha tomada anteriormente, tomamos la fecha y hora actual
    fecha_hoy = n.strftime('%Y-%m-%d')
    hora_actual = n.strftime('%H:%M:%S')
    
    # Crear archivo con cabeceras si no existe
    if not os.path.isfile(archivo_asistencia):
        with open(archivo_asistencia, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Codigo', 'Fecha', 'Hora', 'Estado'])

    # Verificar si ya marcó hoy
    registrado = False
    with open(archivo_asistencia, 'r') as f:
        lector = csv.reader(f)
        for fila in lector:
            if fila and fila[0] == str(codigo_alumno) and fila[1] == fecha_hoy:
                registrado = True
                break
    
    if not registrado:
        with open(archivo_asistencia, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([codigo_alumno, fecha_hoy, hora_actual, 'Presente'])
        return f"Asistencia registrada para: {codigo_alumno}"
    else:
        return f"El alumno {codigo_alumno} ya registro asistencia hoy."