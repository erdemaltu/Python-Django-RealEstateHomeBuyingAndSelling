import json

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage, Home, Category, Comment, Images, CommentForm, \
    UserProfile


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Home.objects.all()[:4]
    category = Category.objects.all()
    dayhomes = Home.objects.all()[:4]
    lasthomes = Home.objects.all().order_by('-id')[:4]
    randomhomes = Home.objects.all().order_by('?')[:4]
    context = {
        'setting': setting,
        'category': category,
        'page': 'home',
        'sliderdata': sliderdata,
        'dayhomes': dayhomes,
        'lasthomes': lasthomes,
        'randomhomes': randomhomes}
    return render(request, 'index.html', context)

@login_required(login_url='/login')
def addcomment(request, id):

    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user

            data = Comment()
            data.user_id = current_user.id
            data.home_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Yorumunuz başarı ile gönderilmiştir. Teşekkür Ederiz")
            return HttpResponseRedirect(url)

    messages.warning(request, "Yorumunuz kaydedilmedi.Lütfen kotrol ediniz")
    return HttpResponseRedirect(url)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)

    context = {'setting': setting, 'page':'hakkimizda'}
    return render(request, 'hakkimizda.html', context)
def referanslar(request):
    setting = Setting.objects.get(pk=1)

    context = {'setting': setting, 'page':'referanslar'}
    return render(request, 'referanslar.html', context)
def iletisim(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['name']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür Ederiz")
            return HttpResponseRedirect('/iletisim')
    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    context = {'setting': setting, 'form':form}
    return render(request, 'iletişim.html', context)

def category_homes(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    homes=Home.objects.filter(category_id=id)
    context = {'homes':homes,
               'category':category,
               'categorydata':categorydata
               }
    return render(request,'homes.html',context)

def home_detail(request,id,slug):
    category = Category.objects.all()
    home = Home.objects.get(pk=id)
    images = Images.objects.filter(home_id=id)
    comment = Comment.objects.filter(home_id=id, status='True')
    context = { 'home': home,
               'category': category,
                'images':images,
                'comment':comment,
               }
    return render(request,'home_detail.html',context)

def home_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']

            if catid == 0:
                home = Home.objects.filter(title__icontains=query)
            else:
                home = Home.objects.filter(title__icontains=query, category__id=catid)

            context = {
                'home' : home,
                'category' : category,
            }
            return render(request, 'homes_search.html', context)

    return HttpResponseRedirect('/')

def home_search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    home = Home.objects.filter(title__icontains=q)
    results = []
    for rs in home:
      home_json = {}
      home_json = rs.title
      results.append(home_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası ! Kullanıcı adı yada şifre yanlış ")
            return HttpResponseRedirect('/login')
    category= Category.objects.all()
    context = {'category': category,
               }
    return render(request, 'login.html',context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request,"Hoşgeldiniz... Sitemize başarılı bir şekilde üye oldunuz.İyi alış verişler dileriz.")
            return HttpResponseRedirect('/')
    category = Category.objects.all()
    form = SignUpForm()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)

def user_view(request):
    category = Category.objects.all()
    current_user=request.user
    profile= UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile':profile,
               }
    return render(request, 'user_profile.html',context)
