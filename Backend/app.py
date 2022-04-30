from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def Index():
    return "corriendo"


@app.route('/procesarxml', methods=["POST"])
def procesar_xml():
    data = request.json["xml"]
    print("xml a analizar:", data)
    return "recibido"


if __name__ == '__main__':
    app.run(debug=True)
