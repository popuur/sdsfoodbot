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
        url = 'http://www.sdsfoodmenu.co.kr:9106/foodcourt/menuplanner/list'
        data = urllib.urlopen(url).read()
        bs = BeautifulSoup(data, 'html.parser')
        day = bs.find("span", {'style' : 'font-size: 13px; color: #d6a066'}).get_text().split()
        
        strM = ""
        """       
        allMenu = bs.find_all("span", {'style' : 'font-size: 16px;font-weight: bold'})
        for i, menu in enumerate(allMenu):
            strM += str(i+1) +". "+ menu.get_text() + "\n"
        """
        strB1 = u"\n* B1\n"
        strB2 = ""
        
        b1_kor1 = bs.find("div", class_="E59C-group-item")
        if b1_kor1 :
            b1_kor1 = b1_kor1.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b1_kor1 = u"[코리1] "+b1_kor1+"\n"
            strB1 += b1_kor1
        
        b1_kor2 = bs.find("div", class_="E59D-group-item")
        if b1_kor2 :
            b1_kor2 = b1_kor2.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b1_kor2 = u"[코리2] "+b1_kor2+"\n"
            strB1 += b1_kor2
        
        b1_west = bs.find("div", class_="E59E-group-item")
        if b1_west :
            b1_west = b1_west.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b1_west = u"[웨스] "+b1_west+"\n"
            strB1 += b1_west
        
        b1_tang = bs.find("div", class_="E59F-group-item")
        if b1_tang :
            b1_tang = b1_tang.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b1_tang = u"[탕맛] "+b1_tang+"\n"
            strB1 += b1_tang
        
        b1_gats = bs.find("div", class_="E59G-group-item")
        if b1_gats : 
            b1_gats = b1_gats.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b1_gats = u"[가츠] "+b1_gats+"\n" 
            strB1 += b1_gats
            
        b1_take = bs.find("div", class_="E59H-group-item")
        if b1_take : 
            b1_take = b1_take.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b1_take = u"[테킷] "+b1_take+"\n" 
            strB1 += b1_take
        
        strM += strB1
        
        strB2 = ""
        
        b2_xing = bs.find("div", class_="E5E6-group-item")
        if b2_xing :
            b2_xing = b2_xing.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b2_xing = u"[씽푸] "+b2_xing+"\n"
            strB2 = u"\n* B2\n"
            strB2 += b2_xing
        
        b2_myun = bs.find("div", class_="E5E7-group-item")
        if b2_myun :
            b2_myun = b2_myun.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b2_myun = u"[미각] "+b2_myun+"\n"
            strB2 += b2_myun
            
        b2_poli = bs.find("div", class_="E5E8-group-item")
        if b2_poli :
            b2_poli = b2_poli.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b2_poli = u"[나폴] "+b2_poli+"\n"
            strB2 += b2_poli   
            
        b2_bibi = bs.find("div", class_="E5E9-group-item")
        if b2_bibi :
            b2_bibi = b2_bibi.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b2_bibi = u"[비빈] "+b2_bibi+"\n"
            strB2 += b2_bibi 
            
        b2_asia = bs.find("div", class_="E5EA-group-item")
        if b2_asia :
            b2_asia = b2_asia.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b2_asia = u"[아시] "+b2_asia+"\n"
            strB2 += b2_asia
            
        b2_chef = bs.find("div", class_="E5EB-group-item")
        if b2_chef :
            b2_chef = b2_chef.find("span", {'style' : 'font-size: 16px;font-weight: bold'}).get_text()
            b2_chef = u"[쉐프] "+b2_chef+"\n"
            strB2 += b2_chef    
        
        strM += strB2
            
        strM += u"\n맛있는 식사하세요!"
         
        strMessage = " ".join(day)+"\n"+strM
        dataSend = {
            "message": {
                "text": strMessage
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