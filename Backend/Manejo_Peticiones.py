import xml.etree.ElementTree as ET
from unidecode import unidecode


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
    raiz = ET.fromstring(texto)
    for respuesta in raiz.findall("./respuesta"):
        empresa = respuesta.find("./analisis/empresa").get("nombre")
        empresa = unidecode(empresa, "utf-8").lower().replace(" ", "")
        name_empresa2 = unidecode(name_empresa, "utf-8").lower().replace(" ", "")
        if empresa == name_empresa2:
            contador_total += int(respuesta.find("./analisis/empresa/mensajes/total").text)
            contador_positivas += int(respuesta.find("./analisis/empresa/mensajes/positivos").text)
            contador_negativas += int(respuesta.find("./analisis/empresa/mensajes/negativos").text)
            contador_neutras += int(respuesta.find("./analisis/empresa/mensajes/neutros").text)

    diccionario = {"total": contador_total, "positivas": contador_positivas, "negativas": contador_negativas,
                   "neutras": contador_neutras}
    return diccionario
