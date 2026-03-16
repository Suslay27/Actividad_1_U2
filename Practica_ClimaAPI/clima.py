import os
import requests
import webbrowser
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Cargamos la API Key desde las variables de entorno para mayor seguridad
API = os.environ.get("OPENWEATHER_API_KEY")

@app.route('/')
def index():
    # Vamos directo al buscador, sin pedir nada al usuario
    return render_template('index.html')

@app.route('/clima', methods=['POST'])
def buscar_clima():
    ciudad = request.form.get('ciudad')
    
    # La app usa tu llave interna automáticamente
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API}&units=metric&lang=es"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            return render_template('resultado.html', clima=datos)
        else:
            return render_template('error.html'), 404
    except:
        return render_template('error.html'), 500

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(port=5000, debug=True)