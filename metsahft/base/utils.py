from pyexpat.errors import messages
from django.shortcuts import redirect, render
import requests
from .models import *
from django.contrib import messages


def payment(request, items, id):
    """
    merchant ID will be the dudes ID,
    merchant order id will be the id of the order,
    it will expire after and hour or so,
    we will put the items in a list of dictionaries.
    """
    obj = {
        "process": "Cart",
        "successUrl": "http://localhost:8000/success",
        "ipnUrl": "http://localhost:8000/ipn",
        "cancelUrl": "http://localhost:8000/cancel",
        "merchantId": "SB1475",
        "merchantOrderId": str(id),
        "expiresAfter": 1,
        "items": items,
        "totalItemsDeliveryFee": 0,
        "totalItemsTax1": 0
    }
    return requests.post("https://test.yenepay.com/", obj)
