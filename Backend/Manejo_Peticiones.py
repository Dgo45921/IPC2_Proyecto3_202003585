import xml.etree.ElementTree as ET
from unidecode import unidecode
import json

lista_empresas_fecha = []
lista_respuestas_fecha = []


def cuenta_todas_fechas_y_empresas(texto):
    contador_total = 0
    contador_positivas = 0
    contador_negativas = 0
    contador_neutras = 0
    raiz = ET.fromstring(texto)
    for respuesta in raiz.findall("./respuesta"):
        contador_total += int(respuesta.find("./mensajes/total").text)
        contador_positivas += int(respuesta.find("./mensajes/positivos").text)
        contador_negativas += int(respuesta.find("./mensajes/negativos").text)
        contador_neutras += int(respuesta.find("./mensajes/neutros").text)

    diccionario = {"total": contador_total, "positivas": contador_positivas, "negativas": contador_negativas,
                   "neutras": contador_neutras}
    return diccionario


def cuenta_todas_fechas_y_una_empresa(texto, name_empresa):
    contador_total = 0
    contador_positivas = 0
    contador_negativas = 0
    contador_neutras = 0
    name_empresa2 = unidecode(name_empresa, "utf-8").lower().replace(" ", "")
    raiz = ET.fromstring(texto)
    for respuesta in raiz.findall("./respuesta"):
        empresas = respuesta.findall("./analisis/empresa")
        for empresa in empresas:
            empresa2 = unidecode(empresa.get("nombre"), "utf-8").lower().replace(" ", "")
            if empresa2 == name_empresa2:
                contador_total += int(empresa.find("./mensajes/total").text)
                contador_positivas += int(empresa.find("./mensajes/positivos").text)
                contador_negativas += int(empresa.find("./mensajes/negativos").text)
                contador_neutras += int(empresa.find("./mensajes/neutros").text)

    diccionario = {"total": contador_total, "positivas": contador_positivas, "negativas": contador_negativas,
                   "neutras": contador_neutras}
    return diccionario


def cuenta_fecha_especifica_y_todas_empresas(texto, fecha):
    contador_total = 0
    contador_positivas = 0
    contador_negativas = 0
    contador_neutras = 0
    raiz = ET.fromstring(texto)
    for respuesta in raiz.findall("./respuesta"):
        fecha_leida = respuesta.find("./fecha").text
        if fecha_leida == fecha:
            contador_total += int(respuesta.find("./mensajes/total").text)
            contador_positivas += int(respuesta.find("./mensajes/positivos").text)
            contador_negativas += int(respuesta.find("./mensajes/negativos").text)
            contador_neutras += int(respuesta.find("./mensajes/neutros").text)
    diccionario = {"total": contador_total, "positivas": contador_positivas, "negativas": contador_negativas,
                   "neutras": contador_neutras}
    return diccionario


def fecha_especifica_y_empresa_especifica(texto, fecha, name_empresa):
    contador_total = 0
    contador_positivas = 0
    contador_negativas = 0
    contador_neutras = 0
    name_empresa2 = unidecode(name_empresa, "utf-8").lower().replace(" ", "")
    raiz = ET.fromstring(texto)
    for respuesta in raiz.findall("./respuesta"):
        fecha_leida = respuesta.find("./fecha").text
        if fecha_leida == fecha:
            empresas = respuesta.findall("./analisis/empresa")
            for empresa in empresas:
                empresa2 = unidecode(empresa.get("nombre"), "utf-8").lower().replace(" ", "")
                if empresa2 == name_empresa2:
                    contador_total += int(empresa.find("./mensajes/total").text)
                    contador_positivas += int(empresa.find("./mensajes/positivos").text)
                    contador_negativas += int(empresa.find("./mensajes/negativos").text)
                    contador_neutras += int(empresa.find("./mensajes/neutros").text)
    diccionario = {"total": contador_total, "positivas": contador_positivas, "negativas": contador_negativas,
                   "neutras": contador_neutras}
    return diccionario


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
