# -*- coding: utf-8 -*-
from twx.botapi import TelegramBot, ReplyKeyboardMarkup, InputFileInfo, InputFile
from bs4 import BeautifulSoup
import requests
import re
import urllib.request

global regx_name
global regx_array
global initStatus
global updates_id

# Define Bot ID
botID = ''
bot = TelegramBot(botID)


# bot.update_bot_info()
# print(bot.username)
# Clean up the status in Program status
def constructor():
    global initStatus, updates_id
    initStatus = True
    updates_id = '0'


def setKeyboard():
    keyboard = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        ['0']
    ]
    reply_markup = ReplyKeyboardMarkup.create(keyboard)
    return reply_markup


# TODO:
# Listener to listen incoming request,
# even there are multiple requests at the same time

def checking_thread():
    global updates_id, initStatus
    # Get content via twx.botapi library
    updates = bot.get_updates(offset=updates_id).wait()
    # Get the latest/last update record
    updates = updates[-1]

    # Check the id is not yet process, process it
    if updates_id != updates[0]:
        updates_id = updates[0]
        # For Debug, Print log message
        print(updates)
        print("\n")

        # Extract information from updates
        message = updates[1]
        senderInfo = message[1]
        content = message[7]
        chatObj = message[3]
        print(content)

        # -----------------
        chat_id = chatObj[0]
        #
        if not initStatus:
            if not (content is None):
                if content.isdigit():

                    html = getWebContentFile(
                        'http://58.177.251.13/acc_management/quote/quote_real.jsp?lang=tchi&txtCode=' + content)

                    price = url_parse_return_price_lists(
                        html,
                        'number_30.*?">(?P<value>[^<>]+?)</td>')

                    # miss = url_parse_return_price_lists(html, '(?P<value>不正確)')
                    # print(price)
                    # print('\n')
                    # print(miss)

                    if not (price == []) | len(content) > 4:
                        # Only get data when price exist
                        name = url_parse_return_price_lists(html, '(?P<value>\[[0-9]+?\][^<>]+?)</td>')
                        # print(name)
                        changes = url_parse_return_price_lists(html, '<span class="number_20[^<>]*?">(?P<value>[^<>]+?)</span>')
                        info = url_parse_return_price_lists(html, '<span class="finfo_tx4">(?P<value>[^<>]+?)</span>')

                        # Response message
                        msg=""

                        try:
                            msg = name[0].strip() + \
                                  '\n現價: ' + price[0].strip() + ' (' + changes[0].strip() + ')' + \
                                  '\n最高價' + info[0].strip() + \
                                  '\t最低價' + info[4].strip() + \
                                  '\n成交金額' + info[1].strip() + \
                                  '\t昨日收市價' + info[2].strip() + \
                                  '\nStock Price data is from REALINK 2016.' + \
                                  '\nThis is not for commercial use, just Academic Purpose'


                        except Exception as e:
                            msg = "Error, Invalid Content"
                            print(e)
                        # Send the msg out
                        bot.send_message(chat_id, msg).wait()

                    else:
                        bot.send_message(chat_id, 'Invalid Content! Please enter stock Number').wait()

        else:
            initStatus = False

        print('================================')


def getWebContentFile(_url):
    r = requests.get(_url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


# Find particular content from assigned url
def url_parse_return_price_lists(soup, _regx):
    # regular expression part
    # "<(?P<parameter>.+)>"
    regx = re.compile(_regx)
    result = regx.finditer(soup.prettify())
    item = []
    for tag in result:
        item.append(tag.group('value'))
    return item


# ----------------------------------------------------
constructor()
while True:
    checking_thread()
