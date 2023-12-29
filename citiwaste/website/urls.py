from django.contrib import admin
from django.urls import path
from website import views


urlpatterns = [
    path("", views.homepage, name = "homepage"),
    path("about/", views.about, name = "about"),
    path("contact/", views.contact, name = "contact"),
    
]
