from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

HTTP_SERVER_URL = {
    'API_SERV_PRIN': os.getenv('API_SERV'),
    'API_SERV': os.getenv('API_SERV2'),
    "API_SERV_SAVE":os.getenv('API_SERV3'),
}

@app.route('/post_data', methods=['POST'])
def intermediario():
    try:
        data = request.get_json()
        host_option = data['host_option']
        if host_option not in HTTP_SERVER_URL:
            return jsonify(error="No se encontró el host"), 500
        
        HTTP_SERVER_URL_TEMP = HTTP_SERVER_URL[host_option]
        path = data['path']
        method = data['method']

        if method == 'GET':
            response = requests.get(HTTP_SERVER_URL_TEMP + path)
        elif method == 'POST':
            response = requests.post(HTTP_SERVER_URL_TEMP + path, json=data['data'])
        print(response.text)
        try:
            return jsonify(response.json()), response.status_code
        except:
            return jsonify(error="No se pudo obtener la respuesta del servidor"), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4523)