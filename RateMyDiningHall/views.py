#
#
#
# WEB SCRAPER USING BEAUTIFUL SOUP
#
#
#

import mysql.connector
from bs4 import BeautifulSoup
import requests

#connect to mysql db
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="!DaNiEl1807",
    database="menu_db"
)

mycursor = mydb.cursor()
sql="INSERT IGNORE INTO food(name,category) VALUES(%s,%s)"


#get URL from UCR dining hall menu
page_to_scrape = [requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=02&locationName=Lothian%20Residential%20Restaurant&naFlag=1&_gl=1*157j69u*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgzMTcuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgzMTcuMC4wLjA."),
                  requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=03&locationName=Glasgow&naFlag=1&_gl=1*1iyhhso*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.")]
i=0
for times in page_to_scrape:  
    soup = BeautifulSoup(page_to_scrape[i].text, "html.parser")
    i+=1
    
    #since lothian doesn't serve on weekends, there must be a try and except to eleminate errors when no tables appear
    try:
        #find all div elements inside the table
        food_table = soup.find('table', attrs={"bordercolorlight":"black"})
        food_rows = food_table.findAll('div')
        
        #iterate through every single div element to check for category/food
        for category in food_rows:
            #if the div class is a category set it equal to cats
            if category['class'][0] == 'shortmenucats':
                cats = category.find('span', attrs={"style":"color: "})
            #if the div class is a food set it equal to food and add it to database
            elif category['class'][0] == 'shortmenurecipes':
                food = category.find('a', attrs={"name":"Recipe_Desc"})
                val = (food.text, cats.text)
                mycursor.execute(sql,val)
    except:
        continue
    
#commit changes
mydb.commit()

#
#
#
# RENDER HTML AND DINING MENU 
#
#
#

from django.shortcuts import render

def home(request):
    
    #keep these variables at none so that we dont get unassigned errors
    menu_data_breakfast = []
    menu_data_lunch = []
    menu_data_dinner = []
    page_to_scrape = None
    
    #if lothian, get request from lothian menu
    if 'lothian' in request.GET:
        #get request from url
        page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=02&locationName=Lothian%20Residential%20Restaurant&naFlag=1&_gl=1*157j69u*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgzMTcuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgzMTcuMC4wLjA.")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        
        #scrape for data and put into db for breakfast, lunch, and dinner
        full_table = soup.find("table", attrs={"bordercolorlight":"black"})
        food_day_tables = full_table.findAll("td", attrs={"width":"30%"})
        for table in food_day_tables:
            food_day = table.find("div", attrs={"class":"shortmenumeals"}).text
            foods = table.findAll('a', attrs={"name":"Recipe_Desc"})
            if food_day == "Breakfast":
                for food in foods:
                    menu_data_breakfast.append(food.text)
            elif food_day == "Lunch":
                for food in foods:
                    menu_data_lunch.append(food.text)
            elif food_day == "Dinner":
                for food in foods:
                    menu_data_dinner.append(food.text)
    
    #if glasgow, get request from glasgow menu
    if 'glasgow' in request.GET:
        #get request from url
        page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=03&locationName=Glasgow&naFlag=1&_gl=1*1iyhhso*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        
        #scrape for data and put into db
        full_table = soup.find("table", attrs={"bordercolorlight":"black"})
        food_day_tables = full_table.findAll("td", attrs={"width":"30%"})
        for table in food_day_tables:
            food_day = table.find("div", attrs={"class":"shortmenumeals"}).text
            foods = table.findAll('a', attrs={"name":"Recipe_Desc"})
            if food_day == "Breakfast":
                for food in foods:
                    menu_data_breakfast.append(food.text)
            elif food_day == "Lunch":
                for food in foods:
                    menu_data_lunch.append(food.text)
            elif food_day == "Dinner":
                for food in foods:
                    menu_data_dinner.append(food.text)
                    
    #render html to django localhost
    return render(request, 'index.html', {'breakfast':menu_data_breakfast, 'lunch':menu_data_lunch, 'dinner':menu_data_dinner})