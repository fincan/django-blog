#ders 214'te redirect eklendi
from django.shortcuts import render, redirect
#213. derste forms.py içinde form classı yaratıldıktan sonra import edildi.
#216. ders LoginForm dahil edildi
from .forms import RegisterForm, LoginForm
#214. derste user modeli yapıya dahil edildi böylece kayıt formundaki bilgiler model nesnesine aktarıldı
from django.contrib.auth.models import User
#yine ders 214'te kullanıcı başarılı bir şekilde kayıt olduğunda otomatik olarak login olması sağlama için login import edildi
#216. derste kayır formuna kullanıcının girdiği bilgi ile veritabanı bilgilerini karşılaştırıyor. eğer kullanıcı bilgisi varsa değer dönüyor yoksa da "none" değer dönüyor
#218. derste logout işlemi için logout eklendi
from django.contrib.auth import login, authenticate, logout
#flash message benzeri Django mesaj yapısı dahil edildi
from django.contrib import messages

# Create your views here.

""" #kullanıcı kayıt fonksiyonu
    #214. derste form sayfasının hazırlanmasının 1. YOLU
def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid(): #bu noktada RegisterForm()'daki clean() metodu çağrılıyor ve eğer sorgusu True döndürürse form.is_valid sağlanmış oluyor
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            #yeni kullanıcı oluşturulması için ORM veritabanı yapısı kullanıldı
            newuser = User(first_name = first_name, last_name=last_name, username=username, email=email)
            #password şifrelenmesi için ayrıca .set-password ile alındı
            newuser.set_password(password)
            newuser.save() #veritabanına kayıt tamamlandı
            login(request, newuser) #eğer kullanıcıyı kayıt işleminden sonra otomatik olarak login yapmak istiyorsak
            return redirect("index") #daha önce anasayfayı index ismi ile adlandırdığımız için sadece ismini yazmamız yeterli oluyor.
        context = { "form": form}
        return render(request, "register.html", context)
    else:
        form = RegisterForm() #get request olduğu sayfaya sadece formu gönderdiğimiz için burada form nesnesini parametre almamış RegisterForm sınıfından oluşturuyoruz.
        context = { "form": form}
        return render(request, "register.html", context) """

#kullanıcı kayıt formu
#214. Derste anlatılan 2.Yol Daha kısa ve mantıklu
def register(request):
    #Form get request ise None yani boş olarak form nesnesi oluşacak; eğer port request ise form parametreleri alacak böylece request durumunu if kontrolü ile kontrol etmek zorunda kalmıyoruz
    form = RegisterForm(request.POST or None)
    if form.is_valid(): #bu noktada RegisterForm()'daki clean() metodu çağrılıyor ve eğer sorgusu True döndürürse form.is_valid sağlanmış oluyor
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        #yeni kullanıcı oluşturulması için ORM veritabanı yapısı kullanıldı
        newuser = User(first_name = first_name, last_name=last_name, username=username, email=email)
        #password şifrelenmesi için ayrıca .set-password ile alındı
        newuser.set_password(password)
        newuser.save() #veritabanına kayıt tamamlandı
        login(request, newuser) #eğer kullanıcıyı kayıt işleminden sonra otomatik olarak login yapmak istiyorsak
        messages.success(request, "Başarıyla Kayıt Oldunuz!")
        return redirect("index") #daha önce anasayfayı index ismi ile adlandırdığımız için sadece ismini yazmamız yeterli oluyor.
    context = { "form": form}
    return render(request, "register.html", context)


#kullanıcını giriş fonksiyonu
def loginuser(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        #LoginForm'da clean() metodunu tanımlamadık ancak aslında override yapmadık. Yoksa forms.Form içerisinde zaten önceden tanımlanmış clean() metodu mevcut
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        #authenticate fonksiyonu önce veritabanında ilk girilen değişkeni sorgluuor varsa ikinci değişkeni sorguluyor ve değişkenler uyumluysa değer dönüyor değilse "none" değer dönüyor
        user_query = authenticate(username = username, password = password)
        if user_query is None:
            #daha önceki derslerde danger messagesları Django'nun ingo messeage tagine bağlamıştık
            messages.info(request, "Girilen Bilgiler Hatalı!")
            return render(request, "login.html", context)
        messages.success(request,"Başarıyla Giriş Yapıldı!")
        login(request, user_query)
        return redirect("index")
    return render(request,"login.html", context)

#kullanıcını oturum sonlandırma fonksiyonu
def logoutuser(request):
    logout(request)
    messages.success(request, "Oturum Başarıyla Sonlandırıldı!")
    return redirect("index")