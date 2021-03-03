#221. derste fonksiyona redirect import edildi ve kullanıldı
from django.shortcuts import render, HttpResponse,redirect, reverse, get_object_or_404
#HttpResponse 204. derte eklendi. index fonk. hazırlanırken işlemin daha kolay anlaşılabilmesi için tercih edildi. Sayfaya direk fonksiyonu içerisinde yazı gönderebiliyoruz.
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
#221. derste fonksiyona messeges özelliği eklemek için import edildi
from django.contrib import messages
#223. derste veritabanından veri alma işlemi için import edildi
from .models import Article, Comment
from user import views
# Create your views here.
#request değişkeni sayfaya yapılan isteklerin Django tarafından yakalanarak oluşturuluyor.Her view fonksiyonunda mutlaka bulunmalı ve ilk parametre olmalı. GET ya da POST olduğunu bu değişken aracılığı ile anlayacağız.

#anasayfa fonksiyonu
def index(request):
    """Anasayfa yönlendirmesini yapan fonk."""
    # Sayfaya http responce yani içerisindeki kelime yazdırma işlemi için kullanıldı ve kaldırıldık.
    #return HttpResponse("Peh!")
    return render(request, "index.html")

#Hakkımda sayfasının fonksiyonu
def about(request):
    """Hakkımda sayfasının urlsini döndüren fonksiyon"""
    return render(request, "about.html")

""" #deneme amaçlı oluşturulan dinamik id fonksiyonu
def detail(request, id):
    #Veritabanında id int olarak kayıtlı. Sayfaya gönderebilmek için str'ye çevirmek gerekiyor yoksa Django sayfada int / str hatası veriyor.
    return HttpResponse("Deneme: " + str(id)) """

#dashboard fonksiyonu
@login_required(login_url="user:login")
def dashboard(request):
    #online kullanıcının yazılarını veritabanında almamız gerekiyor. Veritabanından sözlük yapısında bilgileri alıyoruz.
    articles = Article.objects.filter(author = request.user).order_by("-created_date")
    context = {"articles": articles,}
    return render(request, "dashboard.html", context)

#blog yazı yazma ekran fonksiyonu
@login_required(login_url="user:login")
def addarticle(request):
    #227. derste dosya yükleme işlemini sağlamak için request.FILES or None eklendi
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        #Bu form model ile ilişkili bir form olduğu için sadece kayıt işlemi yapmak yeterli ancak formumuzda user id olmadığı için yazı kaydet denildiğinde Django hata dönüyor. O yüzden öncelikle veritabanına yazma işlemini beklemeye almamız gerekiyor bu yüzden commit=False ekliyoruz ve form.save() i bir değişkene aktarıyoruz
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Yazınız yayınlandı!")
        return redirect("article:dashboard")
    context = {"form": form}
    return render(request, "addarticle.html", context)

#makalere dinamik url ile yönlendiren fonksiyon
#238. dersle sayfada yorumları gösterir hala getirildi
def detail(request, id):
    #224. derste 404 özelliği için yoruma alındı
    """ article = Article.objects.filter(id = id).first() """
    article = get_object_or_404(Article, id = id)
    #context 238. de yoruma alındı çünkü comments de eklendi
    #context = {"article": article}
    #Comment modelini oluşturduğumuzda related_name olarak comments ismini kullanmıştık burada article değişkenine ekleyerek o makalenin ilişkili olduğu yorumların hepsini alabiliyoruz.
    comments = article.comments.all().order_by("-comment_date")
    #context e comments eklendi
    context = {
        "article": article,
        "comments": comments,
    }
    return render(request, "detail.html", context)

#aktif kullanıcının kendine ait yazıları güncelleye fonksiyon
@login_required(login_url="user:login")
def updatearticle(request, id):
    article = get_object_or_404(Article, id = id)
        #article nesnesi içerisinde tüm bilgiler instance parametresine aktarılıyor ve böylece modelin gerekli alanları doldurularak form nesnesine işleniyor
    if request.user.id == article.author_id:
        form = ArticleForm(request.POST or None, request.FILES or None, instance= article)
        if form.is_valid():
            article = form.save(commit = False)
            article.author = request.user
            article.save()
            messages.success(request, "Yazınız güncellendi.")
            return redirect("article:dashboard")
        context = {"form": form}
        return render(request, "update.html", context)
    messages.info(request, "Bu yazı size ait değil!")
    return redirect("index")

#aktif kullanıcının kendine ait yazıları silen fonksiyon
@login_required(login_url="user:login")
def deletearticle(request, id):
    article = get_object_or_404(Article, id = id)
    if request.user.id == article.author_id:
        article.delete()
        messages.success(request, "Yazınız silindi.")
        return redirect("article:dashboard")
    messages.info(request, "Bu yazı size ait değil!")
    return redirect("index")

#Blog yazıları sayfasının fonksiyonu
def articles(request):
    #234. derste arama işlemi için keyword değişkeni ve if bloğu eklendi
    #request.GET "get" requesti yakalarken .get ise bunun içindeki name alanının içeriğini almak için kullanıldı
    keyword = request.GET.get("keyword")
    #eğer arama işlemi yapılmazsa ya da boş dönerse sorgusu hazırlandı
    if keyword:
        #__contains ile arama işleminin yapılacağı alanın içeriği karşılaştırılarak veritabanından eşleşen yazılar alındı
        articles = Article.objects.filter(title__contains = keyword)
        #yazılar context e bağlantı
        context = {"articles": articles}
        return render(request, "articles.html", context)
    #içinde sözlük bulanan liste nesnesi
    articles = Article.objects.all().order_by("-created_date")
    context = {"articles": articles,}
    return render(request, "articles.html", context)

#yorum gönderme ve veritabanına yazma fonksiyonu
def addcomment(request, id):
    article = get_object_or_404(Article, id = id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_email = request.POST.get("comment_email")
        comment_content = request.POST.get("comment_content")
        new_comment = Comment(comment_author = comment_author, comment_content = comment_content, comment_email = comment_email)
        new_comment.article = article
        new_comment.save()
    # buradaki redirect link yazımı çok iyi bir örnek değil.    
    #return redirect("/articles/article/" + str(id))
    #best-practise için reverse() fonksiyonu
    return redirect(reverse("article:detail", kwargs={"id": id}))