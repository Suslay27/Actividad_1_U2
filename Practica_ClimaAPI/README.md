# Práctica: Clima API

Aplicación web en Flask que utiliza la API de OpenWeatherMap para mostrar el clima actual de cualquier ciudad del mundo.

## Requisitos
- Python 3
- Flask
- Requests
- python-dotenv

## Instalación, Configuración y Ejecución
1. Clonar el repositorio.
2. Instalar las dependencias:
   ```bash
   pip install flask requests python-dotenv
   ```
3. Crear un archivo llamado `.env` en la raíz del proyecto basándose en `.env.example` y añadir tu API Key de OpenWeatherMap de forma segura:
   ```env
   OPENWEATHER_API_KEY=tu_api_key_aqui
   ```
   *Nota: las API keys no deben incluirse en el código fuente, la aplicación las carga automáticamente desde este archivo y las expone como variables de entorno.*
4. Ejecutar la aplicación:
   ```bash
   python clima.py
   ```
5. El navegador se abrirá automáticamente en `http://127.0.0.1:5000`.
