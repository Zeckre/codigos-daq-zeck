import numpy as np
import csv
from scipy.io.wavfile import write

# Parámetros
CSV_FILE = "muestras-daq.csv"
WAV_FILE = "muestras-daq.wav"
FS = 8000 

# Leer datos del CSV
tiempos = []
voltajes = []

with open(CSV_FILE, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        tiempos.append(float(row['tiempo']))
        voltajes.append(float(row['voltios']))

# Convertir a numpy array
signal = np.array(voltajes)

# Normalizar la señal a rango -32767..32767 (16 bits PCM)
signal_norm = signal / np.max(np.abs(signal))   # Escala entre -1 y 1
signal_int16 = np.int16(signal_norm * 32767)

# Guardar como WAV
write(WAV_FILE, FS, signal_int16)

print(f"Archivo WAV generado: {WAV_FILE}")

