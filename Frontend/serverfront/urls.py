"""serverfront URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sitioweb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('obtienedata/', views.obtienedata),
    path('mensaje_prueba/', views.mensaje_prueba),
    path('obtienedataprueba/', views.obtiene_data_mensaje_prueba),
    path('obtieneultimoregistro/', views.obtiene_ultimo_registro),
    path('limpiarbase/', views.limpia_base),
    path('resumen_fecha/', views.resumen_fecha),
    path('resumen_rango_fechas/', views.info_resumen_rango_fechas),
    path('info_resumen_fecha/', views.info_resumen_fecha),
    path('info_resumen_rango_fecha/', views.resumen_rango_fecha)
]
