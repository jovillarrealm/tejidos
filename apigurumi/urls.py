from django.urls import path
from .views import PatronListApi

urlpatterns = [
    path('patrons/', PatronListApi.as_view()),
]
