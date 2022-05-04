import xml.etree.ElementTree as ET
from unidecode import unidecode
import json
from datetime import date, timedelta



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
    lista_respuestas = []
    fecha_inicial.replace(" ", "")
    fecha_final.replace(" ", "")
    arreglo_fechas = crear_lista_fechas(fecha_inicial, fecha_final)
    raiz = ET.fromstring(texto_xml)
    fecha_inicial2 = crear_tupla_fecha(fecha_inicial)
    fecha_final2 = crear_tupla_fecha(fecha_final)

    for fecha in arreglo_fechas:
        for respuesta in raiz.findall("./respuesta"):
            fecha_actual2 = fecha.replace(" ", "")
            fecha_actual2 = crear_tupla_fecha(fecha_actual2)
            if fecha_final2 >= fecha_actual2 >= fecha_inicial2:
                contador_total = int(respuesta.find("./mensajes/total").text)
                contador_positivas = int(respuesta.find("./mensajes/positivos").text)
                contador_negativas = int(respuesta.find("./mensajes/negativos").text)
                contador_neutras = int(respuesta.find("./mensajes/neutros").text)
                diccionario_contadores = {"total": contador_total, "positivas": contador_positivas,
                                          "negativas": contador_negativas,
                                          "neutras": contador_neutras, "empresa": "all"}

                diccionario_fecha = {"fecha": fecha, "contadores": diccionario_contadores}
        lista_respuestas.append(diccionario_fecha)


    print(json.dumps(lista_respuestas, indent=4))


def resumen_rango_empresa_especifica(fecha_inicial, fecha_final, texto_xml, name_empresa):
    contador_total = 0
    contador_positivas = 0
    contador_negativas = 0
    contador_neutras = 0
    raiz = ET.fromstring(texto_xml)
    fecha_inicial2 = crear_tupla_fecha(fecha_inicial)
    fecha_final2 = crear_tupla_fecha(fecha_final)

    for respuesta in raiz.findall("./respuesta"):
        fecha_actual2 = respuesta.find("./fecha").text.replace(" ", "")
        fecha_actual2 = crear_tupla_fecha(fecha_actual2)
        if fecha_final2 >= fecha_actual2 >= fecha_inicial2:
            for empresa in respuesta.findall("./analisis/empresa"):
                contador_total += int(empresa.find("./mensajes/total").text)
                contador_positivas += int(empresa.find("./mensajes/positivos").text)
                contador_negativas += int(empresa.find("./mensajes/negativos").text)
                contador_neutras += int(empresa.find("./mensajes/neutros").text)

    fecha_inicial += " - " + fecha_final
    diccionario = {
        "date": fecha_inicial,
        "total": contador_total,
        "positivas": contador_positivas,
        "negativas": contador_negativas,
        "neutras": contador_neutras,
        "empresa": "todas"
    }

    return diccionario


def crear_tupla_fecha(fecha):
    datos_fecha = fecha.split("/")
    tupla = (int(datos_fecha[0]), int(datos_fecha[1]), int(datos_fecha[2]))
    return tupla


def crear_lista_fechas(fecha_inicial, fecha_final):
    arreglo = []
    datos_fecha_inicial = fecha_inicial.split("/")
    inicio_fecha = date(year=int(datos_fecha_inicial[2]), day=int(datos_fecha_inicial[0]),
                        month=int(datos_fecha_inicial[1]))

    datos_fecha_final = fecha_final.split("/")
    fin_fecha = date(year=int(datos_fecha_final[2]), day=int(datos_fecha_final[0]),
                        month=int(datos_fecha_final[1]))

    delta = fin_fecha - inicio_fecha
    for i in range(delta.days + 1):
        day = inicio_fecha + timedelta(days=i)
        dia = ""
        mes = ""
        if day.day < 10:
            dia = "0"+str(day.day)
        else:
            dia = str(day.day)

        if day.month < 10:
            mes = "0" + str(day.month)
        else:
            mes = str(day.month)

        anio = str(day.year)
        fecha = dia + "/" + mes + "/" + anio
        arreglo.append(fecha)
    return arreglo

texto = """<?xml version="1.0" ?>
<lista_respuestas>
  <respuesta>
    <fecha>01/05/2022</fecha>
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
    <fecha>02/05/2022</fecha>
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
    <fecha>03/05/2022</fecha>
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

resumen_rango_todas_las_empresas("01/05/2022", "10/05/2022", texto)