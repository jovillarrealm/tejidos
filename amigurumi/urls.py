from django.urls import path

from .views import HomeView, CreatePatronView, CatalogoView, PatronView


urlpatterns = [
    path("", HomeView.as_view(), name="home"), 
    path("crear/", CreatePatronView.as_view(), name="cpatron"), 
    path("catalogo/", CatalogoView.as_view(), name="catalogo"), 
    path("catalogo/<int:id>/", PatronView.as_view(), name="mostrar"), 
]
