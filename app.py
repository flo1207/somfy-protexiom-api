from flask import Flask, jsonify, request
from somfy import Somfy, SomfyException  # On réutilise ta classe existante
import json

app = Flask(__name__)

# Charger les paramètres depuis un fichier de config externe
with open('config.json', 'r') as f:
    config = json.load(f)

URL = config['url']
PASSWORD = config['password']
CODES = config['codes']

# Endpoint pour tester si l'API est en ligne
@app.route('/api/ping')
def ping():
    return jsonify({"status": "ok", "message": "Somfy API is online."})

# Endpoint pour lire l'état général
@app.route('/api/state', methods=['GET'])
def get_state():
    try:
        with Somfy(URL, PASSWORD, CODES) as somfy:
            state = somfy.get_state()
            return jsonify(state)
    except SomfyException as e:
        return jsonify({"error": str(e)}), 400

# Endpoint pour lire l'état des zones d'alarme
@app.route('/api/zones', methods=['GET'])
def get_zone_states():
    try:
        with Somfy(URL, PASSWORD, CODES) as somfy:
            state = somfy.get_alarme_state()
            return jsonify(state)
    except SomfyException as e:
        return jsonify({"error": str(e)}), 400

# Endpoint pour activer une zone
@app.route('/api/zones/<zone>/on', methods=['POST'])
def activate_zone(zone):
    try:
        with Somfy(URL, PASSWORD, CODES) as somfy:
            if zone == "A":
                somfy.set_A()
            elif zone == "B":
                somfy.set_B()
            elif zone == "C":
                somfy.set_C()
            elif zone == "ABC":
                somfy.set_zone("ABC")
            else:
                return jsonify({"error": "Unknown zone"}), 400
            return jsonify({"status": f"Zone {zone} activated"})
    except SomfyException as e:
        return jsonify({"error": str(e)}), 400

# Endpoint pour désactiver une zone
@app.route('/api/zones/<zone>/off', methods=['POST'])
def deactivate_zone(zone):
    try:
        with Somfy(URL, PASSWORD, CODES) as somfy:
            if zone == "A":
                somfy.unset_A()
            elif zone == "B":
                somfy.unset_B()
            elif zone == "C":
                somfy.unset_C()
            elif zone == "ABC":
                somfy.unset_all_zones()
            else:
                return jsonify({"error": "Unknown zone"}), 400
            return jsonify({"status": f"Zone {zone} deactivated"})
    except SomfyException as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
