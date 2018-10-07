# -*- coding: utf-8 -*-

import logging
import random
import time
from flask import Flask, request, jsonify
from datetime import datetime
from sdsfood import sdsfood

app = Flask(__name__)

@app.route('/')
def hello():
    return 'SDS FOOD BOT!'

@app.route('/keyboard')
def Keyboard():
    dataSend = {
        "type": "buttons",
        "buttons": ["잠실식단", "랜덤추천"]
    }
    return jsonify(dataSend)

@app.route('/get_menu')
def GetMenu():
    bs_sdsfood = sdsfood()
    day_list = bs_sdsfood.get_day_list_from_db()
    return jsonify(day_list)

@app.route('/message', methods=['POST'])
def Message():
    dataReceive = request.get_json()
    start = time.time()
    content = dataReceive['content']
    bs_sdsfood = sdsfood()
    str_message = ""
    img_url = ""
    check = bs_sdsfood.get_open()
    menu_db_list = []
       
    if check :
        menu_db_list = bs_sdsfood.get_day_list_from_db()
        str_message += menu_db_list[1]
        if content == u"잠실식단":
            strB1 = u"\n* B1" 
            strB2 = u"\n\n* B2" 
            
            cntB2 = 0
            for menu in menu_db_list[2]:
                if menu[6] == u"B1":
                    if menu[7] == 1 :
                        strB1 += "\n"+menu[5]+" "+menu[1]
                    else :
                        strB1 +=", "+menu[1]
                elif menu[6] == u"B2":
                    if menu[7] == 1 :
                        strB2 += "\n"+menu[5]+" "+menu[1]
                    else :
                        strB2 +=", "+menu[1]
                    cntB2 += 1
            
            str_message += strB1
            if cntB2 > 0:
                str_message += strB2
            
            str_message += u"\n\n맛있는 식사하세요!"
            img_url = random.choice(menu_db_list[2])[4]
            
        elif content == u"랜덤추천":
           
            menu = []
            menu = random.choice(menu_db_list[2])
            str_message += u"\n* "+menu[6]+"\n"+menu[5]+" "+menu[1]
            str_message += "  "
            str_message += menu[3]
            str_message += u"\n\n추천메뉴와 함께 맛있는 식사하세요!"
            img_url = menu[4]
    else :
        str_message = u"즐거운 휴일되세요!"    
    
    end = time.time() - start
    end = str(end)
    if img_url : 
        dataSend = {
            "message": {
               "text": str_message+"\n",
                "photo": {
                    "url": img_url,
                    "width": 600,
                    "height": 400
                  }
            },
            "keyboard": {
                "type": "buttons",
                "buttons": ["잠실식단", "랜덤추천"]
            }
        }
    else :
        dataSend = {
            "message": {
               "text": str_message+"\n"
            },
            "keyboard": {
                "type": "buttons",
                "buttons": ["잠실식단", "랜덤추천"]
            }
        }
    return jsonify(dataSend)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500