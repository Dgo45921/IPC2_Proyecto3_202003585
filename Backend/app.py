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


@app.route('/procesarxml_prueba', methods=["POST"])
def procesar_xml_prueba():
    data = request.json["xml"]
    resultado = ManejoXML.analizar_prueba(data)
    # print(resultado)
    return resultado


@app.route('/resumen_fecha', methods=["POST"])
def generar_resumen_fecha():

    return "hola"


if __name__ == '__main__':
    app.run(debug=True)
