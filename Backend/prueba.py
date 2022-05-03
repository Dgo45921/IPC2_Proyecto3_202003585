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

cuenta_todas_fechas_y_una_empresa(texto, "ÚmG")
