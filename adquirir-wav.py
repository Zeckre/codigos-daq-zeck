import time
import Adafruit_ADS1x15
import numpy as np
import wave
import struct
import matplotlib.pyplot as plt
import sys
import os

# --- Configuración del ADS1115 ---
adc = Adafruit_ADS1x15.ADS1115(busnum=1)
GAIN = 1  # Rango +/-4.096V

# Tasa de datos del ADS1115 (8 a 860 SPS - muestras por segundo)
# Usaremos 860 SPS para la máxima velocidad de adquisición
DATA_RATE = 860 

# La tasa de muestreo para el archivo WAV DEBE coincidir con la tasa de adquisición
SAMPLE_RATE_HZ = DATA_RATE # Usamos 860 Hz para ser precisos con la adquisición

CANTIDAD_MUESTRAS = 10000
NOMBRE_ARCHIVO_WAV = 'senal_adquirida.wav'
# Ajusta este valor al offset que aplicaste en hardware
OFFSET_APLICADO_HARDWARE = 1.5

# --- Parámetros de conversión a Voltios ---
VOLTAJE_REFERENCIA = 4.096
MAX_VALOR_CRUDO = 32767.0
CONVERSION_FACTOR = VOLTAJE_REFERENCIA / MAX_VALOR_CRUDO
# Rango de 16 bits para audio PCM
MAX_WAV_VALUE = 32767.0 


print(f"Iniciando recolección de {CANTIDAD_MUESTRAS} muestras a {SAMPLE_RATE_HZ} Hz en WAV...")

datos_adquiridos = []
inicio_tiempo = time.time()

# Abrir el archivo WAV para escribir en modo binario
try:
    wav_file = wave.open(NOMBRE_ARCHIVO_WAV, 'wb')
    wav_file.setnchannels(1)  # Mono channel
    wav_file.setsampwidth(2)  # 2 bytes per sample (16 bit)
    wav_file.setframerate(SAMPLE_RATE_HZ)
except wave.Wave_write_error as e:
    print(f"Error al abrir archivo WAV: {e}")
    sys.exit(1)


try:
    for i in range(CANTIDAD_MUESTRAS):
        # Leer el canal 0 (A0)
        valor_crudo = adc.read_adc(0, gain=GAIN, data_rate=DATA_RATE)
        
        # Convertir a Voltaje real (con offset)
        voltaje_leido = valor_crudo * CONVERSION_FACTOR
        
        # Quitar el offset aplicado físicamente
        voltaje_sin_offset = voltaje_leido - OFFSET_APLICADO_HARDWARE

        # --- Preparar datos para WAV (normalizar y convertir a int16 binario) ---
        # Escalar el voltaje al rango de audio (-32767 a 32767)
        # Asumimos que tu señal real está en un rango razonable, ej. +/- 1.5V
        # Si la señal se sale de rango, se recortará (clipping)
        audio_value = int(np.clip(voltaje_sin_offset * (MAX_WAV_VALUE / (VOLTAJE_REFERENCIA/2)), 
                                  -MAX_WAV_VALUE, MAX_WAV_VALUE))
        
        # Empaquetar el entero de 16 bits en formato binario
        wav_frame = struct.pack('<h', audio_value)
        wav_file.writeframesraw(wav_frame)
        
        datos_adquiridos.append(voltaje_sin_offset) # Guardar para la gráfica

        if i % 1000 == 0:
            print(f"Muestra {i}/{CANTIDAD_MUESTRAS} - {voltaje_sin_offset:.4f}V")

except KeyboardInterrupt:
    print("Recolección interrumpida por el usuario.")
except OSError as e:
    print(f"Error de E/S (I2C): {e}")
finally:
    wav_file.close() # MUY IMPORTANTE CERRAR EL ARCHIVO WAV
    fin_tiempo = time.time()

duracion = fin_tiempo - inicio_tiempo
print(f"Recolección completada en {duracion:.2f} segundos.")
print(f"Datos guardados en '{NOMBRE_ARCHIVO_WAV}'")

# Reproducir el archivo WAV con aplay (comando de sistema)
print(f"\nReproduciendo con aplay:")
os.system(f"aplay {NOMBRE_ARCHIVO_WAV}")


# --- Mostrar la gráfica ---
if datos_adquiridos:
    tiempo_eje = np.linspace(0, duracion, len(datos_adquiridos))
    plt.figure(figsize=(10, 5))
    plt.plot(tiempo_eje, datos_adquiridos, linewidth=0.5)
    plt.title(f'Señal Adquirida y Guardada en WAV ({SAMPLE_RATE_HZ} Hz)')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Voltaje (V, sin offset)')
    plt.grid(True)
    plt.show()

