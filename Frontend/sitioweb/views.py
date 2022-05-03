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


def obtienedata(request):
    xml_recibido = request.POST['input']
    diccionario = {"xml": xml_recibido}
    respuesta = requests.post("http://127.0.0.1:5000/procesarxml", json=diccionario)
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
    name = "respuesta_" + dt_string
    Respuesta.objects.create(texto=respuesta.text, name=name)
    return render(request, 'sitioweb/index.html', {"input": xml_recibido, "output": respuesta.text})


def obtiene_data_mensaje_prueba(request):
    xml_recibido = request.POST['input']
    diccionario = {"xml": xml_recibido}
    respuesta = requests.post("http://127.0.0.1:5000/procesarxml_prueba", json=diccionario)
    return render(request, 'sitioweb/mensaje_prueba.html', {"input": xml_recibido, "output": respuesta.text})


def obtiene_ultimo_registro(request):
    texto = Respuesta.objects.last().texto
    print(texto)
    return render(request, 'sitioweb/index.html', {"output": texto})


def limpia_base(request):
    print("borrando base")
    Respuesta.objects.all().delete()
    return render(request, 'sitioweb/index.html')


def info_resumen_fecha(request):
    fecha = request.POST.get('date_selector', "all")
    name_empresa = request.POST.get('campo_empresa', "all")


    print("nombre de la empresa: ", name_empresa)
    print("fecha a buscar: ", fecha)
    return render(request, 'sitioweb/resumen_fecha.html')
