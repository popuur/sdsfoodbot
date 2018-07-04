# -*- coding: utf-8 -*-

import logging
from flask import Flask, request, jsonify
from datetime import datetime
import urllib
from bs4 import BeautifulSoup

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
        data = urllib.urlopen('http://www.sdsfoodmenu.co.kr:9106/foodcourt/menuplanner/list').read()
        bs = BeautifulSoup(data, 'html.parser')
        g = bs.find_all("span", {'style' : 'font-size: 16px;font-weight: bold'})
        a = ""
        for i, menu in enumerate(g):
            a += str(i+1) +". "+ menu.get_text() + "\n"
            
        a += u"\n맛있는 식사하세요!"
        dataSend = {
            "message": {
                "text": a
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