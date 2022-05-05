import json

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
    dato = request.data.decode("unicode_escape")
    texto_xml = ManejoXML.analizar(dato)
    return texto_xml


@app.route('/procesarxml_prueba', methods=["POST"])
def procesar_xml_prueba():
    dato = request.data.decode("unicode_escape")
    resultado = ManejoXML.analizar_prueba(dato)
    # print(resultado)
    return resultado


@app.route('/resumen_fecha', methods=["POST"])
def generar_resumen_fecha():
    date = request.json["fecha"]
    print(date)
    empresa = request.json["empresa"]
    texto_xml = ManejoXML.xml_almacenado
    if date == "all" and empresa == "all":
        respuesta = Manejo_Peticiones.cuenta_todas_fechas_y_empresas(texto_xml)
        respuesta["fecha"] = "todas"
        respuesta["empresa"] = "todas"
        return jsonify(respuesta)
    elif date == "all" and empresa != "all":
        respuesta = Manejo_Peticiones.cuenta_todas_fechas_y_una_empresa(texto_xml, empresa)
        respuesta["fecha"] = "todas"
        respuesta["empresa"] = empresa
        return jsonify(respuesta)
    elif date != "all" and empresa == "all":
        respuesta = Manejo_Peticiones.cuenta_fecha_especifica_y_todas_empresas(texto_xml, date)
        respuesta["fecha"] = date
        respuesta["empresa"] = "todas"
        return jsonify(respuesta)
    elif date != "all" and empresa != "all":
        respuesta = Manejo_Peticiones.fecha_especifica_y_empresa_especifica(texto_xml, date, empresa)
        respuesta["fecha"] = date
        respuesta["empresa"] = empresa
        return jsonify(respuesta)


@app.route('/resumen_rango_fechas', methods=["POST"])
def generar_resumen_rango_fechas():
    fecha_inicio = request.json["fecha_inicio"]
    fecha_final = request.json["fecha_final"]
    empresa = request.json["empresa"]
    xml = ManejoXML.xml_almacenado
    # print(fecha_inicio, fecha_final, empresa)
    if empresa == "all":
        respuesta = Manejo_Peticiones.resumen_rango_todas_las_empresas(fecha_inicio, fecha_final, xml)
        return jsonify(respuesta)
    else:
        respuesta = Manejo_Peticiones.resumen_rango_empresa_especifica(fecha_inicio, fecha_final, xml, empresa)
        print(json.dumps(respuesta))
        return jsonify(respuesta)


@app.route('/get_xml', methods=["GET"])
def obtiene_datos():
    return ManejoXML.xml_almacenado


@app.route('/reset', methods=["DELETE"])
def resetear_datos():
    ManejoXML.xml_almacenado = ""
    ManejoXML.palabras_negativas.clear()
    ManejoXML.palabras_positivas.clear()
    return "base de datos limpia"


if __name__ == '__main__':
    app.run(debug=True)
