from xml.dom import minidom
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from Empresa import Empresa
from Servicio import Servicio
from Mensaje import Mensaje
import re
from unidecode import unidecode

lista_mensajes = []
lista_empresas = []
lista_texto_mensajes = []
mensajes_positivos = []
mensajes_negativos = []
palabras_negativas = []
palabras_positivas = []


def analizar(texto):
    global lista_texto_mensajes, lista_empresas, mensajes_negativos, mensajes_positivos, palabras_positivas, palabras_negativas, lista_mensajes
    lista_empresas.clear()
    lista_texto_mensajes.clear()
    mensajes_positivos.clear()
    mensajes_negativos.clear()
    palabras_negativas.clear()
    palabras_positivas.clear()
    lista_mensajes.clear()

    raiz = ET.fromstring(texto)
    # print(str(raiz.tag))

    # encontrando palabras positivas
    positivos = raiz.find("./diccionario/sentimientos_positivos")
    for palabra in positivos.findall("./palabra"):
        palabras_positivas.append(palabra.text)
        # print(palabra.text)

    # encontrando palabras negativas

    negativos = raiz.find("./diccionario/sentimientos_negativos")
    for palabra in negativos.findall("./palabra"):
        palabras_negativas.append(palabra.text)
        # print(palabra.text)

    # encontrando las empresas en el xml

    empresas = raiz.find("./diccionario/empresas_analizar")
    for empresa in empresas.findall("./empresa"):
        name_empresa = empresa.find("./nombre").text
        # print("aqui comienza una nueva empresa: ", name_empresa)
        nueva_empresa = Empresa(name_empresa)

        # aca se leen los servicios de una empresa
        for servicio in empresa.findall("./servicio"):
            name_servicio = servicio.get("nombre")
            # print("aqui inicia un servicio de la empresa: ", name_empresa, " el servicio es: ", name_servicio)
            nuevo_servicio = Servicio(name_servicio)
            # aca se lee cada alias para cada servicio
            for alias in servicio.findall("./alias"):
                alias_servicio = alias.text
                # print("y un alias para el servicio: ", name_servicio, " es: ", alias_servicio)
                nuevo_servicio.alias.append(alias_servicio)
            nueva_empresa.servicios.append(nuevo_servicio)
        lista_empresas.append(nueva_empresa)

    # aca se leen los mensajes
    print("aca leyendo mensajes")
    # print(lista_empresas)
    # for i in range(len(lista_empresas)):
    #     print("Empresa")
    #     print(lista_empresas[i].nombre)
    #     for j in range(len(lista_empresas[i].servicios)):
    #         print("Servicio de la empresa: ", lista_empresas[i].nombre)
    #         print("nombre del servicio: ", lista_empresas[i].servicios[j].nombre)
    #         for k in range(len(lista_empresas[i].servicios[j].alias)):
    #             print("alias del servicio: ", lista_empresas[i].servicios[j].nombre)
    #             print(lista_empresas[i].servicios[j].alias[k])

    mensajes = raiz.find("./lista_mensajes")
    for mensaje in mensajes.findall("./mensaje"):
        texto_mensaje = mensaje.text
        # print(texto_mensaje)
        lista_texto_mensajes.append(texto_mensaje)
    xml_texto = analizar_mensajes()
    return xml_texto


def analizar_mensajes():
    for i in range(len(lista_texto_mensajes)):
        data_lugar = re.search(r"(Lugar y fecha:)(\s)*(\w+)(\s)*[,]", lista_texto_mensajes[i]).group()
        data_usuario = re.search(r"(Usuario):(\s)*([^\s]+)", lista_texto_mensajes[i]).group()
        fecha = re.search(r"(\d{2})[\/](\d{2})[\/](\d{4})", lista_texto_mensajes[i]).group()
        hora = re.search(r"(\d{2}:\d{2})", lista_texto_mensajes[i]).group()
        data_red_social = re.search(r"(Red social):(\s)*([^\s]+)", lista_texto_mensajes[i]).group()
        lista_texto_mensajes[i] = lista_texto_mensajes[i].replace(data_lugar, "")
        lista_texto_mensajes[i] = lista_texto_mensajes[i].replace(data_usuario, "")
        lista_texto_mensajes[i] = lista_texto_mensajes[i].replace(fecha, "")
        lista_texto_mensajes[i] = lista_texto_mensajes[i].replace(data_red_social, "")
        lista_texto_mensajes[i] = lista_texto_mensajes[i].replace("\n", "")
        lugar = data_lugar.split(":")[1]
        usuario = data_usuario.split(":")[1]
        red_social = data_red_social.split(":")[1]
        nuevo_mensaje = Mensaje(lugar, fecha, hora, usuario, red_social, lista_texto_mensajes[i])
        lista_mensajes.append(nuevo_mensaje)

    return crear_xml()


