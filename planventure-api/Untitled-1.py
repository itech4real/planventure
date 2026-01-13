// filepath: planventure-api/routes.py
from flask import jsonify
from app import app

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/version', methods=['GET'])
def version():
    return jsonify({'version': '1.0.0'}), 200