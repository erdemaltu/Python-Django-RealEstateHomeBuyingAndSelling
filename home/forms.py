from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from home.models import UserProfile, Home


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    catid = forms.IntegerField()

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='Kullanıcı Adı :')
    email = forms.EmailField(max_length=200, label='Email :')
    first_name = forms.CharField(max_length=100, help_text='İsim', label='İsim :')
    last_name = forms.CharField(max_length=100, help_text='Soyisim', label='Soyisim :')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'username','email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder':'kullanıcı adı'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
            'first_name': TextInput(attrs={'class': 'input','placeholder':'isim'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'soyisim' }),
        }

CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city','country','image')
        widgets = {
            'phone'     : TextInput(attrs={'class': 'input','placeholder':'telefon'}),
            'address'   : TextInput(attrs={'class': 'input','placeholder':'adres'}),
            'city'      : Select(attrs={'class': 'input','placeholder':'şehir'},choices=CITY),
            'country'   : TextInput(attrs={'class': 'input','placeholder':'Ülke' }),
            'image'     : FileInput(attrs={'class': 'input', 'placeholder': 'resim', }),
        }

class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ('category', 'title', 'keywords', 'description', 'slug', 'price',
                'square_meters', 'number_of_rooms', 'building_age', 'floor_location', 'number_of_floors',
                'furnished', 'using_status', 'dues', 'from_who', 'swap', 'detail', 'image')
        widgets = {
            'category': Select(attrs={'class': 'form-control', 'placeholder': 'Kategori', }),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Başlık', }),
            'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'Anahtar Kelime', }),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Açıklama', }),
            'slug': TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug', }),
            'price': TextInput(attrs={'class': 'form-control', 'placeholder': 'Fiyat', }),
            'square_meters': TextInput(attrs={'class': 'form-control', 'placeholder': 'Metrekare', }),
            'number_of_rooms': Select(attrs={'class': 'form-control', 'placeholder': 'Oda Sayısı', }),
            'building_age': TextInput(attrs={'class': 'form-control', 'placeholder': 'Bina Yaşı', }),
            'floor_location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Bulunduğu Kat', }),
            'number_of_floors': TextInput(attrs={'class': 'form-control', 'placeholder': 'Kat Sayısı', }),
            'furnished': Select(attrs={'class': 'form-control', 'placeholder': 'Eşyalı', }),
            'using_status': Select(attrs={'class': 'form-control', 'placeholder': 'Kullanım Durumu', }),
            'dues': TextInput(attrs={'class': 'form-control', 'placeholder': 'Aidat', }),
            'from_who': Select(attrs={'class': 'form-control', 'placeholder': 'Kimen', }),
            'swap': Select(attrs={'class': 'form-control', 'placeholder': 'Takas', }),
            'detail': CKEditorWidget(),
            'image': FileInput(attrs={'class': 'form-control', 'placeholder': 'Resim', }),
        }