def crear_xml():
    fecha_actual = ""
    analisis_x = None
    fechas_leidas = []
    empresas_leidas = []
    raiz = Element("lista_respuestas")
    for mensaje in lista_mensajes:
        if mensaje.fecha not in fechas_leidas:
            fechas_leidas.append(mensaje.fecha)
            respuesta = SubElement(raiz, "respuesta")
            fecha = SubElement(respuesta, "fecha")
            fecha.text = mensaje.fecha
            fecha_actual = fecha.text
            lista_contadores = calcular_totales_fecha(mensaje.fecha)
            mensajes = SubElement(respuesta, "mensajes")
            total = SubElement(mensajes, "total")
            total.text = str(lista_contadores[0])
            positivos = SubElement(mensajes, "positivos")
            positivos.text = str(lista_contadores[1])
            negativos = SubElement(mensajes, "negativos")
            negativos.text = str(lista_contadores[2])
            neutros = SubElement(mensajes, "neutros")
            neutros.text = str(lista_contadores[3])
            analisis = SubElement(respuesta, "analisis")
            analisis_x = analisis
    print(prettify(raiz))
    for empresa in lista_empresas:
        if empresa.nombre not in empresas_leidas:
            empresas_leidas.append(empresa.nombre)
            lista_contadores_empresa = calcular_totales_empresa(fecha_actual, empresa.nombre)
            tag_empresa = SubElement(analisis_x, "empresa", {"nombre": empresa.nombre})
            mensajes_empresa = SubElement(tag_empresa, "mensajes")
            total_empresa = SubElement(mensajes_empresa, "total")
            total_empresa.text = str(lista_contadores_empresa[0])
            positivos_empresa = SubElement(mensajes_empresa, "positivos")
            positivos_empresa.text = str(lista_contadores_empresa[1])
            negativos_empresa = SubElement(mensajes_empresa, "negativos")
            negativos_empresa.text = str(lista_contadores_empresa[2])
            neutros_empresa = SubElement(mensajes_empresa, "neutros")
            neutros_empresa.text = str(lista_contadores_empresa[3])
            servicios = SubElement(tag_empresa, "servicios")
            for servicio in empresa.servicios:
                lista_contadores_servicio = calcular_totales_servicio(fecha_actual, empresa.nombre, servicio.nombre, servicio.alias)
                tag_servicio = SubElement(servicios, "servicio", {"nombre": servicio.nombre})
                tag_mensajes_servicio = SubElement(tag_servicio, "mensajes")
                total_servicio = SubElement(tag_mensajes_servicio, "total")
                total_servicio.text = str(lista_contadores_servicio[0])
                positivos_servicio = SubElement(tag_mensajes_servicio, "positivos")
                positivos_servicio.text = str(lista_contadores_servicio[1])
                negativos_servicio = SubElement(tag_mensajes_servicio, "negativos")
                negativos_servicio.text = str(lista_contadores_servicio[2])
                neutros_servicio = SubElement(tag_mensajes_servicio, "neutros")
                neutros_servicio.text = str(lista_contadores_servicio[3])

    return prettify(raiz)


def calcular_totales_fecha(fecha):
    lista_contadores = []
    contador_mensajes_positivos = 0
    contador_mensajes_negativos = 0
    contador_mensajes_neutros = 0

    for mensaje in lista_mensajes:
        contador_palabras_negativas = 0
        contador_palabras_positivas = 0
        if mensaje.fecha == fecha:
            for positivo in palabras_positivas:
                u = unidecode(positivo, "utf-8").lower()
                u2 = unidecode(mensaje.texto, "utf-8").lower()
                if u in u2:
                    contador_palabras_positivas += 1

            for negativo in palabras_negativas:
                u = unidecode(negativo, "utf-8").lower()
                u2 = unidecode(mensaje.texto, "utf-8").lower()
                if u in u2:
                    contador_palabras_negativas += 1

            if contador_palabras_positivas > contador_palabras_negativas:
                contador_mensajes_positivos += 1
            elif contador_palabras_positivas < contador_palabras_negativas:
                contador_mensajes_negativos += 1
            else:
                contador_mensajes_neutros += 1
    total = contador_mensajes_negativos + contador_mensajes_positivos + contador_mensajes_neutros
    lista_contadores.append(total)
    lista_contadores.append(contador_mensajes_positivos)
    lista_contadores.append(contador_mensajes_negativos)
    lista_contadores.append(contador_mensajes_neutros)
    return lista_contadores


