from collections import defaultdict
from email import message
from email.policy import default
from http.client import HTTP_PORT
from django.shortcuts import redirect, render
from django.db.models import Q
from django.core.paginator import Paginator
from random import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import *
from .forms import *
from django.template.defaulttags import register
import requests
from .utils import *
# Create your views here.


def home(request):

    books = Book.objects.all()
    if books.count() > 4:
        books = books[:4]

    categories = Category.objects.all()
    return render(request, "home.html", {"books": books, "categories": categories})


def loginPage(request):

    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        try:
            user = Member.objects.get(phone=phone).user
        except:
            user = None
            messages.error(request, "username is wrong")
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "password is incorrect")
    return render(request, "login.html")


@login_required(login_url="/login")
def logoutUser(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    usr = UserForm()
    form = MemberForm()

    if request.method == "POST":

        usr = UserForm(request.POST)
        form = MemberForm(request.POST)
        # print(form, "this is the form")
        if usr.is_valid() and form.is_valid():
            if form.is_valid() and usr.is_valid:
                usr.save()
                username = request.POST.get("username")
                member = form.save(commit=False)
                member.user = User.objects.get(username=username)
                member.is_equbtegna = False
                member.save()
                login(request, User.objects.get(username=username))
                return redirect("login")
        else:
            messages.error(request, "An error occurred during registration")
            return redirect("register")
    context = {
        "user": usr,
    }
    return render(request, "register.html", context)


@login_required(login_url="/login")
def userProfile(request):
    member = Member.objects.get(user=request.user)
    equbtegna = None
    if member.is_equbtegna == True:
        equbtegna = Equbtegna.objects.get(member=member)
    context = {'member': member, 'equbtegna': equbtegna}
    return render(request, 'user_profile.html', context)


@login_required(login_url="/login")
def editProfile(request):
    user = request.user
    member_form = MemberForm(instance=user)
    if request.method == "POST":
        member_form = MemberForm(
            request.POST, instance=Member.objects.get(user=request.user))
        print(member_form.is_valid())
        if member_form.is_valid():
            member_form.save()
            return redirect("user-profile")
        else:
            return HttpResponse("this shit is invalid YO")
            messages.error(request, "One or more invalid fields")

    context = {"member_form": member_form}
    return render(request, 'edit-profile.html', context)


@login_required(login_url="/login")
def create_book(request):
    if not request.user.has_perm("admin"):
        return redirect("home")
    form = BookForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print(form.errors)
            return redirect("create_book")
    return render(request, 'create-book.html', {'form': form, "categories": categories})


@register.filter
def get_(dictionary, key):
    return dictionary.get(str(key))


@login_required(login_url="/login")
def cart(request):
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(member=Member.objects.get(user=user))
    books = order.books.all()
    packages = order.packages.all()
    package_count = len(packages)
    count = len(books)
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        order = Order.objects.get(member=Member.objects.get(user=user))
        books = order.books.all()
        count = len(books)

        amount_dict = defaultdict(int)
        for index in range(count):
            amount_dict[str(books[index].id)] += int(request.POST.get(
                "amount{}".format(index)))

        for id in amount_dict:
            if Book.objects.get(id=id).count < amount_dict[id]:
                messages.error(request, "Sorry the amount of books you have reqeusted for the book {} with amount {} is less than the amount you have requested which is {}.".format(
                    Book.objects.get(id=id).title, Book.objects.get(id=id).count, amount_dict[id]))
                return redirect("cart")

        for package in packages:
            for book in package.books.all():
                if amount_dict[str(book.id)] + 1 > book.count:
                    messages.error(request,
                                   "the amount of {} books left is lower than the amount of books you are currently specifying".format(book.title))
        print(amount_dict)
        request.session["cart"] = amount_dict
        # request.session[""]
        return redirect("checkout")
    return render(request, 'shopping-cart.html', {'books': books, "order": order, "count": count, "packages": packages, "package_count": package_count})


@ login_required(login_url="/login")
def add_package_to_cart(request, pk):
    if not Packages.objects.get(id=pk):
        return redirect("home")
    if not Member.objects.get(user=request.user):
        return redirect("login")
    user = User.objects.get(id=request.user.id)
    order, created = Order.objects.get_or_create(
        member=Member.objects.get(user=user))
    order.paid = False
    order.delivery = False
    order.save()
    # return HttpResponse(order.books.get(id=pk))
    if order.packages.filter(id=pk):
        return redirect("cart")
    order.packages.add(Packages.objects.get(id=pk))
    return redirect("cart")


@ login_required(login_url="/login")
def delete_package_from_cart(request, pk):
    if not Packages.objects.get(id=pk):
        return redirect("home")
    if not Member.objects.get(user=request.user):
        return redirect("login")
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(member=Member.objects.get(user=user))
    order.packages.remove(Packages.objects.get(id=pk))
    return redirect("cart")


@ login_required(login_url="/login")
def add_to_cart(request, pk):
    if not Book.objects.get(id=pk):
        return redirect("home")
    if not Member.objects.get(user=request.user):
        return redirect("login")
    user = User.objects.get(id=request.user.id)
    order, created = Order.objects.get_or_create(
        member=Member.objects.get(user=user))
    order.paid = False
    order.delivery = False
    order.save()
    # return HttpResponse(order.books.get(id=pk))
    if order.books.filter(id=pk):
        return redirect("cart")
    order.books.add(Book.objects.get(id=pk))
    return redirect("cart")


@ login_required(login_url="/login")
def delete_from_cart(request, pk):
    if not Book.objects.get(id=pk):
        return redirect("home")
    if not Member.objects.get(user=request.user):
        return redirect("login")
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(member=Member.objects.get(user=user))
    amount_dict = request.session.get("cart")

    if amount_dict != None and str(pk) in amount_dict:
        amount_dict.remove(str(pk))
    order.books.remove(Book.objects.get(id=pk))
    return redirect("cart")


@ login_required(login_url="/login")
def checkout(request):
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(member=Member.objects.get(user=user))
    packages = order.packages.all()
    packages_count = len(packages)
    books = order.books.all()

    amount_dict = request.session["cart"]
    count = len(books)
    total = 0
    for book in books:
        if Book.objects.get(id=book.id).count < int(amount_dict[str(book.id)]):
            messages.error(request, "Sorry the amount of books you have reqeusted for the book {} with amount {} is less than the amount you have requested which is {}.".format(
                book.title, book.count, amount_dict[str(book.id)]))
            return redirect("cart")
        total += (int(book.price) *
                  int(amount_dict[str(book.id)]))

    for package in packages:
        value = 1
        if str(book.id) in amount_dict:
            value += amount_dict[str(book.id)]
        if value > book.count:
            messages.error(request, "Sorry the amount of books you have reqeusted for the book {} with amount {} is less than the amount you have requested which is {}.".format(
                book.title, book.count, value))
            return redirect("cart")

        total += (package.price - package.discount)

    if request.method == 'POST':
        for book in books:
            if Book.objects.get(id=book.id).count < int(amount_dict[str(book.id)]):
                messages.error(request, "we only have {} books left".format(
                    Book.objects.get(id=book.id).count))
                return redirect("cart")
        for package in packages:
            value = 1
            if str(book.id) in amount_dict:
                value += amount_dict[str(book.id)]
            if value > book.count:
                messages.error(request, "Sorry the amount of books you have reqeusted for the book {} with amount {} is less than the amount you have requested which is {}.".format(
                    book.title, book.count, value))
                return redirect("cart")

            total += (package.price - package.discount)
        user = User.objects.get(id=request.user.id)
        order = Order.objects.get(member=Member.objects.get(user=user))
        order.delivery = request.POST.get("delivery")
        order.save()
        books = order.books.all()
        try:
            amount_dict = request.session["cart"]
            if len(amount_dict) == 0 and len(order.packages.all()) == 0:
                raise Exception("nothing in the cart")
        except:
            messages.error(request, "you have nothing in the cart")
            return redirect("checkout")
        items = []
        for book in books:
            items.append(
                {
                    "itemId": str(book.id),
                    "itemName": str(book.title),
                    "unitPrice": str(book.price),
                    "quantity": str(amount_dict[str(book.id)])
                }
            )
        for package in packages:
            items.append(
                {
                    "itemId": str(package.id),
                    "itemName": str(package.title),
                    "unitPrice": str(package.price - package.discount),
                    "quantity": 1
                }
            )
        url = "https://testapi.yenepay.com/api/urlgenerate/getcheckouturl/"
        data = {
            "process": "Cart",
            "successUrl": "http://localhost:8000/success",
            "ipnUrl": "http://localhost:8000/ipn",
            "cancelUrl": "http://localhost:8000/cancel",
            "merchantId": "SB1475",
            "merchantOrderId": str(order.id),
            "expiresAfter": 0.4,
            "items": items,
            "totalItemsDeliveryFee": 0,
            "totalItemsTax1": 0
        }
        response = requests.post(url=url, json=data)
        print(response.status_code)
        if response.status_code == 200:
            for book in books:
                Quantity.objects.get_or_create(
                    order=order,
                    book=book,
                    quantity=amount_dict[str(book.id)]
                )
            for package in packages:
                PackageQuantity.objects.get_or_create(
                    order=order,
                    package=package,
                    quantity=1
                )
            result = response.json().get("result")
            return redirect(result)
        else:
            message.error("Error has been encountered")
            redirect("checkout")
    context = {'books': books, "order": order, "count": count,
               "amount": amount_dict, "total": total, "packages": packages}
    return render(request, 'checkout.html', context)


def success(request):
    ii = request.GET.get('itemId')
    total = request.GET.get('TotalAmount')
    moi = request.GET.get('MerchantOrderId')
    ti = request.GET.get('TransactionId')
    status = request.GET.get('Status')
    url = 'https://testapi.yenepay.com/api/verify/pdt/'
    data = {
        "requestType": "PDT",
        "pdtToken": "GLxwJZFcC8SX4X",
        "transactionId": ti,
        "merchantOrderId": moi
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("It's Paid")
        order = Order.objects.get(id=moi)
        books = order.books.all()
        packages = order.packages.all()
        for book in books:
            specific = Quantity.objects.get(
                order=order,
                book=book
            )
            final_book = Book.objects.get(id=book.id)
            final_book.count -= int(specific.quantity)
            final_book.save()
        for package in packages:
            for book in package.books.all():
                final_book = Book.objects.get(id=book.id)
                final_book.count -= int(specific.quantity)
                final_book.save()
        order.paid = True
        order.save()
        # del request.session['cart']
    else:
        messages.error(request, "Payment incomplete")
        redirect("checkout")
        print('Invalid payment process')
    return render(request, 'success.html', {'total': total, 'status': status, "id": ti})


def cancel(request):
    return redirect("cart")


def ipn(request):
    messages.success("the ipn request has been successful")
    print("the ipn thing has been successful")
    return HttpResponse("this is to tell you that the ipn notification is working")
    url = "https://testapi.yenepay.com/api/verify/ipn/"
    totalAmount = request.GET.get('totalAmount')
    buyerId = request.GET.get('buyerId')
    merchantOrderId = request.GET.get('merchantOrderId')
    merchantId = request.GET.get('merchantId')
    merchantCode = request.GET.get('merchantCode')
    transactionId = request.GET.get('transactionId')
    status = request.GET.get("status")
    transactionCode = request.GET.get('transactionCode')
    currency = request.GET.get('currency')
    signature = request.GET.get('signature')

    data = {
        "totalAmount": totalAmount,
        "buyerId": buyerId,
        "merchantOrderId": merchantOrderId,
        "merchantId": merchantId,
        "merchantCode": merchantCode,
        "transactionId": transactionId,
        "status": status,
        "transactionCode": transactionCode,
        "currency": currency,
        "signature": signature
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("It's Paid")
        order = Order.objects.get(id=merchantOrderId)
        books = order.books.all()
        amount_dict = request.session["cart"]
        for book in books:
            Quantity.objects.create(
                order=order,
                book=book,
                quantity=amount_dict[str(book.id)]
            )
            final_book = Book.objects.get(id=book.id)
            final_book.count -= int(amount_dict[str(book.id)])
            final_book.save()
        order.paid = True
        order.save()
        del request.session['cart']
    else:
        print('Invalid payment process')
    return render(request, 'ipn.html')


@ register.filter
def get_value(dictionary, key):
    return dictionary.get(str(key))


@register.filter()
def subtract(value1, value2):
    return value1 - value2


def all_packages(request):
    packages = Packages.objects.all()
    # print(packages[0].books.all()[0].image_front)

    return render(request, 'all-packages.html', {'packages': packages})


def delete_request(request, pk):
    if request.method == "POST":
        req = Request.objects.get(id=pk)
        req.delete()
        return redirect('create_book')


@ login_required(login_url="/login")
def single_package(request, pk):

    package = Packages.objects.get(id=pk)
    books = package.books.all()
    # print(books, 'all books in apackage')
    context = {'package': package, 'books': books}

    return render(request, 'book_package.html', context)


@ login_required(login_url="/login")
def equb_user(request):
    cur_year = ethiopian_date.EthiopianDateConverter(
    ).date_to_ethiopian(datetime.date.today())
    cur_year = cur_year[0]

    form_year = request.GET.get('year')
    print(form_year)
    detail = EqubtegnaDetail.objects.all().filter(
        year=cur_year if not form_year else form_year)
    options = EqubtegnaDetail.YEAR_CHOICES

    choices = [int(i[0]) for i in list(options)][::-1]
    winners = Winner.objects.all()
    selected = int(cur_year) if not form_year else int(form_year)

    context = {'winners': winners, "detail": detail,
               'option': choices, 'selected': selected}
    return render(request, 'equb-single(back).html', context)


@ login_required(login_url="/login")
def equb_choice(request):
    user = User.objects.get(id=request.user.id)
    member = Member.objects.get(user=user)
    # I am assuming the equbtegna is authenticated
    equbtegna = Equbtegna.objects.get(member=member)
    print(equbtegna.equb)
    equboch = Equb.objects.all()
    return render(request, 'equb(back).html', {"equboch": equboch, 'equbtegna': str(equbtegna.equb)})

# choosen_books = []


@ login_required(login_url="/login")
def create_package(request):
    if not request.user.has_perm("admin"):
        return redirect("home")
    q = request.GET.get("q") if request.GET.get('q') != None else ''
    books = Book.objects.filter(Q(title__icontains=q) | Q(author__icontains=q))

    if request.method == 'POST':

        # print(choosen_books)

        add_or_remove = request.POST.get('add_or_remove')
        if request.POST.get('create_package') == 'create_package':

            title = request.POST.get('title')
            discount = request.POST.get('price')
            price = request.POST.get('old-price')
            description = request.POST.get('description')
            books_ = request.session['added_books']
            package = Packages(
                title=title,
                discount=discount,
                price=price,
                description=description,

            )

            # package.books.set(books_)
            print(package, books_)
            if title and discount and price and books_:
                package.save()
                request.session['added_books'].clear()
                request.session.modified = True

                return redirect('home')
            else:

                return redirect('create-package')

        if add_or_remove == 'add':
            id = request.POST.get('id')
            book_by_id = Book.objects.get(id=id)

            if 'added_books' in request.session:
                if str(book_by_id.id) not in request.session['added_books']:
                    request.session['added_books'].append(str(book_by_id.id))
            else:
                request.session['added_books'] = [str(book_by_id.id)]

            request.session.modified = True
        if add_or_remove == 'remove':
            id = request.POST.get('id')
            book_by_id = Book.objects.get(id=id)

            if str(book_by_id.id) in request.session['added_books']:
                request.session['added_books'].remove(str(book_by_id.id))
            request.session.modified = True

    choosen_books = Book.objects.filter(
        id__in=request.session['added_books'] if 'added_books' in request.session else None)
    context = {'books': books, 'choosen_books': choosen_books}
    return render(request, 'create-package(back).html', context)


@ login_required(login_url="/login")
def request_books(request):
    successful = 'False'
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        if title:
            requested_book = Request.objects.get_or_create(
                title=title, author=author)
            successful = "True"
            return render(request, 'request_books.html', {'successful': successful})

    context = {'successful': successful}
    return render(request, 'request_books.html', context)


@ login_required(login_url="/login")
def single_package(request, pk):

    package = Packages.objects.get(id=pk)
    books = package.books.all()
    context = {'package': package, 'books': books}

    return render(request, 'book_package.html', context)


@ login_required(login_url="/login")
def books(request):
    def isInt(num):

        try:
            num = float(num)
            print(num)
            if type(num) == float:
                return True
        except ValueError:
            return False
        except TypeError:
            return False
        return False

    const = 8
    category = Category.objects.all()
    q = request.GET.get('q') if request.GET.get('q') else ''
    sort = request.GET.get('sort') if isInt(request.GET.get('sort')) else 0
    c = request.GET.getlist('category') if request.GET.getlist(
        'category') else category
    pr = [request.GET.get('price-min') if isInt(request.GET.get('price-min')) else 0,
          request.GET.get('price-max') if isInt(request.GET.get('price-max')) else 5000]
    p = request.GET.get('p') if isInt(request.GET.get('p')) else 1
    c = set(c)
    books = []
    p = int(float(p))

    print(q)
    if sort == 1:
        books = Book.objects.filter(

            Q(title__icontains=q) & Q(author__icontains=q) & Q(
                description__icontains=q)

            & Q(price__gt=float(pr[0])-1) & Q(price__lt=float(pr[1])) & Q(categories__in=c)

        ).order_by('popularity')

    elif sort == 2:
        books = Book.objects.filter(
            Q(title__icontains=q) & Q(price__gt=float(
                pr[0])-1) & Q(price__lt=float(pr[1])) & Q(categories__in=c)

        ).order_by('-creation_time')

    else:
        books = Book.objects.filter(
            Q(title__icontains=q) & Q(price__gt=float(
                pr[0])-1) & Q(price__lt=float(pr[1])) & Q(categories__in=c)
        )

    newBooks = Book.objects.filter(new_book=True)
    category = Category.objects.all()
    pages = len(books)//const

    context = {"books": books[(p-1)*const:p*const], "pages": range(1, pages+2), 'p': p, "newBooks": newBooks,
               "minprice": pr[0], 'maxprice': pr[1], 'category': category, 'checkedBox': c}

    return render(request, "metsahft.html", context)


@ login_required(login_url="/login")
def listOfUsers(request):
    if not request.user.has_perm("admin"):
        return redirect("home")
    context = {}
    level = request.GET.get("l") if request.GET.get("l") else ''
    membersWithDept = Equbtegna.objects.filter(
        Q(equbtegna__unpaid_month__gt=0) & Q(equbtegna__type__icontains=level)
    )
    winners = None
    context["inDept"] = membersWithDept
    context["winners"] = winners
    if request.method == "POST":
        num = request.POST.get("num")
        level = request.POST.get("level")

        ekubtegna = Equbtegna.objects.filter(equb__type__et=level)
        ekubtegna = set(ekubtegna) if ekubtegna else set()

        prevWinners = Winner.objects.filter(equbtegna__equb__type__et=level)
        prevWinners = set(prevWinners) if prevWinners else set()

        players = ekubtegna.difference(prevWinners)
        winner = Winner()
        winners = []
        for i in range(num):
            lucky = random.choice(players)
            winner.year = ethiopian_date.current_year()[0]
            winner.month = ethiopian_date.current_year()[1]
            winner.equbtegna = lucky
            winners.append(lucky)
            players.remove(lucky)
            winner.save()

        context["winners"] = winners
        return render(request, "listOfUsers.html", context)
    return render(request, "listOfUsers.html", context)


@ login_required(login_url="/login")
def bookDetail(request, pk):
    book = Book.objects.get(id=pk)
    comments = Review.objects.filter(book=book)
    all_books = Book.objects.all()
    comment_paginator = Paginator(comments, 2)
    page_num = request.GET.get("page")
    page = comment_paginator.get_page(page_num)
    cats = list(book.categories.all())

    related_books = Book.objects.filter(categories=book.categories.all()[0])

    print(related_books)
    if request.method == "POST":
        comment_form = ReviewForm(data=request.POST)
        if comment_form.is_valid():
            comment = request.POST.get('አስተያየት')
            review = Review.objects.get_or_create(
                member=Member.objects.get(user=request.user),
                book=book,
                አስተያየት=comment
            )
            # review.save()
    else:
        comment_form = ReviewForm()
    print(book.categories)
    context = {"book": book, "comments": comments,
               "comment_form": comment_form, "page": page,
               "cats": cats, "related_books": related_books
               }
    return render(request, 'book_detail.html', context)


@ login_required(login_url="/login")
def deleteComment(request, pk):
    comment = Review.objects.get(id=pk)
    if Member.objects.get(user=request.user) != comment.member:
        return redirect("home")
    book = comment.book
    if request.method == "POST":
        comment.delete()
        return redirect("book_detail", pk=book.id)
    return render(request, 'book_detail.html', {"comment": comment})


@ login_required(login_url="/login")
def adminOrders(request):
    if not request.user.has_perm("admin"):
        return redirect("home")
    q = request.GET.get('q') if request.GET.get('q') else ""
    orders = Order.objects.filter(
        Q(member__user__username__icontains=q) |
        Q(id__icontains=q)
    )
    selected = 0
    if request.GET.get("delivery") == "2":
        orders = Order.objects.filter(delivery="True")
        selected = 2
    elif request.GET.get("delivery") == "1":
        orders = Order.objects.filter(delivery="False")
        selected = 1

    context = {"orders": orders, "selected": selected}
    return render(request, 'admin-orders.html', context)


@ login_required(login_url="/login")
def deleteOrder(request, pk):
    if not request.user.has_perm("admin"):
        return redirect("home")
    order1 = Order.objects.get(id=pk)
    if request.method == "POST":
        order1.delete()
        return redirect("admin-orders")

    context = {"order1": order1}
    return render(request, 'admin-orders.html', context)


@ login_required(login_url="/login")
def detailOrder(request, pk):
    if not request.user.has_perm("admin"):
        return redirect("home")
    order = Order.objects.get(id=pk)
    books = list(order.books.all())
    total = 0
    for book in books:
        total += book.price
    context = {"order": order, "books": books, "total": total}
    return render(request, 'detail-order.html', context)
