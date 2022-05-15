
from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name = "home"),
    path("login/", loginPage, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("register/", registerPage, name="register"),
    path("create_book/", create_book, name="create_book"),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),

    path('equb-user',equb_user ,name='equb-user' ),
  
    path('create-package', create_package, name = 'create-package'),
    path('request-books' , request_books , name = 'request_books'),
    path('book-package/<str:pk>', single_package , name = 'book-package'),
    path('books', books, name='books'),
    path('listOfUsers' , listOfUsers , name = 'list-of-users'),
    path("book_detail/<str:pk>/", bookDetail, name="book_detail"),
    path("delete_comment/<str:pk>", deleteComment, name="delete_comment"),
    path("admin-orders/", adminOrders, name="admin-orders"),
    path("admin-orders/delete-order/<str:pk>", deleteOrder, name="delete-order"),
    path("detail-order/<str:pk>", detailOrder, name="detail-order"),
    path("edit-profile/", editProfile, name="edit-profile"),

    path('delete_request/<str:pk>' , delete_request , name = 'delete_request'),
    path("verify/<uidb64>/<token>", verify, name="verify"),
    path("resetPassword/<uidb64>/<token>", resetPassword, name="resetPassword"),
    path("forgotpassword", sendreset, name="sendreset"),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
    path('ipn/', ipn, name='ipn'),
    path('logout', logout),
     path("add-equbtegna" , addEqubtegna , name= "add-equbtegna" ) , 
    path('book-package/<str:pk>', single_package, name='book-package'),

    path('equbreset' , reset , name='equb-reset' )
]

