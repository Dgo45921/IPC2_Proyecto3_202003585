import json
import xml.etree.ElementTree as ET
from flask import jsonify
from unidecode import unidecode


lista_empresas_fecha = []
lista_respuestas_fecha = []


def resumen_rango_todas_las_empresas(fecha_inicial, fecha_final, texto_xml):
    lista_empresas_fecha.clear()
    lista_respuestas_fecha.clear()
    contador_total = 0
    contador_positivas = 0
    contador_negativas = 0
    contador_neutras = 0
    raiz = ET.fromstring(texto_xml)
    fecha_inicial = crear_tupla_fecha(fecha_inicial)
    fecha_final = crear_tupla_fecha(fecha_final)

    for respuesta in raiz.findall("./respuesta"):
        lista_empresas_actuales = []
        fecha_actual = respuesta.find("./fecha").text.replace(" ", "")
        fecha_actual2 = respuesta.find("./fecha").text.replace(" ", "")
        fecha_actual2 = crear_tupla_fecha(fecha_actual2)
        if fecha_final >= fecha_actual2 >= fecha_inicial:
            for empresa in respuesta.findall("./analisis/empresa"):
                diccionario_empresa = {
                    "name_empresa": empresa.get("nombre"),
                    "total": int(empresa.find("./mensajes/total").text),
                    "positivos": int(empresa.find("./mensajes/positivos").text),
                    "negativos": int(empresa.find("./mensajes/negativos").text),
                    "neutros": int(empresa.find("./mensajes/neutros").text)
                }
                lista_empresas_actuales.append(diccionario_empresa)
            diccionario_respuesta = {
                "fecha": fecha_actual,
                "empresas": lista_empresas_actuales
            }
            lista_respuestas_fecha.append(diccionario_respuesta)
    return json.dumps(lista_respuestas_fecha, indent=4)


def crear_tupla_fecha(fecha):
    datos_fecha = fecha.split("/")
    tupla = (int(datos_fecha[0]), int(datos_fecha[1]), int(datos_fecha[2]))
    return tupla


texto = """<?xml version="1.0" ?>
<lista_respuestas>
  <respuesta>
    <fecha>01/04/2022</fecha>
    <mensajes>
      <total>2</total>
      <positivos>1</positivos>
      <negativos>1</negativos>
      <neutros>0</neutros>
    </mensajes>
    <analisis>
      <empresa nombre="USAC">
        <mensajes>
          <total>2</total>
          <positivos>1</positivos>
          <negativos>1</negativos>
          <neutros>0</neutros>
        </mensajes>
        <servicios>
          <servicio nombre="inscripción">
            <mensajes>
              <total>1</total>
              <positivos>1</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="asignación">
            <mensajes>
              <total>1</total>
              <positivos>0</positivos>
              <negativos>1</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="graduación">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
        </servicios>
      </empresa>
      <empresa nombre="UMG">
        <mensajes>
          <total>0</total>
          <positivos>0</positivos>
          <negativos>0</negativos>
          <neutros>0</neutros>
        </mensajes>
        <servicios>
          <servicio nombre="Clases">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="pagos">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="graduación">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
        </servicios>
      </empresa>
    </analisis>
  </respuesta>
  <respuesta>
    <fecha>02/04/2022</fecha>
    <mensajes>
      <total>1</total>
      <positivos>0</positivos>
      <negativos>0</negativos>
      <neutros>1</neutros>
    </mensajes>
    <analisis>
      <empresa nombre="USAC">
        <mensajes>
          <total>1</total>
          <positivos>0</positivos>
          <negativos>0</negativos>
          <neutros>1</neutros>
        </mensajes>
        <servicios>
          <servicio nombre="inscripción">
            <mensajes>
              <total>1</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>1</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="asignación">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="graduación">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
        </servicios>
      </empresa>
      <empresa nombre="UMG">
        <mensajes>
          <total>0</total>
          <positivos>0</positivos>
          <negativos>0</negativos>
          <neutros>0</neutros>
        </mensajes>
        <servicios>
          <servicio nombre="Clases">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="pagos">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="graduación">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
        </servicios>
      </empresa>
    </analisis>
  </respuesta>
  <respuesta>
    <fecha>03/04/2022</fecha>
    <mensajes>
      <total>1</total>
      <positivos>0</positivos>
      <negativos>0</negativos>
      <neutros>1</neutros>
    </mensajes>
    <analisis>
      <empresa nombre="USAC">
        <mensajes>
          <total>0</total>
          <positivos>0</positivos>
          <negativos>0</negativos>
          <neutros>0</neutros>
        </mensajes>
        <servicios>
          <servicio nombre="inscripción">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="asignación">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="graduación">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
        </servicios>
      </empresa>
      <empresa nombre="UMG">
        <mensajes>
          <total>1</total>
          <positivos>0</positivos>
          <negativos>0</negativos>
          <neutros>1</neutros>
        </mensajes>
        <servicios>
          <servicio nombre="Clases">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="pagos">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
          <servicio nombre="graduación">
            <mensajes>
              <total>0</total>
              <positivos>0</positivos>
              <negativos>0</negativos>
              <neutros>0</neutros>
            </mensajes>
          </servicio>
        </servicios>
      </empresa>
    </analisis>
  </respuesta>
</lista_respuestas>
"""

resumen_rango_todas_las_empresas("01/04/2022", "02/04/2022", texto)
