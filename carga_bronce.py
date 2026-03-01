import os
import sys
import tomli

# Leer la carpeta secreta
sys.path.append(os.path.abspath('.secrets'))
from database_config import get_connection

# 1. Probar Conexión
conn = get_connection()
print("Conexión éxito a Supabase")

# 2. Leer archivo TOML para la ruta
with open(".secrets/secrets.toml", "rb") as f:
    config = tomli.load(f)
ruta_archivos = config["paths"]["bronze"]

# 3. Listar archivos y menú interactivo
archivos = [f for f in os.listdir(ruta_archivos) if f.endswith('.csv') or f.endswith('.xlsx')]

print("Archivos disponibles:")
for indice, archivo in enumerate(archivos):
    print(f"{indice}: {archivo}")

entrada = input("Selecciona el número del archivo que deseas cargar: ")

try:
    indice_seleccionado = int(entrada)
    if 0 <= indice_seleccionado < len(archivos):
        print(f"Archivo seleccionado: {archivos[indice_seleccionado]}")
        # (Aquí continuará el código en la próxima clase para hacer el insert a Supabase)
    else:
        print("Número inválido.")
        sys.exit()
except ValueError:
    print("Debes ingresar un número válido.")
    sys.exit()