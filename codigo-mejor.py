import time
import io
import base64
import Adafruit_ADS1x15
import matplotlib.pyplot as plt
import flet as ft

# --- Configuración del Hardware ---
adc = Adafruit_ADS1x15.ADS1115(busnum=1)
GAIN = 1
VOLTAGE_FSR = 4.096
MAX_VALUE_16BIT = 32767

time_data = []
voltage_data = []
start_time = time.time()

def main(page: ft.Page):
    page.title = "DAQ Biomédico en Tiempo Real"

    # Imagen inicial vacía
    img = ft.Image(src_base64="", width=500, height=300)

    # Contenedor responsivo
    content_area = ft.Container(
        content=img,
        bgcolor="#FFFFFF",
        border_radius=10,
        padding=10,
        col={"xs":12, "sm":12, "md":6, "lg":4}
    )
    page.add(content_area)

    def update_chart():
        # Leer ADC
        value = adc.read_adc(0, gain=GAIN, data_rate=860)
        voltage = value * (VOLTAGE_FSR / MAX_VALUE_16BIT)
        current_time = time.time() - start_time

        # Guardar datos
        time_data.append(current_time)
        voltage_data.append(voltage)
        if len(time_data) > 1000:
            time_data.pop(0)
            voltage_data.pop(0)

        # Dibujar con Matplotlib
        fig, ax = plt.subplots()
        ax.plot(time_data, voltage_data, lw=1)
        ax.set_ylim(0, VOLTAGE_FSR)
        ax.set_xlim(max(0, current_time-10), current_time+1)
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Voltaje (V)")
        ax.set_title("Lectura ADC ADS1115 en Tiempo Real")
        ax.grid(True)

        # Guardar en buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        # Convertir a base64 y actualizar imagen en Flet
        img.src_base64 = base64.b64encode(buf.read()).decode("utf-8")
        page.update()

        # Reprogramar actualización cada 200 ms
        page.run_task(update_chart, delay=200)

    update_chart()

ft.app(target=main)
