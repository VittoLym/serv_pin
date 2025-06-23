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
    data = request.get_json()
    perfil = 'N/A' 
    destinatario = data.get('destinatario','Desconocido')
    if('6120302' in destinatario):
        perfil = 'bzurita'
    elif '629967' in destinatario:
        perfil = 'noesosa'
    elif '602173' in destinatario:
        perfil = 'evelazqu'
    sms_db.append({
        "numero": data["numero"],
        "texto": data["texto"],
        "destinatario": perfil,
        "timestamp": datetime.now().isoformat()
    })
    return "OK"

@app.route('/sms-history', methods=['GET'])
def get_sms_history():
    sorted_sms = sorted(sms_db, key=lambda x: x['timestamp'], reverse=True)
    return jsonify(sorted_sms)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
