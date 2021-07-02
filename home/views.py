import json

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm, UserUpdateForm, ProfileUpdateForm, HomeForm
from home.models import Setting, ContactForm, ContactFormMessage, Home, Category, Comment, Images, CommentForm, \
    UserProfile, FAQ


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Home.objects.filter(status='True')[:4]
    category = Category.objects.all()
    dayhomes = Home.objects.filter(status='True')[:6]
    lasthomes = Home.objects.filter(status='True').order_by('-id')[:6]
    randomhomes = Home.objects.filter(status='True').order_by('?')[:6]
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
    homes=Home.objects.filter(category_id=id,status='True')
    context = {'homes':homes,
               'category':category,
               'categorydata':categorydata
               }
    return render(request,'homes.html',context)

def home_detail(request,id,slug):
    category = Category.objects.all()
    home = Home.objects.get(pk=id)
    current_user = home.user
    profile= UserProfile.objects.get(user_id=current_user.id)
    images = Images.objects.filter(home_id=id)
    comment = Comment.objects.filter(home_id=id, status='True')
    randomhomes = Home.objects.filter(status='True').order_by('?')[:4]
    context = { 'home': home,
                'profile':profile,
               'category': category,
                'images':images,
                'comment':comment,
                'randomhomes':randomhomes,
               }
    return render(request,'home_detail.html',context)

def content_detail(request,id,slug):
    category = Category.objects.all()
    home = Home.objects.filter(category_id=id,status='True')
    link = '/home/'+str(home[0].id)+'/'+home[0].slug
    return HttpResponseRedirect(link)

def home_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']

            if catid == 0:
                home = Home.objects.filter(title__icontains=query, status='True')
            else:
                home = Home.objects.filter(title__icontains=query, category__id=catid, status='True')

            context = {
                'home' : home,
                'category' : category,
            }
            return render(request, 'homes_search.html', context)

    return HttpResponseRedirect('/')

def home_search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    home = Home.objects.filter(title__icontains=q ,status='True')
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

@login_required(login_url='/login')
def user_view(request):
    category = Category.objects.all()
    current_user=request.user
    profile= UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile':profile,
               }
    return render(request, 'user_profile.html',context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,'category': category
                       })

def user_comments(request):
    #category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        #'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login') # Check login
def user_deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')

def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by("ordernumber")

    context = {
        'category':category,
        'faq': faq,
    }
    return render(request, 'faq.html', context)

@login_required(login_url='/login')
def home(request):
    category = Category.objects.all()
    current_user = request.user
    home = Home.objects.filter(user_id=current_user.id)
    context = {
        'category' : category,
        'home' : home,
    }
    return render(request, 'user_home.html', context)

@login_required(login_url='/login')
def addhome(request):
    if request.method == 'POST':
        form = HomeForm(request.POST, request.FILES)
        if form.is_valid():
            current_user=request.user
            data=Home()
            data.user_id=current_user.id
            data.category = form.cleaned_data['category']
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.slug = form.cleaned_data['slug']
            data.image = form.cleaned_data['image']
            data.price = form.cleaned_data['price']
            data.square_meters = form.cleaned_data['square_meters']
            data.number_of_rooms = form.cleaned_data['number_of_rooms']
            data.building_age = form.cleaned_data['building_age']
            data.floor_location = form.cleaned_data['floor_location']
            data.number_of_floors = form.cleaned_data['number_of_floors']
            data.furnished = form.cleaned_data['furnished']
            data.using_status = form.cleaned_data['using_status']
            data.dues = form.cleaned_data['dues']
            data.from_who = form.cleaned_data['from_who']
            data.swap = form.cleaned_data['swap']
            data.detail = form.cleaned_data['detail']
            data.status='False'
            data.save()
            messages.success(request, 'Emlak başarı ile eklendi')
            return HttpResponseRedirect('/user/home')
        else:
            messages.success(request, 'Emlak form hatası :' +str(form.errors))
            return HttpResponseRedirect('/user/addhome')
    else:
        category=Category.objects.all()
        form=HomeForm()
        context = {
            'category':category,
            'form':form,
        }
        return render(request, 'user_addhome.html',context)

@login_required(login_url='/login')
def homeedit(request,id):
    home = Home.objects.get(id=id)
    if request.method=='POST':
        form = HomeForm(request.POST, request.FILES, instance=home)
        if form.is_valid():
            form.save()
            messages.success(request, 'Emlak bilgileri başarıyla güncellendi')
            return HttpResponseRedirect('/user/home')
        else:
            messages.success(request, 'Form hatası :' +str(form.errors))
            return HttpResponseRedirect('/user/homeedit/'+str(id))
    else:
        category = Home.objects.all()
        form = HomeForm(instance=home)
        context = {
            'category':category,
            'form':form,
        }
        return render(request, 'user_edithome.html',context)

@login_required(login_url='/login')
def homedelete(request,id):
    current_user=request.user
    Home.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Emlak kaydı silindi...')
    return HttpResponseRedirect('/user/home')

