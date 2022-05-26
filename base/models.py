

from . import ethiopian_date

import uuid
from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.

#modified id
class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=100)
    phone = models.CharField(max_length=13, unique=True ,  error_messages= {'unique':'በዚህ ስልክቁጥር የተመዘገበ ደንበኛ አለ!'})
    address = models.CharField(
        max_length=255)
    is_equbtegna = models.BooleanField(default=False, editable=True)
    chat_id = models.CharField(default=None, editable=True, null=True, blank= True, max_length=100)

    # def __str__(self):
    #     return self.user.name


class Request(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=200 , null=True)
    def __str__(self):
        return self.title



class Category(models.Model):
    name = models.CharField(max_length=100 , primary_key=True)
    def __str__(self):
        return self.name

#correct the newbook field and added new field created
class Book(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, )
    author = models.CharField(max_length=200, )
    price = models.FloatField()
    oldprice = models.FloatField()
    pages = models.IntegerField()
    categories = models.ManyToManyField(Category)
    description = models.TextField()
    about_author = models.TextField(null=True, blank=True)
    image_front = models.ImageField(null=True, default="yebrhan_enat.jpg")
    image_back = models.ImageField(null=True, default="yebrhan_enat.jpg")
    new_book = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    popularity = models.IntegerField(default=0, null=True, blank=True)
    count = models.IntegerField(default=0)
    rating_sum = models.IntegerField(null= True , blank=True, default=5)
    rating_count = models.IntegerField(default=1 , null=True , blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class Rating(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return str(self.member.user)

    

class Equb(models.Model):
    type = models.CharField(max_length=100, primary_key=True)
    amount = models.FloatField(default=220)
    currentRound = models.IntegerField(default=0)
    def __str__(self):
        return self.type
# added created field for packages
class Packages(models.Model):

    title = models.CharField(max_length=400)
    discount = models.FloatField()
    price = models.FloatField()
    amount = models.IntegerField(default=0)
    description = models.TextField( null = True)
    books = models.ManyToManyField(Book)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ("-created",)
    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name ="review", null =True)
    አስተያየት = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
   
    
    class Meta:
        ordering = ("-created",)
    
    def __str__(self):
        return self.አስተያየት[:49]

#modified to retrn str 
class Equbtegna(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    unpaid_month = models.IntegerField(default= 0)

    equb = models.ForeignKey(Equb, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member)

# added new Model
class EqubtegnaDetail(models.Model):
    
    def current_year():
        gc_time =  datetime.date.today()
        et_conv = ethiopian_date.EthiopianDateConverter()
        et_time = et_conv.date_to_ethiopian(gc_time)
        return et_time
    YEAR_CHOICES = [(r,r) for r in range(2000, current_year()[0] + 1)]
    
    MONTHS = (
        ("መስከረም", "መስከረም"),
        ("ጥቅምት", "ጥቅምት"),
        ("ህዳር", "ህዳር"),
        ("ታህሳስ", "ታህሳስ"),
        ("ጥር", "ጥር"),
        ("የካቲት", "የካቲት"),
        ("መጋቢት", "መጋቢት"),
        ("ሚያዚያ", "ሚያዚያ"),
        ("ግንቦት", "ግንቦት"),
        ("ሰኔ", "ሰኔ"),
        ("ሐምሌ", "ሐምሌ"),
        ("ነሐሴ", "ነሐሴ"),
    )
    equbtegna = models.ForeignKey(Equbtegna , on_delete=models.CASCADE)
    paid_amount = models.FloatField()
    year = models.IntegerField(choices=YEAR_CHOICES, default=current_year()[0])
    month = models.CharField(max_length=200 ,default="መስከረም", choices=MONTHS)
    def __str__(self):
        return self.equbtegna.member.user.username


class OrderBook(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.book.title


class OrderPackage(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.package.title

#modified to return str
class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    books = models.ManyToManyField(OrderBook)
    packages = models.ManyToManyField(OrderPackage, null=True)
    delivery = models.BooleanField(null=False, default=False, editable=True)
    paid = models.BooleanField(null=False, default=False, editable=True)
    sold = models.BooleanField(null=False, default=False, editable=True)
    bank_payment = models.BooleanField(null = False, default= True, editable=True)
    transaction_id = models.CharField(null = True,blank = True,max_length=50)

    def __str__(self):
        return self.member.user.username

class Winner(models.Model):
    
    MONTHS = (
        ("መስከረም", "መስከረም"),
        ("ጥቅምት", "ጥቅምት"),
        ("ህዳር", "ህዳር"),
        ("ታህሳስ", "ታህሳስ"),
        ("ጥር", "ጥር"),
        ("የካቲት", "የካቲት"),
        ("መጋቢት", "መጋቢት"),
        ("ሚያዚያ", "ሚያዚያ"),
        ("ግንቦት", "ግንቦት"),
        ("ሰኔ", "ሰኔ"),
        ("ሐምሌ", "ሐምሌ"),
        ("ነሐሴ", "ነሐሴ"),
    )
    YEAR_CHOICES = [(r,r) for r in range(2000, ethiopian_date.current_year()[0] + 1)]

    equbtegna = models.ForeignKey(Equbtegna , on_delete=models.CASCADE)
    year = models.IntegerField(choices=YEAR_CHOICES, default=ethiopian_date.current_year()[0])
    month = models.CharField(max_length=200 ,default="መስከረም", choices=MONTHS)
    round = models.IntegerField(default= 0)
    
    def __str__(self):
        return self.equbtegna.member.user.username

