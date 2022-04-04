from email import message
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
# Create your views here.


def home(request):
    books = Book.objects.all()
    return render(request, "home.html", {"books": books})


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
            return HttpResponse("{} {}".format(usr.errors, form.errors))
            return HttpResponse("Here's the text of the web page.")
            messages.error(request, "An error occurred during registration")
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
            return HttpResponse(request.POST.get("categories"))
            messages.error(request, "")
            return redirect("create_book")
    return render(request, 'create-book.html', {'form': form, "categories": categories})


@login_required(login_url="/login")
def cart(request):
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(member=Member.objects.get(user=user))
    books = order.books.all()
    count = len(books)
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        order = Order.objects.get(member=Member.objects.get(user=user))
        books = order.books.all()
        count = len(books)

        amount_dict = {}
        for index in range(count):
            amount_dict[str(books[index].id)] = request.POST.get(
                "amount{}".format(index))
            # request.session[books[index].id] = request.POST.get(
            #     "amount {index}")
        print(amount_dict)
        request.session["cart"] = amount_dict
        return redirect("checkout")
    return render(request, 'shopping-cart.html', {'books': books, "order": order, "count": count})


@login_required(login_url="/login")
def add_to_cart(request, pk):
    user = User.objects.get(id=request.user.id)
    order, created = Order.objects.get_or_create(
        member=Member.objects.get(user=user))
    # return HttpResponse(order.books.get(id=pk))
    if order.books.get(id=pk):
        return redirect("cart")
    order.books.add(Book.objects.get(id=pk))
    return redirect("cart")


@login_required(login_url="/login")
def delete_from_cart(request, pk):
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(member=Member.objects.get(user=user))
    order.books.remove(Book.objects.get(id=pk))
    return redirect("cart")


@login_required(login_url="/login")
def checkout(request):
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(member=Member.objects.get(user=user))
    books = order.books.all()

    amount_dict = request.session["cart"]
    count = len(books)

    total = 0
    for book in books:
        total += (int(book.price) *
                  int(amount_dict[str(book.id)]))
        if Book.objects.get(id=book.id).count <= int(amount_dict[str(book.id)]):
            messages.error("we only have {} books left".format(
                Book.objects.get(id=book.id).count))
            return redirect("cart")

    if request.method == 'POST':
        for book in books:
            if Book.objects.get(id=book.id).count <= int(amount_dict[str(book.id)]):
                messages.error("we only have {} books left".format(
                    Book.objects.get(id=book.id).count))
                return redirect("cart")
        user = User.objects.get(id=request.user.id)
        order = Order.objects.get(member=Member.objects.get(user=user))
        order.delivery = request.POST.get("delivery")
        order.save()
        books = order.books.all()
        try:
            amount_dict = request.session["cart"]
        except:
            messages.error("you have nothing in the cart")
            return redirect("checkout")
        for book in books:
            Quantity.objects.create(
                order=order,
                book=book,
                quantity=amount_dict[str(book.id)]
            )
            final_book = Book.objects.get(id=book.id)
            final_book.count -= int(amount_dict[str(book.id)])
            final_book.save()
        del request.session['cart']
        return HttpResponse(request.session["cart"])
        return redirect("home")
    return render(request, 'checkout.html', {'books': books, "order": order, "count": count, "amount": amount_dict, "total": total})


@register.filter
def get_value(dictionary, key):
    return dictionary.get(str(key))


@login_required(login_url="/login")
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


@login_required(login_url="/login")
def equb_choice(request):
    user = User.objects.get(id=request.user.id)
    member = Member.objects.get(user=user)
    # I am assuming the equbtegna is authenticated
    equbtegna = Equbtegna.objects.get(member=member)
    print(equbtegna.equb)
    equboch = Equb.objects.all()
    return render(request, 'equb(back).html', {"equboch": equboch, 'equbtegna': str(equbtegna.equb)})

# choosen_books = []


@login_required(login_url="/login")
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


@login_required(login_url="/login")
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


@login_required(login_url="/login")
def single_package(request, pk):

    package = Packages.objects.get(id=pk)
    books = package.books.all()
    context = {'package': package, 'books': books}

    return render(request, 'book_package.html', context)


@login_required(login_url="/login")
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


@login_required(login_url="/login")
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


@login_required(login_url="/login")
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


@login_required(login_url="/login")
def deleteComment(request, pk):
    comment = Review.objects.get(id=pk)
    if Member.objects.get(user=request.user) != comment.member:
        return redirect("home")
    book = comment.book
    if request.method == "POST":
        comment.delete()
        return redirect("book_detail", pk=book.id)
    return render(request, 'book_detail.html', {"comment": comment})


@login_required(login_url="/login")
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


@login_required(login_url="/login")
def deleteOrder(request, pk):
    if not request.user.has_perm("admin"):
        return redirect("home")
    order1 = Order.objects.get(id=pk)
    if request.method == "POST":
        order1.delete()
        return redirect("admin-orders")

    context = {"order1": order1}
    return render(request, 'admin-orders.html', context)


@login_required(login_url="/login")
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
