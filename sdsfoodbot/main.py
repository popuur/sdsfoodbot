# -*- coding: utf-8 -*-

import logging
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
        "buttons": ["잠실식단"]
    }
    return jsonify(dataSend)

@app.route('/message', methods=['POST'])
def Message():
    dataReceive = request.get_json()
    content = dataReceive['content']
    if content == u"잠실식단":
        bs_sdsfood = sdsfood()
        str_message = ""
        
        check = bs_sdsfood.get_open()
        if check :
        
            str_message += bs_sdsfood.get_day()
            
            b1_kor1 = bs_sdsfood.get_menu(u"[코1] ", "E59C-group-item")
            b1_kor2 = bs_sdsfood.get_menu(u"[코2] ", "E59D-group-item")
            b1_west = bs_sdsfood.get_menu(u"[웨스] ", "E59E-group-item") 
            b1_tang = bs_sdsfood.get_menu(u"[탕맛] ", "E59F-group-item")
            b1_gats = bs_sdsfood.get_menu(u"[가츠] ", "E59G-group-item")
            b1_take = bs_sdsfood.get_menu(u"[테킷] ", "E59H-group-item")
          
            b2_xing = bs_sdsfood.get_menu(u"[씽푸] ", "E5E6-group-item")
            b2_myun = bs_sdsfood.get_menu(u"[미각] ", "E5E7-group-item")
            b2_poli = bs_sdsfood.get_menu(u"[나폴] ", "E5E8-group-item")
            b2_bibi = bs_sdsfood.get_menu(u"[비빈] ", "E5E9-group-item")
            b2_asia = bs_sdsfood.get_menu(u"[아시] ", "E5EA-group-item")
            b2_chef = bs_sdsfood.get_menu(u"[쉐프] ", "E5EB-group-item")
            
            
            strB1 = u"\n* B1\n" + b1_kor1 + b1_kor2 + b1_west + b1_tang + b1_gats + b1_take
            strB2 = u"\n* B2\n" + b2_xing + b2_myun + b2_poli + b2_bibi + b2_asia + b2_chef 
            
            str_message += strB1
            if b2_xing :
                str_message += strB2
                
            str_message += u"\n맛있는 식사하세요!"
        else :
            str_message = u"즐거운 휴일되세요!"
        dataSend = {
            "message": {
                "text": str_message
            },
            "keyboard": {
                "type": "buttons",
                "buttons": ["잠실식단"]
            }
        }
    elif content == u"도움말":
        dataSend = {
            "message": {
               "text": "도움말인데 클났음"
            },
            "keyboard": {
                "type": "buttons",
                "buttons": ["잠실식단"]
            }
        }
    return jsonify(dataSend)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500