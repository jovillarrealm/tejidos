from django.urls import path


from .views import CreatePatronView, PatronView, CatalogoView, CustomLoginView, RegisterPage, LogoutView
from .views import CreatePatronView, PatronView, CatalogoView, CustomLoginView, RegisterPage, LogoutView, ReporteView
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('register/', RegisterPage, name="register"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView, name="logout"),
    path("", views.home, name="home"),
    path("catalogo/", CatalogoView.as_view(), name="catalogo"), 
    path("crear/", CreatePatronView.as_view(), name="cpatron"), 
    path("catalogo/<int:id>/", PatronView.as_view(), name="mostrar"),     
    path("catalogo/<str:format>/", ReporteView.as_view(), name="reporte"),     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)