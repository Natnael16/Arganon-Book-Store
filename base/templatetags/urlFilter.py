from unittest.loader import VALID_MODULE_NAME
from django import template

register = template.Library()
@register.filter(name="removeP")
def removeP(value, arg):
    if value.find('&p=') != -1:
        start = value.find('&p=')
        end = value.find('&', start+1)
        end = end if end != -1 else len(value)+1
        return value[:start]+value[end:]+'&'
    elif value.find('?p=') != -1 or value.find('?') == -1:
        return value.replace('?p='+str(arg), '')+ '?'
    elif value.find('p=') == -1:
        
        return value+'&'
    value.replace('p=','')
    return value+'&'

@register.filter(name="get_item")
def get_item(dictionary, key):
    return dictionary[key]

    
