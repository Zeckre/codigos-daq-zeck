import time
import Adafruit_ADS1x15
import matplotlib.pyplot as plt

# --- Configuración del Hardware ---
# Crea una instancia del ADC ADS1115 en el bus I2C 1 (típico para Raspberry Pi)
adc = Adafruit_ADS1x15.ADS1115(busnum=1)

# Ajustes de ganancia y conversión
GAIN = 1  # 1 = +/-4.096V
VOLTAGE_FSR = 4.096 # El rango de voltaje de escala completa para GAIN 1
MAX_VALUE_16BIT = 32767 # Valor máximo firmado de 16 bits para el ADC

# --- Recolección de Datos ---
data_values = []
time_values = []
start_time = time.time()
duration = 10  # Duración de la recolección en segundos

print(f"Recolectando datos durante {duration} segundos...")

try:
    while (time.time() - start_time) < duration:
        # Leer el canal 0 con la ganancia y tasa de datos especificadas
        # La tasa de datos (data_rate=860) es la más rápida disponible
        value = adc.read_adc(0, gain=GAIN, data_rate=860)
        
        # Calcular el voltaje real (la biblioteca Adafruit_ADS1x15 no lo hace automáticamente)
        # Una forma más limpia de calcular el voltaje:
        voltage = value * (VOLTAGE_FSR / MAX_VALUE_16BIT)

        current_time = time.time() - start_time
        
        data_values.append(voltage)
        time_values.append(current_time)
        
        # time.sleep(0.01) # Una pequeña pausa puede ayudar a no saturar la CPU si es necesario

except KeyboardInterrupt:
    print("Recolección de datos interrumpida por el usuario.")

print(f"Datos recolectados: {len(data_values)} muestras.")

# --- Graficación de Datos ---
plt.figure(figsize=(10, 6))
plt.plot(time_values, data_values, marker='o', linestyle='-')
plt.title("Señal del ADC ADS1115 en el Tiempo")
plt.xlabel("Tiempo (segundos)")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.show()
