from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Article(models.Model):
    """
    Veritabanında blog yazılarının satırlarını ve hücrelerini tanımlayan model sınıfı
    """
    author = models.ForeignKey("auth.User", on_delete = models.CASCADE, verbose_name= "Yazar")
    title = models.CharField(max_length=50, verbose_name= "Başlık")
    #226. derste ckeditor eklendiği için yoruma alındı
    """ content = models.TextField(verbose_name= "İçerik") """
    #CkEditor alanı
    content = RichTextField(verbose_name="İçerik")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name= "Oluşturma Tarihi")
    article_image = models.FileField(blank=True, null=True, verbose_name="Dosya Yükle")

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Article modelinden oluşturulmuş blog yazılarına bağlanan kullanıcı yorumları modeli
    """
    # foreign key yardımı ile yorumları article lara bağlıyoruz
    # on_delete = models.CASCADE ile de article silinirse yorumların da otomatik olarak silinmesi sağlıyoruz.
    # related_name özelliğini ise article ların ilerde "yorumlarını" alabilmek için article.comments ile yorum tablosunu almayı sağladık
    article = models.ForeignKey(Article, on_delete = models.CASCADE, verbose_name = "Makale", related_name = "comments")
    # yorumu yazan kişi isim bilgileri
    comment_author = models.CharField(max_length = 50, verbose_name = "İsminiz:")
    #yorum email alanı CharField ile hazırlandı ancak widget a models.EmailInput özelliği ve placeholder eklendi
    comment_email = models.EmailField(max_length = 40, verbose_name = "Eposta Adresiniz:")
    comment_content = models.TextField(max_length = 1000, verbose_name = "Yorumunuz:")
    # yorumu gönderme tarihini otomatik olarak eklemesi için auto_now_add=True
    comment_date = models.DateTimeField(auto_now_add = True)
    # alanlar oluşturulduktan sonra admin paneline bu modeli kayıt ediyoruz article/admin.py
    def __str__(self):
        return self.comment_content


