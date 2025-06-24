from flask import Flask, request, render_template,jsonify
from datetime import datetime
import os
app = Flask(__name__)

sms_db = []

@app.route('/', methods=['GET'])
def home():
    return render_template('main.html')

@app.route('/sms', methods=['POST'])
def sms():
    PERFILES = {
        '6120302': 'bzurita',
        '629967': 'noesosa',
        '602173': 'evelazqu'
    }
    
    try:
        data = request.get_json()
        
        # Validar datos obligatorios
        if not data or 'numero' not in data or 'texto' not in data:
            return "Faltan campos obligatorios (numero o texto)", 400
            
        # Determinar perfil
        destinatario = data.get('destinatario', 'Desconocido')
        perfil = 'N/A'
        
        # Buscar número en los perfiles (versión mejorada)
        for num, perf in PERFILES.items():
            if num in destinatario:
                perfil = perf
                break
        
        # Almacenar SMS
        sms_db.append({
            "numero": data["numero"],
            "texto": data["texto"],
            "destinatario": perfil,
            "timestamp": datetime.now().isoformat()
        })
        
        return "OK", 200
        
    except Exception as e:
        # Loggear el error si es necesario
        return f"Error al procesar SMS: {str(e)}", 500

@app.route('/sms-history', methods=['GET'])
def get_sms_history():
    sorted_sms = sorted(sms_db, key=lambda x: x['timestamp'], reverse=True)
    return jsonify(sorted_sms)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
