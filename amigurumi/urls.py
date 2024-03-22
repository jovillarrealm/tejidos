from django.urls import path

from .views import HomeView, CreatePatronView, PatronView, CatalogoView, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('register/', RegisterPage.as_view(), name="register"),
    path('logout/', LogoutView.as_view(next_page='home'), name="logout"),
    path("", HomeView.as_view(), name="home"),
    path("crear/", CreatePatronView.as_view(), name="cpatron"), 
    path("catalogo/", CatalogoView.as_view(), name="catalogo"), 
    path("catalogo/<int:id>/", PatronView.as_view(), name="mostrar"), 
    
]
