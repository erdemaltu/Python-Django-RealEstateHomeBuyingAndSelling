"""emlak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from home import views

urlpatterns = [
    path('', include('home.urls')),
    path('hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('referanslar/', views.referanslar, name='referanslar'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('home/', include('home.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('home/<int:id>/<slug:slug>/', views.home_detail, name= 'home_detail'),
    path('content/<int:id>/<slug:slug>/', views.content_detail, name='content_detail'),
    path('category/<int:id>/<slug:slug>/', views.category_homes, name='category_homes'),
    path('search/', views.home_search, name='home_search'),
    path('search_auto/', views.home_search_auto, name='home_search_auto'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('user/', views.user_view, name='user_view'),
    path('user/update/', views.user_update, name='user_update'),
    path('user/password/', views.user_password, name='user_password'),
    path('user/comments/', views.user_comments, name='user_comments'),
    path('user/deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),
    path('faq/', views.faq, name='faq'),
    path('user/addhome/', views.addhome, name='addhome'),
    path('user/home/', views.home, name='home'),
    path('user/homeedit/<int:id>', views.homeedit, name='homeedit'),
    path('user/homedelete/<int:id>', views.homedelete, name='homedelete'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)