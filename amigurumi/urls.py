from django.urls import path

from .views import HomeView, CreatePatronView, PatronView, CatalogoView, CustomLoginView, RegisterPage, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', RegisterPage, name="register"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView, name="logout"),
    path("", HomeView.as_view(), name="home"),
    path("crear/", CreatePatronView.as_view(), name="cpatron"), 
    path("catalogo/", CatalogoView.as_view(), name="catalogo"), 
    path("catalogo/<int:id>/", PatronView.as_view(), name="mostrar"),     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)