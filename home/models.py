from django.db import models

# Create your models here.
class Category(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Home(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # relation with Category Table
    title = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    square_meters = models.PositiveIntegerField()
    NUMBER_OF_ROOMS = (
        ('Default', 'Belirtilmemiş'),
        ('1', '1+1'),
        ('2', '2+1'),
        ('3', '3+1'),
        ('4', '4+1'),
    )
    number_of_rooms = models.CharField(max_length=30, choices=NUMBER_OF_ROOMS, default='Default')
    building_age = models.PositiveIntegerField()
    floor_location = models.IntegerField()
    number_of_floors = models.PositiveIntegerField()
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
    dues = models.PositiveIntegerField()
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
    detail = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Images(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title