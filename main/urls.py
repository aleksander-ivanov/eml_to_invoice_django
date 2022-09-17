from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("build/", views.build, name='build'),
    path("about/", views.about, name='about'),
]