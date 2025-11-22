import time
import Adafruit_ADS1x15
import numpy as np
import pyaudio
from scipy import signal
import sys

# --- Configuración del ADS1115 ---
adc = Adafruit_ADS1x15.ADS1115(busnum=1)
GAIN = 1  
DATA_RATE = 860 # Tasa de adquisición real del ADS1115 (máximo)

# --- Configuración de Audio ---
ACQUISITION_RATE_HZ = 860.0 # Frecuencia de muestreo de ENTRADA
PLAYBACK_RATE_HZ = 8000.0   # Frecuencia de muestreo de SALIDA (8kHz es muy compatible)

# Aumentamos el tamaño del chunk. Leer 2 segundos de datos a la vez (860 * 2 = 1720 muestras)
CHUNK_SIZE_ACQ = 860

OFFSET_APLICADO_HARDWARE = 1.5 # Tu offset físico

# Parámetros de conversión a Voltios y Audio
VOLTAJE_REFERENCIA = 4.096
CONVERSION_FACTOR = VOLTAJE_REFERENCIA / 32767.0
MAX_WAV_VALUE = 32767.0 # Rango de 16 bits para audio PCM


# Inicializar PyAudio
p = pyaudio.PyAudio()

# Abrir el stream de audio con la tasa de reproducción compatible
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=int(PLAYBACK_RATE_HZ),
                output=True,
                frames_per_buffer=1024) # Ajuste adicional del buffer de PyAudio

print(f"Adquiriendo a {ACQUISITION_RATE_HZ} Hz y reproduciendo a {PLAYBACK_RATE_HZ} Hz en tiempo real...")
print("Usando CHUNK_SIZE de {CHUNK_SIZE_ACQ}. Presiona Ctrl+C para detener.")

try:
    while True:
        # 1. Adquirir un CHUNK de muestras del ADS1115 a 860 Hz
        voltajes_sin_offset = []
        for _ in range(CHUNK_SIZE_ACQ):
            valor_crudo = adc.read_adc(0, gain=GAIN, data_rate=DATA_RATE)
            voltaje_leido = valor_crudo * CONVERSION_FACTOR
            v_sin_offset = voltaje_leido - OFFSET_APLICADO_HARDWARE
            voltajes_sin_offset.append(v_sin_offset)
        
        voltajes_sin_offset = np.array(voltajes_sin_offset)

        # 2. Remuestrear (Resamplear) los datos a la tasa de reproducción compatible
        num_muestras_salida = int(len(voltajes_sin_offset) * (PLAYBACK_RATE_HZ / ACQUISITION_RATE_HZ))
        audio_resampled = signal.resample(voltajes_sin_offset, num_muestras_salida)

        # 3. Normalizar y escalar para formato de audio int16
        max_abs_val = np.max(np.abs(audio_resampled))
        if max_abs_val > 0:
            escala_audio = MAX_WAV_VALUE / max_abs_val
            audio_data_int16 = (audio_resampled * escala_audio).astype(np.int16)
        else:
            audio_data_int16 = np.zeros(len(audio_resampled), dtype=np.int16)
            
        # 4. Escribir en el stream de audio
        # write() es bloqueante, espera a que el buffer de hardware se vacíe lo suficiente
        stream.write(audio_data_int16.tobytes())

except KeyboardInterrupt:
    print("Detenido por el usuario.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    # Cerrar el stream y terminar PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Reproducción y adquisición finalizadas.")


