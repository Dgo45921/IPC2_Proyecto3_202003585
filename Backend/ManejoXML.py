import xml.etree.ElementTree as ET

lista_mensajes = []
mensajes_positivos = []
mensajes_negativos = []
palabras_negativas = []
palabras_positivas = []


def analizar(texto):
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
        print("aqui comienza una nueva empresa: ", name_empresa)

        # aca se leen los servicios de una empresa
        for servicio in empresa.findall("./servicio"):
            name_servicio = servicio.get("nombre")
            print("aqui inicia un servicio de la empresa: ", name_empresa, " el servicio es: ", name_servicio)
            # aca se lee cada alias para cada servicio
            for alias in servicio.findall("./alias"):
                alias_servicio = alias.text
                print("y un alias para el servicio: ", name_servicio, " es: ", alias_servicio)

    # aca se leen los mensajes
    print("aca leyendo mensajes")
    mensajes = raiz.find("./lista_mensajes")
    for mensaje in mensajes.findall("./mensaje"):
        texto_mensaje = mensaje.text
        print(texto_mensaje)

