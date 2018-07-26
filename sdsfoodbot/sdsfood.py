# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup

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
        
    def get_day (self):
        day = self.bs.find("span", {'style' : 'font-size: 13px; color: #d6a066'}).get_text().split()
        return " ".join(day) + "\n"
    
    def get_open (self):
        result = False
        open = self.bs.find(class_="notice-bold")
        if open :
            result = False
        else :
            result = True
        return result


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
    
    def get_menu_list(self, store_str, classId):
        store = self.bs.find("div", class_=classId)
        menu = []
        if store :
            store_list = store.find_all("span", {'style' : 'font-size: 16px;font-weight: bold'})
            for i in store_list:
                menu.append(store_str+" "+i.get_text())
        return menu
    
    def get_menu_db_list(self):
        menu_list = []
        for id in self.store_id_list:
            store = self.bs.find("div", class_=id+"-group-item")
            menu = []
            if store :
                menu.append(id)
                store_list = store.find_all('tr')
                for i in store_list:
                    #print(i)
                    menu_name = i.find("span", {'style' : 'font-size: 16px;font-weight: bold'})
                    menu_material = i.find("span", {'style' : 'font-size: 10px;color: #737373'})
                    menu_kcal = i.find("span", {'style' : 'display: inline-block;font-size: 10px;color: #adadad;margin-top: 3px'})
                    menu_img = i.img['src']
                    
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
                        menu.append(menu_img)
                    else:
                        menu.append("")
                    menu.append(self.store_name_list[id])
                    menu.append(self.store_floor_list[id])
                    
            if menu :              
                menu_list.append(menu)
        return menu_list