from django.shortcuts import render, redirect
from .models import Respuesta
import requests, datetime


# Create your views here.
def home(request):
    return render(request, 'sitioweb/index.html', {})


def mensaje_prueba(request):
    return render(request, 'sitioweb/mensaje_prueba.html')


def obtienedata(request):
    # print("hola me han hecho una peticion")
    xml_recibido = request.POST['input']
    # print(xml_recibido)
    diccionario = {"xml": xml_recibido}
    respuesta = requests.post("http://127.0.0.1:5000/procesarxml", json=diccionario)
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
    name = "respuesta_" + dt_string
    Respuesta.objects.create(texto=respuesta.text, name=name)
    texto = Respuesta.objects.last().texto
    print(texto)
    return render(request, 'sitioweb/index.html', {"input": xml_recibido, "output": respuesta.text})


def obtiene_data_mensaje_prueba(request):
    xml_recibido = request.POST['input']
    # print(xml_recibido)
    diccionario = {"xml": xml_recibido}
    respuesta = requests.post("http://127.0.0.1:5000/procesarxml_prueba", json=diccionario)
    # print(respuesta.text)
    return render(request, 'sitioweb/mensaje_prueba.html', {"input": xml_recibido, "output": respuesta.text})
