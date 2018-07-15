import urllib
from bs4 import BeautifulSoup

class sdsfood:
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