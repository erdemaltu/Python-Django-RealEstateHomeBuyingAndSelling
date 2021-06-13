from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactForm, ContactFormMessage, Home, Category


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Home.objects.all()[:4]
    category = Category.objects.all()
    dayhomes = Home.objects.all()[:4]
    lasthomes = Home.objects.all().order_by('-id')[:4]
    randomhomes = Home.objects.all().order_by('?')[:4]
    context = {
        'setting': setting,
        'category':category,
        'page':'home',
        'sliderdata':sliderdata,
        'dayhomes':dayhomes,
        'lasthomes':lasthomes,
        'randomhomes':randomhomes}
    return render(request, 'index.html', context)

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