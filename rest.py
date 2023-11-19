from flask import Flask, jsonify, request
import service

app = Flask(__name__)


@app.route('/request', methods=['POST'])
def request_to_chatbot():
    prompt = request.json.get("prompt")
    response = service.response(prompt)
    return jsonify(response), 200


@app.route('/welcome', methods=['GET'])
def welcome_message():
    response = service.welcome()
    return jsonify(response), 200


@app.route('/google-api-key', methods=['GET'])
def get_api_key():
    response = service.get_api_key()
    return jsonify(response), 200


@app.route('/google-api-key', methods=['POST'])
def save_api_key():
    api_key = request.json.get("api-key")
    response = service.save_api_key(api_key)
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)
