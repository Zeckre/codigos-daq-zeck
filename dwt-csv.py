import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pywt
import sys
import os

NOMBRE_ARCHIVO = 'muestras-daq.csv'

if not os.path.exists(NOMBRE_ARCHIVO):
    print(f"Error: No se encontró el archivo '{NOMBRE_ARCHIVO}'")
    sys.exit(1)

# Cargar los datos desde el archivo CSV
df = pd.read_csv(NOMBRE_ARCHIVO)
tiempo = df['Tiempo (s)'].values

# --- CORRECCIÓN AQUÍ: Usar el nuevo nombre de columna ---
# Reemplazamos 'Valor Voltios' por 'Valor Voltios (sin offset)'
nombre_columna_voltaje = 'Valor Voltios (sin offset)' 

if nombre_columna_voltaje not in df.columns:
    print(f"Error: No se encontró la columna '{nombre_columna_voltaje}' en el archivo CSV.")
    # Si quieres usar el nombre viejo como fallback, descomenta la siguiente línea:
    # nombre_columna_voltaje = 'Valor Voltios'
    # if nombre_columna_voltaje not in df.columns:
    #      print("Error: Tampoco se encontró 'Valor Voltios'.")
    #      sys.exit(1)

voltaje = df[nombre_columna_voltaje].values
N = len(voltaje)

# --- Configuración de la Transformada Wavelet Discreta (DWT) ---

# Elegimos la wavelet base (ej. 'db1' para Haar, 'db4' es popular)
wavelet = 'db6' 

# Nivel de descomposición
nivel = 1 

print(f"Aplicando DWT ({wavelet}) con nivel {nivel} a {N} muestras...")

# --- 1. Aplicar la DWT ---

# La DWT devuelve los coeficientes de aproximación (cA) y detalle (cD)
cA, cD = pywt.dwt(voltaje, wavelet, mode='symmetric')

print(f"Longitud de coeficientes de Aproximación (cA): {len(cA)}")
print(f"Longitud de coeficientes de Detalle (cD): {len(cD)}")


# --- 2. Analizar las componentes ---

# Podemos reconstruir las señales a partir de los coeficientes para graficarlas:
# Reconstruir solo la componente de baja frecuencia (tendencia)
A = pywt.idwt(cA, None, wavelet, mode='symmetric') 
# Reconstruir solo la componente de alta frecuencia (ruido/detalle)
D = pywt.idwt(None, cD, wavelet, mode='symmetric') 

# --- CORRECCIÓN AQUÍ: Ajustar las longitudes para graficar ---
# El algoritmo de DWT/IDWT puede producir arrays ligeramente más largos. 
# Recortamos los arrays reconstruidos A y D para que coincidan exactamente con la longitud original N.
A = A[:N]
D = D[:N]

# --- 3. Visualización de Resultados (Añadido para utilidad) ---

plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(tiempo, voltaje, label='Señal Original',
         linewidth=0.5)
plt.title('Señal Original Adquirida')
plt.xlabel('Tiempo (s)')
plt.ylabel('Voltaje (V)')
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(tiempo, A, label=f'Aproximación (Baja Frecuencia) - {wavelet}', color='green',
         linewidth=0.5)
plt.title('Componente de Aproximación')
plt.xlabel('Tiempo (s)')
plt.ylabel('Voltaje (V)')
plt.grid(True)
plt.legend()


plt.subplot(3, 1, 3)
plt.plot(tiempo, D, label=f'Detalle (Alta Frecuencia) - {wavelet}', color='red',
         linewidth=0.5)
plt.title('Componente de Detalle (Ruido)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Voltaje (V)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

