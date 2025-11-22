import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import sys
import os

NOMBRE_ARCHIVO_CSV = 'muestras-daq.csv'
COLUMNA_VOLTAJE = 'Valor Voltios (sin offset)'

if not os.path.exists(NOMBRE_ARCHIVO_CSV):
    print(f"Error: No se encontró el archivo '{NOMBRE_ARCHIVO_CSV}'")
    sys.exit(1)

# Cargar los datos desde el archivo CSV
df = pd.read_csv(NOMBRE_ARCHIVO_CSV)
tiempo = df['Tiempo (s)'].values
voltaje = df[COLUMNA_VOLTAJE].values
N = len(voltaje) # Número de puntos de datos

# Calcular la tasa de muestreo promedio (Fs)
if N > 1:
    duracion_total = tiempo[-1] - tiempo[0]
    Fs = N / duracion_total
    print(f"Tasa de muestreo (Fs) aproximada: {Fs:.2f} Hz")
else:
    print("Error: No hay suficientes datos para calcular Fs.")
    sys.exit(1)

# --- Aplicar la FFT ---

# Calcular la FFT
# np.abs() toma la magnitud de los números complejos resultantes
yf = np.abs(fft(voltaje))

# Calcular las frecuencias correspondientes
# fftfreq devuelve las frecuencias para N puntos y tasa de muestreo Fs
xf = fftfreq(N, 1/Fs)

# --- Visualización del Espectro de Frecuencia ---

plt.figure(figsize=(10, 6))

# Graficamos solo el lado positivo del espectro (frecuencias positivas)
# Esto es suficiente para señales reales
plt.plot(xf[:N//2], 2.0/N * yf[:N//2],
         linewidth=0.5) 

plt.title('Espectro de Frecuencia (FFT)')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud Normalizada (Voltios Pico)')
plt.grid()

# Establecer límites de frecuencia si es necesario (ej. hasta Fs/2)
# plt.xlim(0, Fs/2) 

plt.show()

