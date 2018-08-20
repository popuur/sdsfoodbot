# -*- coding: utf-8 -*-

import urllib
import datetime
from bs4 import BeautifulSoup
from google.appengine.ext import ndb
 
class sds_menu(ndb.Model):
    day_hour = ndb.StringProperty()
    food_day = ndb.StringProperty()
    food_menu = ndb.JsonProperty()


class sdsfood:
    #코1, 코2, 웨스, 탕맛, 가즈, 테킷, 씽푸, 미각, 나폴, 비빈, 아시, 쉐프
    store_id_list = ("E59C", "E59D", "E59E", "E59F", "E59G", "E59H", "E5E6", "E5E7", "E5E8", "E5E9", "E5EA", "E5EB")
    store_name_list = {"E59C":u"[코1]", "E59D":u"[코2]", "E59E":u"[웨스]", "E59F":u"[탕맛]", "E59G":u"[가츠]", "E59H":u"[테킷]"
                       , "E5E6":u"[씽푸]", "E5E7":u"[미각]", "E5E8":u"[나폴]", "E5E9":u"[비빈]", "E5EA":u"[아시]", "E5EB":u"[쉐프]"}
    store_floor_list = {"E59C":u"B1", "E59D":u"B1", "E59E":u"B1", "E59F":u"B1", "E59G":u"B1", "E59H":u"B1"
                   , "E5E6":u"B2", "E5E7":u"B2", "E5E8":u"B2", "E5E9":u"B2", "E5EA":u"B2", "E5EB":u"B2"}

   
    def __init__(self):
        url = 'http://www.sdsfoodmenu.co.kr:9106/foodcourt/menuplanner/list'
        data = urllib.urlopen(url).read()
        self.bs = BeautifulSoup(data, 'html.parser')

    #날짜 가져오기        
    def get_day (self):
        day = self.bs.find("span", {'style' : 'font-size: 13px; color: #d6a066'}).get_text().split()
        return " ".join(day) + "\n"
    
    #오픈일 확인
    def get_open (self):
        result = False
        open = self.bs.find(class_="notice-bold")
        if open :
            result = False
        else :
            result = True
        return result

    #class id로 찾아 파싱
    def get_menu(self, store_str, classId):
        store = self.bs.find("div", class_=classId)
        if store :
            store_list = store.find_all("span", {'style' : 'font-size: 16px;font-weight: bold'})
            num = 0;
            menu_str = ""
            for i in store_list:
                if num > 0 :
                    menu_str += ", "
                menu_str += i.get_text()
                num += 1;
            store = store_str + menu_str +"\n"
        else :
            store = ""
        return store
    
    #class id로 찾아서 메뉴 파싱
    def get_menu_list(self, store_str, classId):
        store = self.bs.find("div", class_=classId)
        menu = []
        if store :
            store_list = store.find_all("span", {'style' : 'font-size: 16px;font-weight: bold'})
            for i in store_list:
                menu.append(store_str+" "+i.get_text())
        return menu
    
    def get_menu_from_parse(self, classId, menu_html, num):
        #0:id, 1:name, 2:material, 3:kcal, 4:img, 5:store_name, 6:floor, 7:order_num
        menu = [] 
        menu.append(classId)
        menu_name = menu_html.find("span", {'style' : 'font-size: 16px;font-weight: bold'})
        menu_material = menu_html.find("span", {'style' : 'font-size: 10px;color: #737373'})
        menu_kcal = menu_html.find("span", {'style' : 'display: inline-block;font-size: 10px;color: #adadad;margin-top: 3px'})
        menu_img = menu_html.find("img")
        
        if menu_name:
            menu.append(menu_name.get_text())
        else : 
            menu.append("")
        if menu_material:
            menu.append(menu_material.get_text())
        else :
            menu.append("")
        if menu_kcal:
            menu.append(menu_kcal.get_text())
        else :
            menu.append("")
        if menu_img:
            menu_img = menu_html.img['src']
            menu.append(menu_img)
        else:
            menu.append("")
        menu.append(self.store_name_list[classId])
        menu.append(self.store_floor_list[classId])
        menu.append(num)
        
        return menu
        
    
    #class id로 받아오고 파싱추가
    def get_menu_list_from_parse(self):
        menu_list = []
        for id in self.store_id_list:
            store = self.bs.find("div", class_=id+"-group-item")
            menu = [] #0:id, 1:name, 2:material, 3:kcal, 4:img, 5:store_name, 6:floor
            if store :
                store_list = store.find_all('tr')
                num = 1
                for i in store_list:
                    menu = self.get_menu_from_parse(id, i, num)                   
                    if menu :              
                        menu_list.append(menu)
                        num += 1
                        
        return menu_list
    
    def put_daily_menu_list_to_db(self, day_list):
        day_db = sds_menu()        
        day_db.day_hour = day_list[0]
        day_db.food_day = day_list[1]
        day_db.food_menu = day_list[2]
        day_db.key = ndb.Key('sds_menu', day_list[0])
        day_db.put()
        

    def check_time(self, hour):
        order = 0
        
        if hour >= 1 and hour < 8 :
            order = 2
        elif hour >= 8 and hour < 20 :
            order = 3
        else :
            order = 1
        return order

    def get_order_time(self):
        dt = datetime.datetime.now()
        day_hour = dt.strftime("%H")
        day_order = self.check_time(day_hour)
        day_num = dt.strftime("%Y%m%d")+"_"+str(day_order)
        return day_num
    
    
    def get_day_list_from_parse(self):
        menu_list = self.get_menu_list_from_parse()
        store_date = self.get_day()
        day_num = self.get_order_time()
        
        day_list = []
        day_list.append(day_num)
        day_list.append(store_date)                        
        day_list.append(menu_list)
        
        return day_list
    
    def put_day_list_to_db(self):
        day_list = self.get_day_list_from_parse()
        self.put_daily_menu_list_to_db(day_list)
        return day_list
    
    def get_day_list_from_db(self):
        day_num = self.get_order_time()
        day_key = ndb.Key('sds_menu', day_num)
        day_menu = []
        day_get = day_key.get()
        
        if day_get :
            day_menu.append(day_get.day_hour)
            day_menu.append(day_get.food_day)
            day_menu.append(day_get.food_menu)
           
        else :
            day_menu = self.put_day_list_to_db()

        return day_menu