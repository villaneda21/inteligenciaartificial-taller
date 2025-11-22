# script_ventas_v1.py
import csv
import json

# Código sucio sin funciones
archivo = "datos.csv"
f = open(archivo, 'r')
lector = csv.reader(f)
datos = list(lector)
f.close()

salida = []
for fila in datos:
    obj = {"id": fila[0], "monto": int(fila[1]) * 1.19} # Hardcode del IVA
    salida.append(obj)

f2 = open("reporte.json", 'w')
json.dump(salida, f2)
f2.close()
print("Listo")