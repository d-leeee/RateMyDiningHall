from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

def home(request):
    menu_data = None
    menu_data_list = ""
    if 'lothian' in request.GET:
        #get URL from UCR dining hall menu
        page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University+of+California%2C+Riverside+Dining+Services&locationNum=02&locationName=Lothian+Residential+Restaurant&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=10%2F28%2F2023")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        #scrape daily food menu
        menu_data = dict()
        for food in soup.findAll("a", attrs={"name":"Recipe_Desc"}):
            menu_data_list += food.text + "\n"
        menu_data['food'] = menu_data_list
        pass
    
    if 'glasgow' in request.GET:
        #get URL from UCR dining hall menu
        page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University+of+California%2C+Riverside+Dining+Services&locationNum=03&locationName=Glasgow&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=11%2F10%2F2023")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        #scrape daily food menu
        menu_data = dict()
        for food in soup.findAll("a", attrs={"name":"Recipe_Desc"}):
            menu_data_list += food.text 
        menu_data['food'] = menu_data_list
        pass
    
    return render(request, 'index.html', {'menu':menu_data})