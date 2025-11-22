import pandas as pd
import numpy as np
from scipy.io.wavfile import write
import sys
import os

NOMBRE_ARCHIVO_CSV = 'muestras-daq.csv' # Archivo de entrada
NOMBRE_ARCHIVO_WAV = 'senal_audio1.wav'                 # Archivo de salida
COLUMNA_VOLTAJE = 'Valor Voltios (sin offset)'

# Frecuencia de muestreo estándar para audio. 
# Si usas un valor no estándar como 379 Hz, la reproducción manual con 'aplay' es la mejor opción.
SAMPLE_RATE_AUDIO = 380 # Hz (Valor de tu elección)

if not os.path.exists(NOMBRE_ARCHIVO_CSV):
    print(f"Error: No se encontró el archivo '{NOMBRE_ARCHIVO_CSV}'")
    sys.exit(1)
    
# Verificar la columna antes de cargar todo el DataFrame
try:
    temp_df = pd.read_csv(NOMBRE_ARCHIVO_CSV, nrows=1)
    if COLUMNA_VOLTAJE not in temp_df.columns:
        print(f"Error: No se encontró la columna '{COLUMNA_VOLTAJE}' en el archivo CSV.")
        sys.exit(1)
except Exception as e:
    print(f"Error al leer el encabezado del CSV: {e}")
    sys.exit(1)


try:
    # Cargar los datos desde el archivo CSV
    df = pd.read_csv(NOMBRE_ARCHIVO_CSV)
    # --- CORRECCIÓN APLICADA AQUÍ ---
    voltajes = df[COLUMNA_VOLTAJE].values
    
    print(f"Datos cargados. Cantidad de muestras: {len(voltajes)}")

    # Normalizar los datos al rango de audio (-32768 a 32767 para int16)
    
    max_abs_val = np.max(np.abs(voltajes))
    if max_abs_val == 0:
        print("La señal es plana (voltaje constante), no se puede generar audio significativo.")
        sys.exit(0)

    # Escalamos al rango de valores para audio (formato PCM de 16 bits es común)
    # El rango para int16 es de -32768 a 32767
    escala_audio = 32767 / max_abs_val
    audio_data = (voltajes * escala_audio).astype(np.int16)

    # Escribir el array numpy a un archivo WAV usando scipy
    write(NOMBRE_ARCHIVO_WAV, SAMPLE_RATE_AUDIO, audio_data)

    print(f"Archivo de audio '{NOMBRE_ARCHIVO_WAV}' generado exitosamente con tasa de muestreo {SAMPLE_RATE_AUDIO} Hz.")
    print("\nPara reproducirlo en la Raspberry Pi, usa la terminal:")
    print(f"  aplay {NOMBRE_ARCHIVO_WAV}")
    print("o, si tienes omxplayer instalado:")
    print(f"  omxplayer {NOMBRE_ARCHIVO_WAV}")


except FileNotFoundError:
    print(f"Error: El archivo '{NOMBRE_ARCHIVO_CSV}' no se encontró.")
    print("Asegúrate de ejecutar primero el script de recolección de datos.")
except Exception as e:
    print(f"Ocurrió un error: {e}")

