import csv
import random
import os
from datetime import datetime, timedelta

# Asegurar que la carpeta assets/docs exista
os.makedirs('assets/docs', exist_ok=True)

# Listas de datos falsos para generar aleatoriedad
departamentos = ['Ventas', 'IT', 'Recursos Humanos', 'Marketing', 'Finanzas', 'Operaciones']
nombres = ['Juan', 'Maria', 'Carlos', 'Ana', 'Luis', 'Elena', 'Jorge', 'Lucia', 'Miguel', 'Sofia']
apellidos = ['Garcia', 'Martinez', 'Lopez', 'Gonzalez', 'Perez', 'Rodriguez', 'Sanchez', 'Ramirez']
niveles = ['Junior', 'Intermedio', 'Senior', 'Director']
categorias = ['Electronica', 'Mobiliario', 'Papeleria', 'Limpieza', 'Software']
productos_nom = ['Laptop', 'Silla', 'Escritorio', 'Monitor', 'Teclado', 'Raton', 'Impresora', 'Boligrafos', 'Cuaderno', 'Licencia']

# 1. Generar empleados.csv (100 filas)
with open('assets/docs/empleados.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id_empleado', 'nombre', 'apellido', 'departamento', 'salario', 'fecha_ingreso'])
    for i in range(1, 101):
        fecha = (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1500))).strftime('%Y-%m-%d')
        writer.writerow([f'E{i:03d}', random.choice(nombres), random.choice(apellidos), random.choice(departamentos), str(random.randint(1500, 5000)), fecha])

# 2. Generar manager.csv (100 filas)
with open('assets/docs/manager.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id_manager', 'nombre_completo', 'area_asignada', 'nivel_gerarquico'])
    for i in range(1, 101):
        nombre_comp = f"{random.choice(nombres)} {random.choice(apellidos)}"
        writer.writerow([f'M{i:03d}', nombre_comp, random.choice(departamentos), random.choice(niveles)])

# 3. Generar producto.csv (100 filas)
with open('assets/docs/producto.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id_producto', 'nombre_producto', 'categoria', 'precio', 'stock_disponible'])
    for i in range(1, 101):
        writer.writerow([f'P{i:03d}', random.choice(productos_nom), random.choice(categorias), str(round(random.uniform(10.0, 1500.0), 2)), str(random.randint(0, 500))])

print("¡Archivos CSV generados con éxito en la carpeta assets/docs!")