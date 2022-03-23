from random import choices
from secrets import choice
from turtle import mode
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User

# Create your models here.
class Member(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    is_equbtegna = models.BooleanField()

    def __str__(self):
        return self.user
    
class Request(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title



class Category(models.Model):
    name = CharField(max_length= 50)
    
    
class Book(models.Model):
    title = models.CharField(max_length=200,null=False,blank=False)
    author = models.CharField(max_length=200,null=False,blank=False)
    price = models.FloatField(null=False,blank=False)
    oldprice = models.FloatField(null=False)
    pages = models.IntegerField(null=False)
    categories = models.ManyToManyField(Category, )
    description = models.TextField(null=False)
    about_author = models.TextField(null=True, blank=True)
    # images = models.ImageField()
    new_book = models.BooleanField(null=False)
    def __str__(self):
        return self.title    
    

class Equb(models.Model):
    EQUB_TYPE = (
       ("1ኛ ደረጃ","1ኛ ደረጃ"),
       ("2ኛ ደረጃ","2ኛ ደረጃ" ),
       ("3ኛ ደረጃ","3ኛ ደረጃ" ),
       ("4ኛ ደረጃ","4ኛ ደረጃ" ),
    )
    type = models.CharField(max_length=200, choices=EQUB_TYPE)
    

class Packages(models.Model):
    title = models.CharField(max_length=400)
    discount = models.FloatField()
    price = models.FloatField()
    description = models.TextField()
    books = models.ManyToManyField(Book, related_name='books', blank=True)
    
    def __str__(self) -> str:
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE) 
    comment = models.TextField(null=True)
    
    def __str__(self):
        return self.comment[:49]
    
    
class Equbtegna(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    unpaid_month = models.IntegerField()
    equb = models.ForeignKey(Equb, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user)

    
    
    
    
    