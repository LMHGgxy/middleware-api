from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Cargar configuraciones desde JSON
with open('apis.json') as f:
    HTTP_SERVER_URL = json.load(f)

@app.route('/post_data', methods=['POST'])
def intermediario():
    try:
        data = request.get_json()
        host_option = data.get('host_option')
        if not host_option or host_option not in HTTP_SERVER_URL:
            return jsonify(error="Host no válido o no proporcionado."), 400

        base_url = HTTP_SERVER_URL[host_option]
        path = data.get('path', '')
        method = data.get('method', 'GET').upper()
        payload = data.get('data', {})

        full_url = f"{base_url}{path}"
        headers = data.get('headers', {})

        if method == 'GET':
            response = requests.get(full_url, headers=headers, params=payload)
        elif method == 'POST':
            response = requests.post(full_url, headers=headers, json=payload)
        elif method == 'PUT':
            response = requests.put(full_url, headers=headers, json=payload)
        elif method == 'DELETE':
            response = requests.delete(full_url, headers=headers, json=payload)
        else:
            return jsonify(error="Método HTTP no soportado."), 405

        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            return jsonify(text=response.text), response.status_code

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4523)
