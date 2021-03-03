"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#211. derste moduler url kullanımı için include import edildi
from django.urls import path, include
#204. derste index sayfasının hazırlanması işlemleri içerisinde eklendi. index i render eden fonksiyon böylece buraya import edilmiş oldu.
from article import views
# settings ve static importları sadece geliştirme sürecinde olmalılar
#settings ve static dosya yükleme işlemi için dahil edildi.
from django.conf import settings
from django.conf.urls.static import static
""" from django.conf import settings
from django.conf.urls.static import static """

urlpatterns = [
    path('admin/', admin.site.urls),
    #anasayfa/landing page için tırnaklar içerisi boş bırakıldı, eğer / girişmiş olsaydı Django hata verecekti.
    # Flask'taki url_for işlemine benzer bir işlem yapmak için burada name attr. oluşturarak bu işlemi yapabiliyoruz.
    path('', views.index, name = "index"),
    path('about/', views.about, name = "about"),
    #dinamik id yapısını deneme amaçlı oluşturduğumuz sayfa yolu
    path('detail/<int:id>', views.detail, name = "detail"),
    #211. derste modüler url yapısına örnek olarak eklendi.
    path('articles/',include("article.urls")),
    #user/register, user/login, user/logout url lerini bağlayan path
    path("user/", include("user.urls") ),
] 

#Dosya yüklerken MEDIA_URL ve MEDIA_ROOT a erişim için
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)