import cv2
import numpy as np

class ModeloPCA:
    def __init__(self):
        self.face_recognizer = cv2.face.EigenFaceRecognizer_create()
        self.entrenado = False
        self.mapa_nombres = {}

    def entrenar(self, imagenes, etiquetas, mapa_nombres):
        """
        Entrena el modelo Eigenfaces con las imágenes cargadas.
        """
        if not imagenes or len(imagenes) == 0:
            print("Error: No hay imágenes para entrenar.")
            return False
            
        print(f"Entrenando PCA con {len(imagenes)} imágenes...")
        self.face_recognizer.train(imagenes, etiquetas)
        self.mapa_nombres = mapa_nombres
        self.entrenado = True
        print("Entrenamiento completado exitosamente.")
        return True

    def predecir(self, rostro_img):
        """
        Recibe un recorte de rostro (100x100 gris) y devuelve el código del alumno.
        """
        if not self.entrenado:
            return "Modelo No Entrenado", float('inf')
        
        # El reconocedor devuelve (etiqueta, confianza/distancia)
        # En Eigenfaces, menor distancia = mejor coincidencia.
        # Distancias > 3000-4000 suelen ser desconocidos.
        label, distancia = self.face_recognizer.predict(rostro_img)
        
        codigo = self.mapa_nombres.get(label, "Desconocido")
        return codigo, distancia