from flask import Flask, request
from flask_cors import CORS
import ManejoXML


app = Flask(__name__)
CORS(app)


@app.route('/')
def Index():
    return "corriendo"


@app.route('/procesarxml', methods=["POST"])
def procesar_xml():
    data = request.json["xml"]
    texto_xml = ManejoXML.analizar(data)
    return texto_xml


if __name__ == '__main__':
    app.run(debug=True)
