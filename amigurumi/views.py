from django.shortcuts import render, redirect

from django import forms

from django.views import View
from django.views.generic import TemplateView

from django.http import HttpResponseRedirect

from abc import ABC, abstractmethod



# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"

class CreatePatronView(View):
    template_name = "home.html"

class CatalogoView(View):
    template_name = "home.html"















class Contenedor(ABC):
    @abstractmethod
    def agregar(self):
        pass
    
    @abstractmethod
    def remover(self):
        pass