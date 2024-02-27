from django.urls import path

from .views import HomeView, CreatePatronView, CatalogoView


urlpatterns = [
    path("", HomeView.as_view(), name="home"), 
    path("", CreatePatronView.as_view(), name="cpatron"), 
    path("", CatalogoView.as_view(), name="catalogo"), 
]
