from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm, TextInput, Textarea, FileInput
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Home(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # relation with Category Table
    title = models.CharField(max_length=255)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(blank=True,null=True, upload_to="images/")
    price = models.FloatField()
    square_meters = models.PositiveIntegerField(blank=True)
    NUMBER_OF_ROOMS = (
        ('Default', 'Belirtilmemiş'),
        ('1', '1+1'),
        ('2', '2+1'),
        ('3', '3+1'),
        ('4', '4+1'),
    )
    number_of_rooms = models.CharField(blank=True, max_length=30, choices=NUMBER_OF_ROOMS, default='Default')
    building_age = models.PositiveIntegerField(blank=True)
    floor_location = models.IntegerField(blank=True)
    number_of_floors = models.PositiveIntegerField(blank=True)
    FURNISHED = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    furnished = models.CharField(max_length=30, choices=FURNISHED, default='False')
    USING_STATUS = (
        ('Idle', 'Boşta'),
        ('OnRent', 'Kirada'),
    )
    using_status = models.CharField(max_length=30, choices=USING_STATUS, default='Idle')
    dues = models.PositiveIntegerField(blank=True)
    FROM_WHO = (
        ('FromTheOwner', 'Sahibinden'),
        ('FromRealEstateAgent', 'Emlakçıdan'),
    )
    from_who = models.CharField(max_length=30, choices=FROM_WHO, default='FromTheOwner')
    SWAP = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    swap = models.CharField(max_length=30, choices=SWAP, default='False')
    status = models.CharField(max_length=10, choices=STATUS)
    detail = RichTextUploadingField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def get_absolute_url(self):
        return reverse('home_detail', kwargs={'slug': self.slug})

class HomeForm(ModelForm):
    class Meta:
        model = Home
        fields=['category', 'title', 'keywords', 'description', 'slug', 'image', 'price',
                'square_meters', 'number_of_rooms', 'building_age', 'floor_location', 'number_of_floors',
                'furnished', 'using_status', 'dues', 'from_who', 'swap', 'detail', ]
        widgets = {
            #'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }

class Images(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True, max_length=150)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=150)
    smtpserver = models.CharField(blank=True, max_length=20)
    smtpemail = models.CharField(blank=True, max_length=20)
    smtppassword = models.CharField(blank=True, max_length=10)
    smtpport = models.CharField(blank=True,max_length=5)
    icon= models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.CharField(blank=True, max_length=255)
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'İsim & Soyisim'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Konu'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email Adresi'}),
            'message': Textarea(attrs={'class': 'input', 'placeholder': 'Mesajınız', 'rows': '5'}),
        }

class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=200, blank=True)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name+' '+self.user.last_name+' ['+self.user.username + '] '

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']

class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    status=models.CharField(max_length=10, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question



