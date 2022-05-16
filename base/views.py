
import json

import random

from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import CharField
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from telegram import ReplyKeyboardRemove
from base.utils import TokenGenerator
from .models import *
from .forms import *
from django.core.paginator import *
from django.core.paginator import Paginator
from collections import defaultdict
from .wait import toBeVerified
from .bot import main, sendmessage
from collections import defaultdict
# from email import message
# from email.policy import default
# from http.client import HTTP_PORT
from django.template.defaulttags import register
import requests
from .utils import *
# Create your views here.

main()

def home(request):
    books = Book.objects.filter(Q(count__gt = 0)).order_by('-popularity')
    newbooks = Book.objects.filter(Q(count__gt = 0)).order_by('-created')
    newbooks1 = newbooks[:max(3, len(newbooks)//2)]
    newbooks2 = newbooks[max(3, len(newbooks)//2):]
    return render(request, "home.html", {"books": books, "newbooks1": newbooks1, "newbooks2": newbooks2})


def verify(request, uidb64, token):
    user = None
    uid = force_str(urlsafe_base64_decode(uidb64))
    #print(uid)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        #print(uid)
        user = toBeVerified.get(uid)['user']
    except Exception as e:
        return HttpResponse("Invalid Token or Registration time expired")

    #print(user,TokenGenerator.check_token(user, token))
    if user and TokenGenerator.check_token(user, token):
        member = toBeVerified.get(uid)['member']
        user.save()
        member.user = user
        member.chat_id = toBeVerified.get(uid)['chat_id']
        member.save()
        
      
        sendmessage(member.chat_id, "በትክክል ተመዝግበዋል!", ReplyKeyboardRemove())
        return redirect('login')
        return HttpResponse("Thank you for verifying "+ str(user))
    return HttpResponse("login")

def loginPage(request):
    
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        if len(phone) < 9 or len(phone)> 13:
            errors ="Phone Number or password is wrong"
            return render(request, "login.html", {"errors": errors})

        pre = len(phone) - 9
        phone = phone[pre:]
        phone = "+251" + phone
        user = None
        try:
            member = Member.objects.get(phone=phone)
            # return HttpResponse(member.user.username)
            user = authenticate(
                username=member.user.username, password=password)
        except:
            user = None
            errors ="Phone Number or password is wrong"
            print('errros 1' , errors)
            return render(request, "login.html", {"errors": errors})

        #print(user, 'I am user')
        if user:
            login(request, user)
            return redirect("home")
        else:
            errors = "Phone Number or password is wrong"
            print('errors 2')
            return render(request, "login.html", {"errors": errors})
    return render(request, "login.html")




@login_required(login_url="/login")
def logoutUser(request):
    logout(request)
    return redirect("home")

def resetPassword(request, uidb64=None, token=None):
    password = None
    if request.method == "POST":
        usr = ResetForm(request.POST)
        # usr = ResetForm()
        if usr.is_valid():
            password = request.POST.get("password1")
            user = None
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                #print(uid)
                user = Member.objects.get(phone=uid).user
            except Exception as e:
                return HttpResponse("<h1>ደንበኛው አልተገኘም</h1>")
            
            if user and TokenGenerator.check_token(user, token):
                user.set_password(password)
                user.save()
                # usr.save()
                return redirect("login")
            return HttpResponse("password Reset Failed")
        else:
            # return HttpResponse(str(usr.errors))
            return render(request, "resetpassword.html", { 'user_error': usr.errors})
            
    context = {"uidb64": uidb64, "token": token}
    return render(request, "resetpassword.html",context)

def sendreset(request):
    if request.method == "POST":
        phone = request.POST.get("resetphone")
        pre = len(phone) - 9
        phone = phone[pre:]
        phone = '+251' + phone
        member = Member.objects.get(phone=phone)
        user = member.user
        uidb64 = urlsafe_base64_encode(force_bytes(phone)) 
        link = reverse('resetPassword', kwargs={'uidb64': uidb64,'token': TokenGenerator.make_token(user)})
    
        activate_url = 'http://127.0.0.1:8000'+ link
        message = '*Reset Password*\n'  + ' \nHi *' + str(user) + \
        '*\nplease use this link to reset your password \n' + activate_url + "\n\nif you were not expecting to get this message Ignore it!"
        sendmessage(member.chat_id,message)

        # HttpResponse("password link sent to your telegram account")
        return redirect('https://t.me/menfesawi_metsahft_bot')
    return render(request, "forgot.html")


def registerPage(request):
    usr = UserForm()
    form = MemberForm()
    
    if request.method == "POST":

        usr = UserForm(request.POST)
        form = MemberForm(request.POST)
        # form.user = usr
        #print(usr.is_valid(), form.is_valid())
        #print(form, "this is the form" , usr)
        if usr.is_valid() and form.is_valid():
            user = usr.save(commit=False)
            username = request.POST.get("username")
            member = form.save(commit=False)
            
            member.is_equbtegna = False
            phone = request.POST.get("phone")[-9:]
            phone  = "+251" + phone
            toBeVerified.add(phone, {'member': member, 'user': user}, 600 )
            # login(request, User.objects.get(username=username))
            return redirect('https://t.me/menfesawi_metsahft_bot')

        else:
            # #print(usr, form)

            return render(request, "register.html", { 'user_error': usr.errors , 'form_error' : form.errors})
            return HttpResponse("{} {}".format(usr.errors, form.errors))
            return HttpResponse("Here's the text of the web page.")
            messages.error(request, "An error occurred during registration")
    context = {
        "user": usr,
    }
    return render(request, "register.html", context)




@login_required(login_url="/login")
def editProfile(request):
    user = request.user
    member = Member.objects.get(user = user)
    member_form = MemberForm(instance=member)
    #print(member_form)
    if request.method == "POST":
        member_form = MemberForm(
            request.POST, instance=Member.objects.get(user=request.user))
        ##print(member_form.is_valid())
        if member_form.is_valid():
            member_form.save()
            member = Member.objects.get(user = user)
            return render(request, 'user_profile.html', {"member" : member , 'success': 'success' })
        else:
            # return HttpResponse("this shit is invalid YO")
            err = messages.error(request, "One or more invalid fields")
            return render(request , 'user_profile.html' , {'member': member , 'error' : err})

    context = {"member_form": member_form, 'member': member}
    return render(request, 'user_profile.html', context)


@login_required(login_url="/login")
def create_book(request):
    if not request.user.has_perm("admin"):
        return redirect("home")
    form = BookForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        # return HttpResponse(request.FILES.get("image_front"))
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # return HttpResponse(request.FILES.get("image_front"))
            form.save()

            return redirect("home")
        else:
            #print(form)
            e = form.errors
            return render(request , 'create-book.html' , {'form': form, "categories": categories , 'error':e})

    r_books = Request.objects.all()
    return render(request, 'create-book.html', {'form': form, "categories": categories , 'r_books' : r_books})

def cart(request):
    if request.method == "POST":
        return redirect("checkout")
    return render(request, 'shopping-cart.html', {'books': books})


@ login_required(login_url="/login")
def checkout(request):
    if request.method == 'POST':
        member = Member.objects.get(user=request.user)
        order = Order.objects.create(
            member=member , delivery = request.POST.get("delivery"))
        cart = json.loads(request.POST.get("cart"))
        amount_dict = defaultdict(int)
        package_amount = defaultdict(int)
        items = []
        books = []
        packages = []
        for item in cart:
            def validate_book(id):
                try:
                    book = Book.objects.get(id=id)
                    if amount_dict[str(book.id)] > book.count:
                        messages.error(request, "Sorry the amount of books you have reqeusted for the book {} with amount {} is less than the amount you have requested which is {}.".format(
                            book.title, book.count, amount_dict[str(book.id)]))
                except:
                    messages.error(request, "Item with id {} is invalid", id)
                    return redirect("checkout")

            def validate_package(id):
                try:
                    package = Packages.objects.get(id=id)
                    books = package.books.all()

                    if package_amount[str(package.id)] > package.amount:
                        messages.error(request, "Sorry the amount of books you have reqeusted for the book {} with amount {} is less than the amount you have requested which is {}.".format(
                            book.title, book.count, amount_dict[str(book.id)]))

                    #print("the books are", books)
                    for book in books:
                        amount_dict[str(book.id)
                                    ] += package_amount[str(package.id)]
                        validate_book(book.id)
                except:
                    messages.error(
                        request, "Item {} is invalid", item["title"])
                    return redirect("checkout")

            if "id" not in item or "package" not in item or "qty" not in item:
                messages.error(request, "Item {} is invalid", item["title"])
                return redirect("checkout")
            type = item["package"]

            if type == "false":
                #print("tis a book")
                amount_dict[item["id"]] += int(item["qty"])
                validate_book(item["id"])
                #print("it's valid")
                book = Book.objects.get(id=item["id"])
                books.append((book, amount_dict[str(book.id)]))
                items.append(
                    {
                        "itemId": str(book.id),
                        "itemName": str(book.title),
                        "unitPrice": str(book.price),
                        "quantity": str(amount_dict[str(book.id)])
                    }
                )

            elif type == "true":
                item["id"] = str(int(item["id"]))
                #print("tis a package, with id", item["id"])
                #print("has quantity", int(item["qty"]))
                package_amount[item["id"]] += int(item["qty"])
                #print("package amount is", package_amount)
                validate_package(item["id"])
                package = Packages.objects.get(id=item["id"])
                packages.append((package, package_amount[item["id"]]))
                items.append(
                    {
                        "itemId": str(package.id),
                        "itemName": str(package.title),
                        "unitPrice": str(package.discount),
                        "quantity": str(package_amount[str(package.id)])
                    }
                )

        if not items:
            messages.error(request, "There are no Items in your cart")
            redirect("checkout")
        #print("items are", items)
        url = "https://testapi.yenepay.com/api/urlgenerate/getcheckouturl/"
        data = {
            "process": "Cart",
            "successUrl": "http://localhost:8000/success",
            "ipnUrl": "http://localhost:8000/ipn",
            "cancelUrl": "http://localhost:8000/cancel",
            "merchantId": "SB1475",
            "merchantOrderId": str(order.id),
            "expiresAfter": 2,
            "items": items,
            "totalItemsDeliveryFee": 0,
            "totalItemsTax1": 0
        }
        response = requests.post(url=url, json=data)
        #print(response.status_code)
        if response.status_code == 200:
            for book in books:
                order_book = OrderBook.objects.create(
                    member=member, book=book[0], quantity=book[1])
                order.books.add(order_book)
            for package in packages:
                order_package = OrderPackage.objects.create(
                    member=member, package=package[0], quantity=package[1]
                )
                order.packages.add(order_package)
            result = response.json().get("result")
            return redirect(result)
        else:
            order.delete()
            messages.error(
                request, "Error has been encountered, Post request has Failed")
            redirect("checkout")
    return render(request, 'checkout.html')

@login_required(login_url="/login")
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
        #print("It's Paid")
        order = Order.objects.get(id=moi)
        books = order.books.all()
        packages = order.packages.all()
        for order_book in books:
            book = order_book.book
            final_book = Book.objects.get(id=book.id)
            final_book.count -= int(order_book.quantity)
            final_book.save()
        for order_package in packages:
            package = order_package.package
            for book in package.books.all():
                final_book = Book.objects.get(id=book.id)
                final_book.count -= int(order_package.quantity)
                final_book.save()
            package.amount -= int(order_package.quantity)
            package.save()
        # order.save(commit = False)
        order.paid = True
        order.save()
    else:
        messages.error(request, "Payment incomplete")
        return redirect("checkout")
        #print('Invalid payment process')
    return render(request, 'success.html', {'total': total, 'status': status, "id": ti})

def cancel(request):
    return redirect("cart")


def ipn(request):
    messages.success("the ipn request has been successful")
    #print("the ipn thing has been successful")
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
        # print("It's Paid")
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


@ register.filter()
def subtract(value1, value2):
    return value1 - value2

@login_required(login_url="/login")
def equb_user(request):
    cur_year = ethiopian_date.EthiopianDateConverter(
    ).date_to_ethiopian(datetime.date.today())
    cur_year = cur_year[0]

    form_year = request.GET.get('year')
    ##print(form_year)
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
    user = User.objects.get(id = request.user.id)
    member = Member.objects.get(user = user)
    # I am assuming the equbtegna is authenticated
    equbtegna =  Equbtegna.objects.get(member = member) if Equbtegna.objects.count() > 0 else None
    equbtype = str(equbtegna.equb) if equbtegna else ''
    equboch= Equb.objects.all()
    return render(request, 'equb(back).html' ,{ "equboch" : equboch , 'equbtegna' : equbtype  })

# choosen_books = []

@login_required(login_url="/login")
def create_package(request):
    if not request.user.has_perm("admin"):
        return redirect("home")
    if Book.objects.count() < 1: return HttpResponse('<h2> መጀመሪያ መጻሕፍትን ያስገቡ!</h2>')
    q = request.GET.get("q") if request.GET.get('q') != None else ''
    books = Book.objects.filter((Q(title__icontains = q) | Q(author__icontains = q)) & Q(count__gt = 0))
    
    if request.method == 'POST':
        
      
        add_or_remove = request.POST.get('add_or_remove')
        if request.POST.get('create_package') == 'create_package':

            title = request.POST.get('title')
            discount = request.POST.get('price')
            price = request.POST.get('old-price')
            description = request.POST.get('description')
            books_ = request.session['added_books']
            
            package = Packages(
                title = title,
                discount = discount,
                price = price,
                description = description,
                
            )
          
            
            if title and discount and price and books_ :

                package.save()
                package.books.set(books_)
                ##print(package)
                package.save()
                request.session['added_books'].clear()
                request.session.modified = True

                return redirect('/books#packages')
            else:
# 
                return redirect('create-package')
            
        if add_or_remove == 'add':
            id = request.POST.get('id')
            book_by_id = Book.objects.get(id = id)


            if 'added_books' in request.session:
                if str(book_by_id.id) not in request.session['added_books']:
                    request.session['added_books'].append(str(book_by_id.id))
            else:
                request.session['added_books'] = [str(book_by_id.id)]

            request.session.modified = True
        if add_or_remove == 'remove':
            id = request.POST.get('id')
            book_by_id = Book.objects.get(id = id)
        
            if str(book_by_id.id) in request.session['added_books']:
                request.session['added_books'].remove(str(book_by_id.id))
            request.session.modified = True
        
    choosen_books = Book.objects.filter(id__in = request.session['added_books'] if 'added_books' in request.session else [])
    context = {'books' : books , 'choosen_books' : choosen_books}
    return render(request , 'create-package(back).html', context)


@login_required(login_url="/login")
def request_books(request):
    successful = 'False'
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        if title:
            if Request.objects.count() <= 40000:
                requested_book = Request.objects.get_or_create(title = title , author = author)
                successful = "True"
            return redirect('books')
    
    context = {'successful':successful}
    return render(request , 'request_books.html', context)




def single_package(request,pk):
    
    package = Packages.objects.get(id = pk)
    books = package.books.all()
    ##print(books, 'all books in apackage')
    context = {'package' : package , 'books':books}

    return render(request, 'book_package.html' , context )


def books(request):
    def isFloat(num):
       
        try:
            num = float(num)
            ##print(num)
            if type(num) == float:
                return True
        except ValueError:
            return False
        except TypeError:
            return False
        return False
    def isInt(num):
        try:
            num = int(num)
        
            if type(num) == int:
                return True
        except ValueError:
            return False
        except TypeError:
            return False
        return False

    const = 8
    order = {1:'-popularity',2:'-created'}
    category = Category.objects.all()
    q = request.GET.get('q') if request.GET.get('q') else ''
    sort = request.GET.get('sort', 1) if isInt(request.GET.get('sort', 1)) and int(request.GET.get('sort', 1)) in order else 1

    c = request.GET.getlist('category') if request.GET.getlist('category') else category
    pr = [request.GET.get('price-min') if isFloat(request.GET.get('price-min')) else 0, request.GET.get('price-max') if isFloat(request.GET.get('price-max')) else 5000]
    p = request.GET.get('p') if isInt(request.GET.get('p')) else 1
    c = set(map(str, c))
    books = []
    p = int(p)
    ##print(q,sort, c, pr,p)
    sort = int(sort)
    # booksbycategory = defaultdict(int)
    # 
    # for i in category:
    #     booksbycategory[i] = len(Book.objects.filter(
    #         Q(Q(title__icontains = q)|Q(author__icontains = q)|Q(description__icontains = q))&
    #          Q(price__gt = float(pr[0])-1) & Q(price__lt = float(pr[1])) &Q(new_book =False)
    #     ))
    
    
    # # books = Book.objects.filter(
    # #         Q(Q(title__icontains = q)|Q(author__icontains = q)|Q(description__icontains = q))&
    # #          Q(price__gt = float(pr[0])-1) & Q(price__lt = float(pr[1])) & Q(categories__in = c)&Q(new_book =False)
    # #     ).order_by(order[sort])
   

########################################################33333
    booksbycategory = defaultdict(list)
    sort = int(sort)
    for i in category:
        booksbycategory[i] = list(Book.objects.filter(
            Q(
                Q(title__icontains = q)|Q(author__icontains = q)|Q(description__icontains = q)
            )&
             Q(price__gt = float(pr[0])-1) & Q(price__lt = float(pr[1]))&Q( categories__name = str(i)) &Q(new_book =False)&Q(count__gt = 0)
        ))
    books = set()
    
    for i in booksbycategory:
        
        if str(i) in c:
            books.update(booksbycategory[i])
        booksbycategory[i] = len(booksbycategory[i])

    books = list(books)
    
    books.sort(key=lambda x: x.popularity, reverse=True) if sort == 1 else books.sort(key=lambda x: x.created, reverse=True)
    
 #########################################################################333  

   
    newBooks = Book.objects.filter(new_book = True)
    category = Category.objects.all()
    #### testing 
    books = books
    newBooks = list(newBooks)
    page = request.GET.get('p', 1)

    paginator = Paginator(books, 40)
    #print('paginao')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    books1 = list(set(books[:len(books)//4]))
    books2 = list(set(books[len(books)//4 : len(books)//2]))
    books3 = set(books[len(books)//2 : (len(books)*3)//4])
    books4 = set(books[(len(books)*3)//4 : len(books)])
    print(books1 , books2)
    context = {"books": books,"books4": books4,"books3": books3,"books2": books2,"books1": books1, 'p': p,"strp": str(p),'paginator':paginator, 
    "newBooks": newBooks, "minprice": pr[0], 'maxprice': pr[1], 'category':category, 
    'bNo':booksbycategory, 'checkedBox': c, 'sort': sort, 'q':q}
    packages = set(Packages.objects.all())
    exclude = []
    for package in packages:
        for singleBook in list(package.books.all()):
            if singleBook.count <= 0:
                exclude.append(package)
    for ex in exclude:
        packages.discard(ex)
    exclude = []

    context['packages'] = packages
    #print(packages)
    return render(request, "metsahft.html", context)

@login_required(login_url="/login")
def reset(request):
    if not request.user.has_perm("admin"):
        return redirect("home")
    context = {}
    level = request.GET.get("l") if request.GET.get("l") else ''
    print(level)
    membersWithDept = Equbtegna.objects.filter(
        Q(unpaid_month__gt = 0)& (Q(equb__type = level) if level != '' else Q(equb__type__icontains = level))
        )
    equb = Equb.objects.all()
    winners = None
    context["inDept"]= membersWithDept
    context["winners"] = winners
    context["equb"] = equb
    context['l'] = level
    context['message'] = "The equb round has been Reseted "
    context['reset'] = False
    if request.method == "POST":
        type = request.POST.get("type")
        print(request.POST)
        curequb = Equb.objects.get(type__exact = type)
        curequb.currentRound += 1
        curequb.save()
    return redirect('list-of-users')

@login_required(login_url="/login")
def listOfUsers(request):
    if not request.user.has_perm("admin"):
        return redirect("home")
    context = {}
    level = request.GET.get("l") if request.GET.get("l") else ''
    ##print(level)
    membersWithDept = Equbtegna.objects.filter(
        Q(unpaid_month__gt = -1)& (Q(equb__type = level) if level != '' else Q(equb__type__icontains = level))
        )
    equb = Equb.objects.all()
    winners = None
    context["inDept"]= membersWithDept
    context["winners"] = winners
    context["equb"] = equb
    context['l'] = level
    context['message'] = None
    if request.method == "POST":
        
        num = int(request.POST.get("num"))
        type = request.POST.get("type")
        curequb = None
        try:
            curequb = Equb.objects.get(type__exact = str(type))
        except Equb.DoesNotExist:
            context["message"] = "ምንም እቁብ አልተመዘገበም"
            return render(request, "listOfUsers.html", context)
        
        ekubtegna  = Equbtegna.objects.filter(equb__type = type)
        ekubtegna = set(ekubtegna) if ekubtegna != None else set()
        context['type'] = type
        prevWinners = Winner.objects.filter( Q(equbtegna__equb__type = type) & Q(round = curequb.currentRound))
       
        context["reset"] = True if ekubtegna else False
        for i in prevWinners:
            ##print(i.equbtegna)
            if i.equbtegna in ekubtegna:
                ekubtegna.remove(i.equbtegna)
        # for i in range(len(prevWinners
        #     prevWinners[i] = prevWinners[i].equbtegna.id
        # prevWinners = set(prevWinners)
    
        ##print(ekubtegna)
        winner = Winner()  
        winners = []
        
        for i in range(min(num, len(ekubtegna))):
            lucky = random.choice(tuple(ekubtegna))
            ##print(ekubtegna)
            winner.year = ethiopian_date.current_year()[0]
            winner.month = ethiopian_date.current_year()[1]
            winner.equbtegna = lucky
            winner.round = curequb.currentRound
            winner.save()
            winners.append(winner)
            winner = Winner()
            ekubtegna.remove(lucky)
            
    
        context["winners"]= winners
        context["message"] = "every one has won on this round please start the next round  to proceed " if prevWinners else "there are no equbtegnas please wait until there are until they Register"
        
        return render(request, "listOfUsers.html", context)
    allequb = Equb.objects.all()
    context['allequb'] = allequb
    return render(request, "listOfUsers.html", context)
        


def bookDetail(request,pk):
    book = Book.objects.get(id=pk)
    comments = book.review.all()
    all_books = Book.objects.all()
    comment_paginator = Paginator(comments, 4)
    page_num = request.GET.get("page")
    page =  comment_paginator.get_page(page_num)
    cats = list(book.categories.all())
           
    related_books = Book.objects.filter(categories = book.categories.all()[0])
    
    ##print(related_books)
    if request.method == "POST":
        comment_form = ReviewForm(data = request.POST)
        #print(Member.objects.get(user = request.user))
        if comment_form.is_valid():
            comment = request.POST.get('አስተያየት')
            review = Review.objects.get_or_create(
                member = Member.objects.get(user = request.user ), 
                book = book,
                አስተያየት = comment    
            )
            comment_form = ReviewForm()
            return redirect('/book_detail/{}'.format(pk))
            # review.save()
  
    comment_form = ReviewForm()
    ##print(book.categories)
    context = {"book":book, "comments":comments, 
                "comment_form":comment_form, "page":page,
                "cats":cats, "related_books":related_books
               }
    return render(request,'book_detail.html', context)
  
    
@login_required(login_url="/login")
def deleteComment(request,pk):
    comment = Review.objects.get(id = pk)
    if Member.objects.get(user=request.user) != comment.member:
        return redirect("home")
    book = comment.book
    if request.method == "POST":
        comment.delete()
        return redirect("book_detail", pk=book.id )
    return render(request, 'book_detail.html', {"comment":comment})



@login_required(login_url="/login")
def deleteOrder(request,pk):
    if not request.user.has_perm("admin"):
        return redirect("home")
    order1 = Order.objects.get(id = pk)
    if request.method == "POST":
        order1.delete()
        return redirect("admin-orders")  
    
    context={"order1":order1}
    return render(request, 'admin-orders.html', context)





@login_required(login_url='login')
def delete_request(request , pk):
    if not request.user.has_perm("admin"):
        return redirect("home")
    if request.method == "POST":
        req = Request.objects.get(id = pk)
        req.delete()
        return redirect('create_book')

@login_required(login_url="/login")
def adminOrders(request):
    if not request.user.has_perm("admin"):
        return redirect("home")
    price = {}
    qty = {}
    order_price = {}
    q = request.GET.get('q') if request.GET.get('q') else ""
    orders =list(Order.objects.filter(
        Q(member__user__username__icontains = q) |
        Q(id__icontains = q) |
        Q(member__phone__icontains = q)
        
        ).exclude(paid = False).exclude(sold = True))
    for order in orders:
        orderPrice =0
        for order_book in order.books.all():
            quantity= order_book.quantity
            price  = order_book.book.price * quantity
            orderPrice += price

        for order_package in order.packages.all():
            quantity= order_package.quantity
            price  = order_package.package.discount * quantity
            orderPrice += price
        
        order_price[order] = orderPrice
    selected = 0
    if  request.GET.get("delivery") == "2":
        orders = Order.objects.filter(delivery = True,sold = False , paid = True)
        selected = 2
    elif request.GET.get("delivery") == "1":
        orders = Order.objects.filter(delivery = False ,sold = False , paid = True)
        selected = 1
    
    context = {"orders":orders, "selected":selected, "order_price": order_price}
    return render(request, 'admin-orders.html', context)

@login_required(login_url="/login")
def detailOrder(request, pk):
    if not request.user.has_perm("admin"):
        return redirect("home")
    qty = {}
    price = {}
    order = Order.objects.get(id = pk)
    order_books = order.books.all()
    order_packages = order.packages.all()


    orderPrice = 0
    for order_book in order.books.all():
            quantity= order_book.quantity
            price  = order_book.book.price * quantity
            orderPrice += price

    for order_package in order.packages.all():
        quantity= order_package.quantity
        price  = order_package.package.discount * quantity
        orderPrice += price

    # for bok in books:
    #     qty[bok]= Quantity.objects.get(book = bok).quantity
    #     price[bok] = bok.price * qty[bok]
    # total = 0
    #print(orderPrice)
    # for book in books:
    #     total += price[book] 
    context ={"order":order, "order_books":order_books,"order_packages":order_packages, "total":orderPrice}
    return render(request, 'detail-order.html', context)

# needs validation and success messsasge
@login_required(login_url="/login")
def addEqubtegna(request):
    if not request.user.has_perm("admin"):
            return redirect("home")
    if request.method == 'POST':
        phone = request.POST.get('memberPhone')
        try:
            member = Member.objects.get(phone = phone)
        except:
            return redirect('list-of-users')
        equb = request.POST.get('equbType')
        
        if member and equb:
            e = Equbtegna()
            e.member = member
            e.equb = Equb.objects.get(type = equb)
            if e not in Equbtegna.objects.all():
                e.save()
            
            return redirect('list-of-users')

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)