def calcular_totales_empresa(fecha, empresa):
    lista_contadores = []
    contador_mensajes_positivos = 0
    contador_mensajes_negativos = 0
    contador_mensajes_neutros = 0

    for mensaje in lista_mensajes:
        empresa_en_mensaje = False
        contador_palabras_negativas = 0
        contador_palabras_positivas = 0
        if mensaje.fecha == fecha:
            for positivo in palabras_positivas:
                u = unidecode(positivo, "utf-8").lower()
                u2 = unidecode(mensaje.texto, "utf-8").lower()
                u3 = unidecode(empresa, "utf-8").lower()
                if u in u2 and u3 in u2:
                    empresa_en_mensaje = True
                    contador_palabras_positivas += 1

            for negativo in palabras_negativas:
                u = unidecode(negativo, "utf-8").lower()
                u2 = unidecode(mensaje.texto, "utf-8").lower()
                u3 = unidecode(empresa, "utf-8").lower()
                if u in u2 and u3 in u2:
                    empresa_en_mensaje = True
                    contador_palabras_negativas += 1

            if contador_palabras_positivas > contador_palabras_negativas:
                contador_mensajes_positivos += 1
            elif contador_palabras_positivas < contador_palabras_negativas:
                contador_mensajes_negativos += 1
            else:
                if empresa_en_mensaje:
                    contador_mensajes_neutros += 1
    total = contador_mensajes_negativos + contador_mensajes_positivos + contador_mensajes_neutros
    lista_contadores.append(total)
    lista_contadores.append(contador_mensajes_positivos)
    lista_contadores.append(contador_mensajes_negativos)
    lista_contadores.append(contador_mensajes_neutros)
    return lista_contadores


def calcular_totales_servicio(fecha, empresa, servicio, alias_servicio):
    lista_contadores = []
    contador_mensajes_positivos = 0
    contador_mensajes_negativos = 0
    contador_mensajes_neutros = 0

    for i in range(len(alias_servicio)):
        alias_servicio[i] = unidecode(alias_servicio[i], "utf-8").lower()

    for mensaje in lista_mensajes:
        empresa_en_mensaje = False
        servicio_en_mensaje = False
        contador_palabras_negativas = 0
        contador_palabras_positivas = 0
        if mensaje.fecha == fecha:
            for positivo in palabras_positivas:
                u = unidecode(positivo, "utf-8").lower()
                u2 = unidecode(mensaje.texto, "utf-8").lower()
                u3 = unidecode(empresa, "utf-8").lower()
                u4 = unidecode(servicio, "utf-8").lower()
                if u in u2 and u3 in u2 and (u4 in u2 or check_word_in_string(u2, alias_servicio)):
                    empresa_en_mensaje = True
                    servicio_en_mensaje = True
                    contador_palabras_positivas += 1

            for negativo in palabras_negativas:
                u = unidecode(negativo, "utf-8").lower()
                u2 = unidecode(mensaje.texto, "utf-8").lower()
                u3 = unidecode(empresa, "utf-8").lower()
                u4 = unidecode(servicio, "utf-8").lower()
                if u in u2 and u3 in u2 and (u4 in u2 or check_word_in_string(u2, alias_servicio)):
                    empresa_en_mensaje = True
                    servicio_en_mensaje = True
                    contador_palabras_negativas += 1

            if contador_palabras_positivas > contador_palabras_negativas:
                contador_mensajes_positivos += 1
            elif contador_palabras_positivas < contador_palabras_negativas:
                contador_mensajes_negativos += 1
            else:
                if empresa_en_mensaje and servicio_en_mensaje:
                    contador_mensajes_neutros += 1
    total = contador_mensajes_negativos + contador_mensajes_positivos + contador_mensajes_neutros
    lista_contadores.append(total)
    lista_contadores.append(contador_mensajes_positivos)
    lista_contadores.append(contador_mensajes_negativos)
    lista_contadores.append(contador_mensajes_neutros)
    return lista_contadores


def check_word_in_string(cadena, lista):
    for i in range(len(lista)):
        if lista[i] in cadena:
            return True
    return False

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
