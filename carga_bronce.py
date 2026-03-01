import sys
import os
import tomli
import pandas as pd
import psycopg2.extras

# Permitir a Python leer la carpeta oculta .secrets
sys.path.append(os.path.abspath('.secrets'))
from database_config import get_connection

def cargar_a_supabase(conexion, archivo, ruta):
    print(f"\nLeyendo el archivo {archivo}...")
    
    # 1. Leer el CSV usando Pandas
    df = pd.read_csv(ruta)
    
    # 2. Agregar la columna de control 'fuente_archivo'
    df['fuente_archivo'] = archivo
    
    # 3. Obtener el nombre de la tabla (quitando '.csv')
    nombre_tabla = archivo.replace('.csv', '')
    
    # 4. Preparar la consulta SQL
    columnas = ','.join(list(df.columns))
    query = f"INSERT INTO bronze.{nombre_tabla} ({columnas}) VALUES %s"
    
    # 5. Convertir a formato compatible con psycopg2
    valores = [tuple(x) for x in df.to_numpy()]
    
    # 6. Ejecutar la inserción masiva en Supabase
    cursor = conexion.cursor()
    try:
        psycopg2.extras.execute_values(cursor, query, valores)
        conexion.commit() 
        print(f"¡Éxito! Se han cargado {len(df)} registros en la tabla bronze.{nombre_tabla}.")
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        conexion.rollback() 
    finally:
        cursor.close()

def main():
    print("Conectando a Supabase...")
    conexion = get_connection()
    if not conexion:
        sys.exit("No se pudo establecer conexión con la base de datos.")
    
    print("Conexión exitosa.")

    # Leer la ruta de los archivos desde el archivo toml
    try:
        with open('.secrets/secrets.toml', 'rb') as f:
            config = tomli.load(f)
            ruta_base = config['paths']['bronze_path']
    except FileNotFoundError:
        sys.exit("Error: No se encontró el archivo .secrets/secrets.toml")

    # Listar los archivos CSV
    archivos = [f for f in os.listdir(ruta_base) if f.endswith('.csv')]
    
    if not archivos:
        sys.exit(f"No se encontraron archivos en la ruta: {ruta_base}")

    print("\nArchivos disponibles para cargar:")
    for i, archivo in enumerate(archivos):
        print(f"{i + 1}. {archivo}")

    # Seleccionar archivo
    seleccion = input("\nSelecciona el número del archivo que deseas cargar: ")
    
    try:
        indice = int(seleccion) - 1
        if 0 <= indice < len(archivos):
            archivo_seleccionado = archivos[indice]
            ruta_completa = os.path.join(ruta_base, archivo_seleccionado)
            
            # Llamar a la función de carga
            cargar_a_supabase(conexion, archivo_seleccionado, ruta_completa)
        else:
            print("Número fuera de rango. Operación cancelada.")
    except ValueError:
        print("Entrada no válida. Operación cancelada.")

if __name__ == "__main__":
    main()