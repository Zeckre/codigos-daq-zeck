import flet as ft
import plotly.graph_objs as go
import Adafruit_ADS1x15
import time

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

    # Figura inicial vacía
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[], y=[], mode="lines", name="Señal"))
    fig.update_layout(
        xaxis_title="Tiempo (s)",
        yaxis_title="Voltaje (V)",
        yaxis_range=[0, VOLTAGE_FSR],
        title="Lectura ADC ADS1115 en Tiempo Real"
    )

    chart = ft.PlotlyChart(fig, expand=True)

    # --- Aquí va tu contenedor responsivo ---
    content_area = ft.Container(
        content=chart,   # ⬅️ reemplazamos el Text por el gráfico
        bgcolor="#FFFFFF",
        border_radius=10,
        padding=10,
        col={"xs":12, "sm":12, "md":6, "lg":4}
    )

    page.add(content_area)

    # Función para actualizar el gráfico periódicamente
    def update_chart():
        value = adc.read_adc(0, gain=GAIN, data_rate=860)
        voltage = value * (VOLTAGE_FSR / MAX_VALUE_16BIT)
        current_time = time.time() - start_time

        time_data.append(current_time)
        voltage_data.append(voltage)
        if len(time_data) > 1000:
            time_data.pop(0)
            voltage_data.pop(0)

        fig.data[0].x = time_data
        fig.data[0].y = voltage_data
        chart.figure = fig
        page.update()

        # Reprogramar cada 100 ms
        page.run_task(update_chart, delay=100)

    update_chart()

ft.app(target=main)
