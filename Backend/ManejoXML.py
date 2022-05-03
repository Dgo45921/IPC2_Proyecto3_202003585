from xml.dom import minidom
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
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
    lista_mensajes.clear()

    raiz = ET.fromstring(texto)
    # print(str(raiz.tag))

    # encontrando palabras positivas
    positivos = raiz.find("./diccionario/sentimientos_positivos")
    for palabra in positivos.findall("./palabra"):
        if palabra.text not in palabras_positivas:
            palabras_positivas.append(palabra.text)
        # print(palabra.text)

    # encontrando palabras negativas

    negativos = raiz.find("./diccionario/sentimientos_negativos")
    for palabra in negativos.findall("./palabra"):
        if palabra.text not in palabras_negativas:
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
    # print("aca leyendo mensajes")
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


def analizar_prueba(texto):
    raiz = ET.fromstring(texto)
    mensaje = raiz.text
    data_lugar = re.search(r"(Lugar y fecha:)(\s)*(\w+)(\s)*[,]", mensaje).group()
    data_usuario = re.search(r"(Usuario):(\s)*([^\s]+)", mensaje).group()
    fecha = re.search(r"(\d{2})[\/](\d{2})[\/](\d{4})", mensaje).group()
    hora = re.search(r"(\d{2}:\d{2})", mensaje).group()
    data_red_social = re.search(r"(Red social):(\s)*([^\s]+)", mensaje).group()
    mensaje.replace(data_lugar, "")
    mensaje.replace(data_usuario, "")
    mensaje.replace(fecha, "")
    mensaje.replace(data_red_social, "")
    # mensaje.replace("\n", "")
    lugar = data_lugar.split(":")[1]
    usuario = data_usuario.split(":")[1]
    red_social = data_red_social.split(":")[1]
    nuevo_mensaje = Mensaje(lugar, fecha, hora, usuario, red_social, mensaje)
    respuesta = analizar_mensaje_prueba(nuevo_mensaje)
    return respuesta


def analizar_mensaje_prueba(objeto_mensaje):
    empresas_leidas = []
    raiz = Element("respuesta")
    fecha = SubElement(raiz, "fecha")
    fecha.text = objeto_mensaje.fecha
    red_social = SubElement(raiz, "red_social")
    red_social.text = objeto_mensaje.red_social
    usuario = SubElement(raiz, "usuario")
    usuario.text = objeto_mensaje.autor
    empresas = SubElement(raiz, "empresas")
    for empresa in lista_empresas:
        if empresa.nombre not in empresas_leidas:
            u = unidecode(empresa.nombre, "utf-8").lower()
            u2 = unidecode(objeto_mensaje.texto, "utf-8").lower()
            if u in u2:
                tag_empresa = SubElement(empresas, "empresa", {"nombre": empresa.nombre})
                for servicio in empresa.servicios:
                    alias_servicio = servicio.alias
                    for i in range(len(alias_servicio)):
                        alias_servicio[i] = unidecode(alias_servicio[i], "utf-8").lower()
                    name_servicio = unidecode(servicio.nombre, "utf-8").lower()
                    if name_servicio in u2 or check_word_in_string(u2, alias_servicio):
                        tag_servicio = SubElement(tag_empresa, "servicio")
                        tag_servicio.text = servicio.nombre

    contadores_prueba = genera_contadores_prueba(objeto_mensaje)
    total_palabras = contadores_prueba[0]
    tag_positivas = SubElement(raiz, "palabras_positivas")
    tag_positivas.text = str(contadores_prueba[1])
    tag_negativas = SubElement(raiz, "palabras_negativas")
    tag_negativas.text = str(contadores_prueba[2])
    tag_sentimiento_positivo = SubElement(raiz, "sentimiento_positivo")
    tag_sentimiento_positivo.text = str((contadores_prueba[1] / total_palabras) * 100) + " %"
    tag_sentimiento_negativo = SubElement(raiz, "sentimiento_negativo")
    tag_sentimiento_negativo.text = str((contadores_prueba[2] / total_palabras) * 100) + " %"
    tag_sentimiento_analizado = SubElement(raiz, "sentimiento_analizado")
    if contadores_prueba[1] > contadores_prueba[2]:
        tag_sentimiento_analizado.text = "positivo"
    elif contadores_prueba[1] < contadores_prueba[2]:
        tag_sentimiento_analizado.text = "negativo"
    else:
        tag_sentimiento_analizado.text = "neutro"

    return prettify(raiz)


def genera_contadores_prueba(mensaje):
    contadores = []
    contador_positivas = 0
    contador_negativas = 0
    for positivo in palabras_positivas:
        u = unidecode(positivo, "utf-8").lower()
        u2 = unidecode(mensaje.texto, "utf-8").lower()
        if u in u2:
            contador_positivas += 1

    for negativo in palabras_negativas:
        u = unidecode(negativo, "utf-8").lower()
        u2 = unidecode(mensaje.texto, "utf-8").lower()
        if u in u2:
            contador_negativas += 1

    total_palabras = contador_positivas + contador_negativas
    contadores.append(total_palabras)
    contadores.append(contador_positivas)
    contadores.append(contador_negativas)
    return contadores


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
        # lista_texto_mensajes[i] = lista_texto_mensajes[i].replace("\n", "")
        lugar = data_lugar.split(":")[1]
        usuario = data_usuario.split(":")[1]
        red_social = data_red_social.split(":")[1]
        nuevo_mensaje = Mensaje(lugar, fecha, hora, usuario, red_social, lista_texto_mensajes[i])
        lista_mensajes.append(nuevo_mensaje)

    return crear_xml()


def crear_xml():
    fechas_leidas = []
    empresas_leidas = []
    raiz = Element("lista_respuestas")
    for mensaje in lista_mensajes:
        if mensaje.fecha not in fechas_leidas:
            fechas_leidas.append(mensaje.fecha)
            respuesta = SubElement(raiz, "respuesta")
            fecha = SubElement(respuesta, "fecha")
            fecha.text = mensaje.fecha
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
    texto_actual = ET.tostring(raiz)
    # print(prettify(raiz))
    # print(type(texto_actual))
    # print(texto_actual)
    raiz = ET.fromstring(texto_actual)
    # print(raiz.tag)
    for respuesta in raiz.findall("./respuesta"):
        fecha = respuesta.find("./fecha")
        analisis = respuesta.find("./analisis")
        for empresa in lista_empresas:
            empresas_leidas.append(empresa.nombre)
            lista_contadores_empresa = calcular_totales_empresa(fecha.text, empresa.nombre)
            tag_empresa = SubElement(analisis, "empresa", {"nombre": empresa.nombre})
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
                lista_contadores_servicio = calcular_totales_servicio(fecha.text, empresa.nombre, servicio.nombre,
                                                                      servicio.alias)
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
                if empresa_en_mensaje and servicio_en_mensaje:
                    contador_mensajes_positivos += 1
            elif contador_palabras_positivas < contador_palabras_negativas:
                if empresa_en_mensaje and servicio_en_mensaje:
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
