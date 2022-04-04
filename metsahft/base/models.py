from email.policy import default
from random import choices
import uuid
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User
from . import ethiopian_date
import datetime
# Create your models here.


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, unique=True)
    is_equbtegna = models.BooleanField()

    def __str__(self):
        return self.user.username


class Request(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=False, blank=False)
    author = models.CharField(max_length=200, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    oldprice = models.FloatField(null=False)
    pages = models.IntegerField(null=False)
    categories = models.ManyToManyField(Category)
    description = models.TextField(null=False)
    about_author = models.TextField(null=True, blank=True)
    image_front = models.ImageField(null=False, default="yebrhan_enat.jpg")
    image_back = models.ImageField(null=False, default="yebrhan_back.jpg")
    new_book = models.BooleanField(null=False)
    count = models.IntegerField(default=0)
    created = models.DateTimeField(
        auto_now_add=True)
    popularity = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Equb(models.Model):
    EQUB_TYPE = (
        ("1ኛ ደረጃ", "1ኛ ደረጃ"),
        ("2ኛ ደረጃ", "2ኛ ደረጃ"),
        ("3ኛ ደረጃ", "3ኛ ደረጃ"),
        ("4ኛ ደረጃ", "4ኛ ደረጃ"),
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
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.comment[:49]


class Equbtegna(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    unpaid_month = models.IntegerField()
    equb = models.ForeignKey(Equb, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member)


class EqubtegnaDetail(models.Model):

    def current_year():
        gc_time = datetime.date.today()
        et_conv = ethiopian_date.EthiopianDateConverter()
        et_time = et_conv.date_to_ethiopian(gc_time)
        return et_time
    YEAR_CHOICES = [(r, r) for r in range(2000, current_year()[0] + 1)]

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
    equbtegna = models.ForeignKey(Equbtegna, on_delete=models.CASCADE)
    paid_amount = models.FloatField()
    year = models.IntegerField(choices=YEAR_CHOICES, default=current_year()[0])
    month = models.CharField(max_length=200, default="መስከረም", choices=MONTHS)

    def __str__(self):
        return self.equbtegna.member.user.username


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    price = models.IntegerField()
    books = models.ManyToManyField(Book)
    delivery = models.BooleanField(default=False)
    paid = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.member.user.username


class Quantity(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()


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
    YEAR_CHOICES = [(r, r)
                    for r in range(2000, ethiopian_date.current_year()[0] + 1)]

    equbtegna = models.ForeignKey(Equbtegna, on_delete=models.CASCADE)
    year = models.IntegerField(
        choices=YEAR_CHOICES, default=ethiopian_date.current_year()[0])
    month = models.CharField(max_length=200, default="መስከረም", choices=MONTHS)

    def __str__(self):
        return self.equbtegna.member.user.username
