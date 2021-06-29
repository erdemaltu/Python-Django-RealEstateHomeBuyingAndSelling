from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from home.models import UserProfile


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