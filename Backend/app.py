from flask import Flask, request, jsonify
from flask_cors import CORS
import ManejoXML
import Manejo_Peticiones

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
    date = request.json["fecha"]
    empresa = request.json["empresa"]
    texto_xml = request.json["xml"]
    if date == "all" and empresa == "all":
        respuesta = Manejo_Peticiones.cuenta_todas_fechas_y_empresas(texto_xml)
        return jsonify(respuesta)
    elif date == "all" and empresa != "all":
        respuesta = Manejo_Peticiones.cuenta_todas_fechas_y_una_empresa(texto_xml, empresa)
        return jsonify(respuesta)
    # print("La empresa: ", empresa)
    # print("La fecha: ", date)
    # print("el xml es: ", texto_xml)

    return "hola"


if __name__ == '__main__':
    app.run(debug=True)
