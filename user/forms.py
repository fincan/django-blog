from django import forms

#kayıt formu
class RegisterForm(forms.Form):
    """Kullanıcı Kayıt Formu Sınıfı"""
    first_name = forms.CharField(min_length=2, max_length=25, label="İsminiz:")
    last_name = forms.CharField(min_length=2, max_length=25, label="Soyadınız:")
    email = forms.CharField(max_length= 40, min_length = 3, label = "Eposta Adresiniz:", widget=forms.EmailInput(attrs={"placeholder": "ornek@ornek.com"}))
    username = forms.CharField(max_length= 25, min_length = 3, label = "Kullanıcı Adı:" )
    password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, label="Parola")
    confirm = forms.CharField(max_length=20,min_length=8, label="Parolayı Doğrula", widget=forms.PasswordInput)
    #Django docsta şifre kontrol metodu
    def clean(self):
        """Şifrelerin uyuşup uyuşmadığını kontrol eder"""
        cleaned_data = super().clean()
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        confirm = self.cleaned_data.get("confirm")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor!")
        #Burada formdaki verileri almak için sözlük yapısı kuruyoruz. Django bu verileri sözlük içerisinde işliyor.
        values = {
            "username": username,
            "password": password,            
            "email": email,            
            "first_name": first_name,            
            "last_name": last_name,            
        }
        return values

#Giriş formu
class LoginForm(forms.Form):
    """Giriş Formu Sınıfı"""
    username = forms.CharField(label = "Kullanıcı Adı:")
    password = forms.CharField(label = "Şifre:", widget = forms.PasswordInput)