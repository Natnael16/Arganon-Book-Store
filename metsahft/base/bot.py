
from telegram import Bot, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import telegram
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
from logging import basicConfig, getLogger, INFO
from .models import *
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text
from .waitlist import wait
from django.urls import reverse

from base.utils import TokenGenerator

basicConfig(level=INFO)
log = getLogger()
Bot = Bot('5106653872:AAE_rQM2_o_AGPBpbiBXTf_rYGVOc3YkOD4')
updater = Updater(token='5106653872:AAE_rQM2_o_AGPBpbiBXTf_rYGVOc3YkOD4', use_context=True)
dispatcher = updater.dispatcher
def start(update, context: CallbackQuery):

    try:
        user = Member.objects.get(chat_id = update.effective_chat.id)
        buttons = [
            [InlineKeyboardButton("Request Book", url='http://127.0.0.1:8000/')], [InlineKeyboardButton("My order status", url='http://127.0.0.1:8000/')],[InlineKeyboardButton("About Us", url='http://127.0.0.1:8000/')],[InlineKeyboardButton("Help", url='http://127.0.0.1:8000/')]
        ]
        msg = str("Hi "+ str(user) +" What can i help you with?")
        context.bot.send_message(chat_id=update.effective_chat.id,
        text = msg,
        reply_markup = InlineKeyboardMarkup(buttons,  resize_keyboard=True))
    

    except(KeyError, Member.DoesNotExist):
        buttons = [
            [KeyboardButton("Send Verifcation Url", True )]
        ]
        msg = str("Hi "+ str(update.effective_chat.first_name) +" Click on Send Verification Url to verify your account!")
        context.bot.send_message(chat_id=update.effective_chat.id,
        text = msg,
        reply_markup = ReplyKeyboardMarkup(buttons,  resize_keyboard=True)) 


def messageHandler(update, context):
    try:
        user = Member.objects.get(phone=update.message.contact.phone_number)
        msg = send_verification(user, update.effective_chat.id)

        context.bot.send_message(chat_id=update.effective_chat.id,text = msg, parse_mode="Markdown")
        

    except (KeyError,Member.DoesNotExist):
        buttons = [
           [InlineKeyboardButton("Go to MenfesawiBooks Website", url='http://127.0.0.1:8000/')]
        ]
        
        msg = str("Fuck You *"+ str(update.message.chat.first_name) +"* \n\n*"+ str(update.message.contact.phone_number) +"* has not been registered on our website or you have not been registered on MenfesawiBooks.com please follow this link and register first!")
        context.bot.send_message(chat_id=update.effective_chat.id,
        text = msg,
        reply_markup = InlineKeyboardMarkup(buttons,  resize_keyboard=True), parse_mode= "Markdown")
    

def help(update, context):
    update.message.reply_text(
        "help for this bot",
        parse_mode="markdown")

def main():
    

    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)
    
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
   
    dispatcher.add_handler(MessageHandler(Filters.contact, messageHandler))
    updater.start_polling()

def send_verification(uid, cid):
    user = uid
   

    uidb64 = urlsafe_base64_encode(force_bytes(user.phone)) 
    cid = urlsafe_base64_encode(force_bytes(cid)) 
    link = reverse('activate', kwargs={'uidb64': uidb64,'cid': cid ,'token':TokenGenerator.make_token(user)})
    activate_url = 'http://127.0.0.1:8000'+link
    message_activation = '*Activate your account*\n'  + ' \nHi *' + str(user) + \
        '*\nplease use this link to verify your account \n' + activate_url + "\n\nif you were not expecting to get this message! Fuckoff"
    return message_activation

def sendmessage(chatid, msg, replymarkup=None):
    dispatcher.bot.send_message(chatid, msg,reply_markup = replymarkup)