# Práctica: Conversor de Divisas

Aplicación web desarrollada con Flask para convertir divisas utilizando la API de Frankfurter. La aplicación también muestra un gráfico del historial de los últimos 30 días de la conversión seleccionada.

## Requisitos
- Python 3
- Flask
- Requests
- Matplotlib

## Instalación y Ejecución
1. Clonar el repositorio.
2. Instalar las dependencias en tu entorno:
   ```bash
   pip install flask requests matplotlib
   ```
3. Ejecutar la aplicación:
   ```bash
   python app.py
   ```
4. El navegador se abrirá automáticamente en `http://127.0.0.1:5001`.

## Uso
Seleccione la cantidad, la divisa de origen y la de destino, y haga clic en convertir para ver el resultado actual y el gráfico de tendencia de los últimos 30 días.
