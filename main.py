from utils.registro_asistencia import ejecutar_menu
from utils.file_manager import asegurar_directorio_principal
import sys
import os


if __name__ == "__main__":

    asegurar_directorio_principal() 
    ejecutar_menu()
