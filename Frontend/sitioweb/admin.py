from django.contrib import admin
from . import models


# Register your models here.
class Info(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(models.Respuesta, Info)
