from django import forms
#Django dokümanda anlatıldıkğ gibi daha önceden hazırladığımız Article Model sınıfını buraya dahil ediyoruz
from .models import Article

#forms.Formdan farklı olarak Django doc tan models den form hazırlama yöntemi kullanıldı
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        #daha önce oluşturduğumuz Article Modelinde author, title, content ve created_alanlarını oluşturmuştuk ancak bu sayfada sadece input alanı olarak  title/content kullanacağız
        # 227. derste dosya yükleme alanı için "article_image" eklendi
        fields = ["title", "content", "article_image"]