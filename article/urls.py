from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "article"

urlpatterns = [
    path("dashboard/", views.dashboard, name = "dashboard"),
    path("addarticle/", views.addarticle, name = "addarticle"),
    path("article/<int:id>", views.detail, name = "detail"),
    path("update/<int:id>", views.updatearticle, name = "update"),
    path("delete/<int:id>", views.deletearticle, name = "delete"),
    path("comment/<int:id>", views.addcomment, name = "comment"),
    #burada linkin sanki index gibi boş olmasının sebebi blog urls içerisinde articles ı dahil etmemiş olmamız. buradaki boşluk domin/articles şeklinde dolduruluyor olacak.
    path("", views.articles, name = "articles"),
]