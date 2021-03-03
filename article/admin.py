from django.contrib import admin
#236. derste Comment modeli de dahil edildi
from .models import Article, Comment #oluşturduğumuz model import edildi.

# Register your models here.

#202. derste bunun yerine dekorator kullanıldı
# admin.site.register(Article)
#Bu class içi class ve dekorator yapısı ile 
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    #article admin sayfasında tabloda makalelerin gösterilecek alanları
    list_display = ["title", "author", "created_date"]
    #gösterilek alanlarda o makalenin düzenleme sayfasına link ekleme
    list_display_links = ["title", "created_date"]
    #article admin sayfasında liste içine yazılan alanlarda arama kutusu oluşturma
    search_fields = ["title"]
    #article admin sayfasında liste içine verilen alana göre süzgeç oluşturma
    list_filter = ["created_date", "author"]
    #class Meta bir kalıp bunu başka bir isimle oluşturamıyoruz.
    class Meta:
        #ArticleAdmin ile Article bağlamak için
        model = Article


#comment modeli olduğu gibi admin panelde göstereceğimiz için class a bağlamamıza gerek yok
#admin.site.register(Comment)
#kayıt işlemini tamamladık şimdi veritabanında modele bağlı tablomuzu oluşturmamız gerekiyor. makemigrations / migrate


#comment modeli admin panelde Comment.objects(1) gibi yerine seçtiğimiz alanlar ve bu alanlara bağlantı vererek gösteriyoruz
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["article","comment_content", "comment_author", "comment_email", "comment_date"]
    list_display_links = ["article", "comment_content"]
    class Meta:
        model = Comment