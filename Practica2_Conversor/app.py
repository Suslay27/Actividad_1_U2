import io
import base64
import datetime
import requests
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import webbrowser

app = Flask(__name__)

API_URL = "https://api.frankfurter.app"

@app.route('/')
def index():
    # Carga las monedas automáticamente desde la red
    resp = requests.get(f"{API_URL}/currencies")
    if resp.status_code == 200:
        monedas = resp.json()
    else:
        monedas = {}
    return render_template('index.html', monedas=monedas)

@app.route('/convertir', methods=['POST'])
def convertir():
    cantidad = request.form.get('cantidad')
    desde = request.form.get('desde')
    a = request.form.get('a')

    # Obtiene la conversión actual
    url_actual = f"{API_URL}/latest?amount={cantidad}&from={desde}&to={a}"
    resp_actual = requests.get(url_actual)
    if resp_actual.status_code == 200:
        data = resp_actual.json()
        resultado = data['rates'][a]
        fecha_act = data['date']
    else:
        resultado = 0
        fecha_act = "Error"

    # Obtiene datos de los últimos 30 días para el gráfico
    hoy = datetime.date.today()
    hace_30 = hoy - datetime.timedelta(days=30)
    url_hist = f"{API_URL}/{hace_30}..{hoy}?from={desde}&to={a}"
    resp_hist = requests.get(url_hist)
    
    if resp_hist.status_code == 200:
        data_hist = resp_hist.json()
        fechas = sorted(list(data_hist['rates'].keys()))
        valores = [data_hist['rates'][f][a] for f in fechas]
        
        if valores:
            media = sum(valores) / len(valores)
            var_abs = valores[-1] - valores[0]
            var_porc = (var_abs / valores[0]) * 100 if valores[0] != 0 else 0
        else:
            media = var_abs = var_porc = 0
    else:
        fechas = []
        valores = []
        media = var_abs = var_porc = 0

    # Crea el gráfico con estilo oscuro y colores modernos
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 5), facecolor='#0f172a00') # Transparent background
    ax = plt.gca()
    ax.set_facecolor('#0f172a00') # Transparent axes
    
    plt.plot(fechas, valores, color='#6366f1', linewidth=3, marker='o', markersize=5, markerfacecolor='#fff', markeredgecolor='#6366f1')
    
    max_val = max(valores)
    min_val = min(valores)
    plt.scatter(fechas[valores.index(max_val)], max_val, color='#22c55e', s=120, label=f'Peak: {max_val:.4f}', zorder=5, edgecolors='white')
    plt.scatter(fechas[valores.index(min_val)], min_val, color='#ef4444', s=120, label=f'Low: {min_val:.4f}', zorder=5, edgecolors='white')
    
    plt.title(f"Tendencia {desde} a {a}", pad=20, fontsize=14, fontweight='bold', color='#f8fafc')
    plt.xticks(fechas[::5], rotation=45, color='#94a3b8')
    plt.yticks(color='#94a3b8')
    
    legend = plt.legend(frameon=True, facecolor='#1e293b', edgecolor='#334155')
    plt.setp(legend.get_texts(), color='#f8fafc')
    
    plt.grid(True, linestyle='--', alpha=0.1, color='#94a3b8')
    
    # Eliminar bordes innecesarios
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Convierte el gráfico en una imagen de texto (Base64)
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', transparent=True, dpi=100)
    img.seek(0)
    grafico_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return render_template('resultado.html', 
                           res=f"{resultado:.2f}", 
                           tasa=f"{(resultado/float(cantidad)):.4f}", 
                           desde=desde, a=a, cant=cantidad,
                           fecha=fecha_act,
                           grafico=grafico_url,
                           media=f"{media:.4f}",
                           var_abs=f"{var_abs:.4f}",
                           var_porc=f"{var_porc:.2f}")

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5001')
    app.run(port=5001, debug=True)