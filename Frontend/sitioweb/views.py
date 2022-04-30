from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests


# Create your views here.
def home(request):
    return render(request, 'sitioweb/index.html', {})


def obtienedata(request):
    # print("hola me han hecho una peticion")
    xml_recibido = request.POST['input']
    # print(xml_recibido)
    diccionario = {"xml": xml_recibido}
    respuesta = requests.post("http://127.0.0.1:5000/procesarxml", json=diccionario)
    print(respuesta.text)
    return render(request, 'sitioweb/index.html', {"input": xml_recibido})
