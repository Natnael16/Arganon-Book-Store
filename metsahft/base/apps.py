from django.apps import AppConfig
from .models import Category

class BaseConfig(AppConfig):
    name = 'base'
    BOOK_CATAGORIES = [
    'ነገረ ማርያም',
    'ነገረ ኢየሱስ',
    'ገድላትና ድርሳናት', 
    'ትምህርተ ሐይማኖት',
    'ስርዐት ቤተ-ክርስቲያን',
    'የዜማ እና የጸሎት',
    'የታሪክ መጻሕፍት',
    'የግዕዝ መጻሕፍት',
    # ('የህጻናት', 'የህጻናት'),
    'ትርጉም መጻህፍት',
    'የተለያዩ',
    ]
    for title in BOOK_CATAGORIES:
        Category.objects.create(name = title )
