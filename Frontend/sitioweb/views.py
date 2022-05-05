import json
from unidecode import unidecode
from django.shortcuts import render, redirect
from .models import Respuesta
import requests, datetime


# Create your views here.
def home(request):
    return render(request, 'sitioweb/index.html', {})


def mensaje_prueba(request):
    return render(request, 'sitioweb/mensaje_prueba.html')


def resumen_fecha(request):
    return render(request, 'sitioweb/resumen_fecha.html')


def resumen_rango_fecha(request):
    return render(request, 'sitioweb/resumen_rango_fechas.html')


def obtienedata(request):
    xml_recibido = request.POST['input']
    headers = {'Content-Type': 'application/xml; charset=utf-8'}
    respuesta = requests.post("http://127.0.0.1:5000/procesarxml", data=xml_recibido, headers=headers)
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
    name = "respuesta_" + dt_string
    Respuesta.objects.create(texto=respuesta.text, name=name)
    return render(request, 'sitioweb/index.html', {"input": xml_recibido, "output": respuesta.text})


def obtiene_data_mensaje_prueba(request):
    xml_recibido = request.POST['input']
    headers = {'Content-Type': 'application/xml; charset=utf-8'}
    respuesta = requests.post("http://127.0.0.1:5000/procesarxml_prueba", data=xml_recibido, headers=headers)
    return render(request, 'sitioweb/mensaje_prueba.html', {"input": xml_recibido, "output": respuesta.text})


def obtiene_ultimo_registro(request):
    texto = requests.get("http://127.0.0.1:5000/get_xml").text
    # print(texto)
    return render(request, 'sitioweb/index.html', {"output": texto})


def limpia_base(request):
    print("borrando base")
    Respuesta.objects.all().delete()
    requests.delete("http://127.0.0.1:5000/reset")
    return render(request, 'sitioweb/index.html')


def info_resumen_fecha(request):
    fecha = request.POST.get('date_selector', "all")
    name_empresa = request.POST.get('campo_empresa', "all")

    if fecha != "all":
        datos_fecha = fecha.split("-")
        fecha = datos_fecha[2] + "/" + datos_fecha[1] + "/" + datos_fecha[0]

    info = {"empresa": name_empresa, "fecha": fecha}

    respuesta = requests.post("http://127.0.0.1:5000/resumen_fecha", json=info)
    total = respuesta.json()["total"]
    positivas = respuesta.json()["positivas"]
    negativas = respuesta.json()["negativas"]
    neutras = respuesta.json()["neutras"]
    date = respuesta.json()["fecha"]
    empresa = respuesta.json()["empresa"]
    print(total, positivas, negativas, neutras)

    return render(request, 'sitioweb/resumen_fecha.html', {"date": date,
                                                           "empresa": empresa,
                                                           "total": total,
                                                           "positivos": positivas,
                                                           "negativos": negativas,
                                                           "neutros": neutras})


def info_resumen_rango_fechas(request):
    name_empresa = request.POST.get('campo_empresa', "all")
    fecha_inicio = request.POST.get('low_date', "none")
    fecha_final = request.POST.get('high_date', "none")
    if fecha_inicio != "none":
        datos_fecha = fecha_inicio.split("-")
        fecha_inicio = datos_fecha[2] + "/" + datos_fecha[1] + "/" + datos_fecha[0]

    if fecha_final != "none":
        datos_fecha = fecha_final.split("-")
        fecha_final = datos_fecha[2] + "/" + datos_fecha[1] + "/" + datos_fecha[0]



    info = {"fecha_inicio": fecha_inicio, "fecha_final": fecha_final,"empresa": name_empresa}
    respuesta = requests.post("http://127.0.0.1:5000/resumen_rango_fechas", json=info)
    print(respuesta.text)
    total = respuesta.json()["total"]
    positivas = respuesta.json()["positivas"]
    negativas = respuesta.json()["negativas"]
    neutras = respuesta.json()["neutras"]
    date = respuesta.json()["date"]
    empresa = respuesta.json()["empresa"]
    return render(request, 'sitioweb/resumen_rango_fechas.html', {"date": date,
                                                           "empresa": empresa,
                                                           "total": total,
                                                           "positivos": positivas,
                                                           "negativos": negativas,
                                                           "neutros": neutras})
