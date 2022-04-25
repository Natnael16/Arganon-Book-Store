from django import views
from django.contrib import admin
from django.urls import path, include
from .views import *
from .utils import *

urlpatterns = [
    path('', home, name="home"),
    path("login/", loginPage, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("register/", registerPage, name="register"),
    path("create_book/", create_book, name="create_book"),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path("add-package-to-cart/<str:pk>",
         add_package_to_cart, name="add-package-to-cart"),
    path("add-to-cart/<str:pk>", add_to_cart, name="add-to-cart"),
    path("remove_package/<str:pk>",
         delete_package_from_cart, name="remove_package"),
    path("remove_book/<str:pk>", delete_from_cart, name="remove_book"),
    path('equb-user', equb_user, name='equb-user'),
    path('equb-choice', equb_choice, name='equb-choice'),
    path('create-package', create_package, name='create-package'),
    path('request-books', request_books, name='request_books'),
    path('book-package/<str:pk>', single_package, name='book-package'),
    path('books', books, name='books'),
    path('list-of-users', listOfUsers, name='list-of-users'),
    path("book_detail/<str:pk>/", bookDetail, name="book_detail"),
    path("delete_comment/<str:pk>", deleteComment, name="delete_comment"),
    path("admin-orders/", adminOrders, name="admin-orders"),
    path("admin-orders/delete-order/<str:pk>",
         deleteOrder, name="delete-order"),
    path("detail-order/<str:pk>", detailOrder, name="detail-order"),
    path("user-profile/", userProfile, name="user-profile"),
    path("edit-profile/", editProfile, name="edit-profile"),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
    path('ipn/', ipn, name='ipn'),
    path('book-package/<str:pk>', single_package, name='book-package'),
    path("all-packages", all_packages, name="all-packages"),
]
