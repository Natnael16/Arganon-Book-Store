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


# def create_book(request):
#     pass


@ login_required(login_url="/login")
def create_book(request):
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


def delete_from_cart(request, pk):
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(member=Member.objects.get(user=user))
    order.books.remove(Book.objects.get(id=pk))
    return redirect("cart")


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

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        order = Order.objects.get(member=Member.objects.get(user=user))
        books = order.books.all()
        try:
            amount_dict = request.session["cart"]
        except:
            return redirect("checkout")
        for book in books:
            Quantity.objects.create(
                order=order,
                book=book,
                quantity=amount_dict[str(book.id)]
            )
        del request.session['cart']
        return HttpResponse(request.session["cart"])
        return redirect("home")
    return render(request, 'checkout.html', {'books': books, "order": order, "count": count, "amount": amount_dict, "total": total})


@register.filter
def get_value(dictionary, key):
    return dictionary.get(str(key))
