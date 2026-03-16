import requests
from flask import Flask, render_template, request, flash
from datetime import datetime, timedelta
import os
import webbrowser
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'nasa_secret_key' # For flash messages

# Configuración
NASA_API_KEY = os.environ.get('NASA_API_KEY', 'DEMO_KEY')
URL_BASE = "https://api.nasa.gov/planetary/apod"

# Proxy para evitar bloqueos del navegador (ORB/CORS)
@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return "Falta URL", 400
    try:
        # Descargar la imagen desde el servidor con User-Agent para evitar bloqueos 403
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        res = requests.get(url, stream=True, timeout=10, headers=headers)
        from flask import Response
        return Response(res.content, mimetype=res.headers.get('Content-Type'))
    except Exception as e:
        return str(e), 500

# BASE DE DATOS DE IMÁGENES REALES DE NASA (Respaldo)
IMAGENES_POR_FECHA = {
    "2005-09-27": {
        "title": "Los Pilares de la Creación",
        "explanation": "Los famosos Pilares de la Creación en la Nebulosa del Águila, capturados por el Hubble. Estas columnas de gas y polvo son viveros estelares donde nacen nuevas estrellas.",
        "url": "https://apod.nasa.gov/apod/image/0509/pillars_hst.jpg"
    },
    "2005-10-01": {
        "title": "La Galaxia del Sombrero",
        "explanation": "La galaxia del Sombrero (M104) es una de las galaxias más fotogénicas. Su brillante núcleo y su prominente carril de polvo la hacen parecer un sombrero.",
        "url": "https://apod.nasa.gov/apod/image/0510/sombrero_hst.jpg"
    }
}

def get_nasa_data(fecha_str):
    """Obtiene datos de la API de NASA o del respaldo local."""
    # Intentar con la API primero
    try:
        params = {
            'api_key': NASA_API_KEY,
            'date': fecha_str
        }
        print(f"Solicitando datos a NASA para: {fecha_str}")
        response = requests.get(URL_BASE, params=params, timeout=10)
        print(f"Respuesta NASA: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Límite de peticiones de NASA alcanzado (Rate Limit).")
        else:
            print(f"Error de API: {response.text}")
    except Exception as e:
        print(f"Excepción en la solicitud a NASA: {e}")
    
    # Si falla la API o no hay datos, buscar en respaldo local
    if fecha_str in IMAGENES_POR_FECHA:
        print(f"Cargando desde cache local para: {fecha_str}")
        data = IMAGENES_POR_FECHA[fecha_str].copy()
        data['date'] = fecha_str
        data['media_type'] = 'image'
        return data
    
    # Imagen genérica si nada más funciona
    print(f"Usando imagen de respaldo para: {fecha_str}")
    return {
        "title": "Universo Infinito (Vista de Respaldo)",
        "explanation": f"Lo sentimos, no pudimos conectar con los servidores de la NASA para la fecha {fecha_str}. Intenta con otra fecha o verifica tu conexión.",
        "url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=1920&q=80",
        "media_type": "image",
        "date": fecha_str
    }

def get_nasa_gallery(fecha_fin_dt):
    """Obtiene galería de imágenes de los últimos 7 días (incluyendo el actual)."""
    fecha_inicio_dt = fecha_fin_dt - timedelta(days=6)
    try:
        params = {
            'api_key': NASA_API_KEY,
            'start_date': fecha_inicio_dt.strftime('%Y-%m-%d'),
            'end_date': fecha_fin_dt.strftime('%Y-%m-%d')
        }
        res = requests.get(URL_BASE, params=params, timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error al obtener galería NASA: {e}")
        
    # Galería de respaldo local
    print("Cargando galería de respaldo local")
    galeria_respaldo = []
    for date_key, info in IMAGENES_POR_FECHA.items():
        item = info.copy()
        item['date'] = date_key
        item['media_type'] = 'image'
        galeria_respaldo.append(item)
    return galeria_respaldo

@app.route('/')
def index():
    # Obtener fecha de la URL
    fecha_str = request.args.get('fecha')
    
    # Fechas importantes
    hoy_dt = datetime.now()
    hoy_str = hoy_dt.strftime('%Y-%m-%d')
    limite_inicio = "1995-06-16"
    
    # Si no hay fecha o es inválida, usar hoy
    if not fecha_str:
        fecha_str = hoy_str
    
    try:
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d')
    except ValueError:
        fecha_str = hoy_str
        fecha_dt = hoy_dt

    # Validar rango de fechas
    fecha_limite_dt = datetime.strptime(limite_inicio, '%Y-%m-%d')
    if fecha_dt < fecha_limite_dt:
        fecha_dt = fecha_limite_dt
        fecha_str = limite_inicio
    elif fecha_dt > hoy_dt:
        fecha_dt = hoy_dt
        fecha_str = hoy_str

    # Obtener datos
    data = get_nasa_data(fecha_str)
    galeria = get_nasa_gallery(fecha_dt)
    
    # Calcular navegación
    ayer = (fecha_dt - timedelta(days=1)).strftime('%Y-%m-%d')
    ayer_valido = (fecha_dt - timedelta(days=1)) >= fecha_limite_dt
    
    manana = (fecha_dt + timedelta(days=1)).strftime('%Y-%m-%d')
    manana_valido = (fecha_dt + timedelta(days=1)) <= hoy_dt
    
    es_hoy = (fecha_str == hoy_str)

    return render_template('index.html', 
                         datos=data, 
                         galeria=galeria,
                         ayer=ayer if ayer_valido else None, 
                         manana=manana if manana_valido else None, 
                         es_hoy=es_hoy, 
                         fecha_actual=fecha_str, 
                         limite=limite_inicio,
                         hoy=hoy_str)

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5002')
    app.run(debug=True, port=5002)
