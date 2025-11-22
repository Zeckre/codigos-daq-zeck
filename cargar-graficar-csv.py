import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

NOMBRE_ARCHIVO = 'muestras-daq.csv'

if not os.path.exists(NOMBRE_ARCHIVO):
    print(f"Error: No se encontró el archivo '{NOMBRE_ARCHIVO}'")
    sys.exit(1)

# Cargar los datos desde el archivo CSV
df = pd.read_csv(NOMBRE_ARCHIVO)

print("Datos cargados:")
print(df.head())

# Graficar los datos
plt.figure(figsize=(10, 5))

# MODIFICA ESTA LÍNEA para cambiar el grosor
# Puedes usar 'linewidth' o la abreviatura 'lw'
plt.plot(df['Tiempo (s)'], df['Valor Voltios (sin offset)'], 
         label='Voltaje ADS1115', 
         color='r',
         linewidth=0.5) # <--- Cambia este valor (ej. 0.5, 0.2, 1.0)

plt.title('Lecturas DAQ 10000 muestras')
plt.xlabel('Tiempo (s)')
plt.ylabel('Voltios')
plt.ylim(-1.5, 1.5) 
plt.legend()
plt.grid(True)
plt.show()

