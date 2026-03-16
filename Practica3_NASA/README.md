# Práctica: APOD de la NASA

Aplicación web desarrollada con Flask que interactúa con la API de "Astronomy Picture of the Day" (APOD) de la NASA.

## Requisitos
- Python 3
- Flask
- Requests

## Obtener API Key de la NASA
Para que la aplicación funcione correctamente, es necesario obtener una API Key gratuita en [api.nasa.gov](https://api.nasa.gov/).

## Instalación, Configuración y Ejecución
1. Clonar el repositorio.
2. Instalar las dependencias:
   ```bash
   pip install flask requests python-dotenv
   ```
3. Crear un archivo `.env` en la raíz del proyecto y añadir tu API Key de forma segura:
   ```env
   NASA_API_KEY=tu_api_key_aqui
   ```
4. Ejecutar la aplicación:
   ```bash
   python app.py
   ```
5. El navegador se abrirá automáticamente en `http://127.0.0.1:5002`.
