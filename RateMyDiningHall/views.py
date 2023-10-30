from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import mysql.connector

#connect to mysql db
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="!DaNiEl1807",
    database="menu_db"
)

mycursor = mydb.cursor()
sql="INSERT IGNORE INTO food(name,category) VALUES(%s,%s)"
        
def home(request):
    #keep these variables at none so that we dont get unassigned errors
    menu_data = None
    menu_data_list = ""
    menu_data = dict()
    page_to_scrape = None
    
    #if lothian, get request from lothian menu
    if 'lothian' in request.GET:
        #get request from url
        page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=02&locationName=Lothian%20Residential%20Restaurant&naFlag=1&_gl=1*157j69u*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgzMTcuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgzMTcuMC4wLjA.")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        
        #scrape for data and put into db
        for food in soup.findAll("a", attrs={"name":"Recipe_Desc"}):
            menu_data_list += food.text + "\n"
            menu_data['food'] = menu_data_list
            val=(food.text, "")
            mycursor.execute(sql,val)
        pass
    
    #if glasgow, get request from glasgow menu
    if 'glasgow' in request.GET:
        #get request from url
        page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=03&locationName=Glasgow&naFlag=1&_gl=1*1iyhhso*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        
        #scrape for data and put into db
        for food in soup.findAll("a", attrs={"name":"Recipe_Desc"}):
            menu_data_list += food.text + "\n"
            menu_data['food'] = menu_data_list
            val=(food.text, "")
            mycursor.execute(sql,val)
        pass
    
    #render html to django localhost
    return render(request, 'index.html', {'menu':menu_data})

#commit changes to db
mydb.commit()