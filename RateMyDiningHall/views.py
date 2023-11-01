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

# connect to mysql db
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="!DaNiEl1807",
    database="menu_db"
)

mycursor = mydb.cursor()
sql = "INSERT IGNORE INTO food(name,category) VALUES(%s,%s)"


# get URL from UCR dining hall menu
page_to_scrape = [requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=02&locationName=Lothian%20Residential%20Restaurant&naFlag=1&_gl=1*157j69u*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgzMTcuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgzMTcuMC4wLjA."),
                  requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=03&locationName=Glasgow&naFlag=1&_gl=1*1iyhhso*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.")]
i = 0
for times in page_to_scrape:
    soup = BeautifulSoup(page_to_scrape[i].text, "html.parser")
    i += 1

    # since lothian doesn't serve on weekends, there must be a try and except to eleminate errors when no tables appear
    try:
        # find all div elements inside the table
        food_table = soup.find('table', attrs={"bordercolorlight": "black"})
        food_rows = food_table.findAll('div')

        # iterate through every single div element to check for category/food
        for category in food_rows:
            # if the div class is a category set it equal to cats
            if category['class'][0] == 'shortmenucats':
                cats = category.find('span', attrs={"style": "color: "})
            # if the div class is a food set it equal to food and add it to database
            elif category['class'][0] == 'shortmenurecipes':
                food = category.find('a', attrs={"name": "Recipe_Desc"})
                val = (food.text, cats.text)
                mycursor.execute(sql, val)
    except:
        continue

# commit changes
mydb.commit()

#
#
#
# RENDER HTML AND DINING MENU
#
#
#

from django.shortcuts import render
import numpy as np
import functools

def home(request):

    
    page_to_scrape = None

    # if lothian, get request from lothian menu
    if 'lothian' in request.GET:
        menu_data_breakfast = []
        menu_data_lunch = []
        menu_data_dinner = []
        # get request from url
        page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=02&locationName=Lothian%20Residential%20Restaurant&naFlag=1&_gl=1*157j69u*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgzMTcuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgzMTcuMC4wLjA.")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        # scrape for data and put into db for breakfast, lunch, and dinner
        full_table = soup.find("table", attrs={"bordercolorlight": "black"})
        food_day_tables = full_table.findAll("td", attrs={"width": "30%"})
        for table in food_day_tables:
            food_day = table.find(
                "div", attrs={"class": "shortmenumeals"}).text
            foods = table.findAll('a', attrs={"name": "Recipe_Desc"})
            if food_day == "Breakfast":
                for food in foods:
                    menu_data_breakfast.append(food.text)
            elif food_day == "Lunch":
                for food in foods:
                    menu_data_lunch.append(food.text)
            elif food_day == "Dinner":
                for food in foods:
                    menu_data_dinner.append(food.text)

    # if glasgow, get request from glasgow menu
    if 'glasgow' in request.GET:
        
        # keep these variables at none so that we dont get unassigned errors
        menu_salad_deli_and_more_lunch = np.array([])
        menu_wok_kitchen_lunch = np.array([])
        menu_hot_plate_lunch = np.array([])
        menu_three_sixty_grill_lunch = np.array([])
        menu_the_carvery_lunch = np.array([])
        menu_sweets_and_treats_lunch = np.array([])
        menu_build_your_own_vegan_bowl_lunch = np.array([])
        
        menu_salad_deli_and_more_dinner = np.array([])
        menu_wok_kitchen_dinner = np.array([])
        menu_hot_plate_dinner = np.array([])
        menu_three_sixty_grill_dinner = np.array([])
        menu_the_carvery_dinner = np.array([])
        menu_sweets_and_treats_dinner = np.array([])
        menu_build_your_own_vegan_bowl_dinner = np.array([])
        
        menu_fresh_baked_pastries = np.array([])
        menu_cereal_station = np.array([])
        menu_breakfast_offerings = np.array([])
        
        menu_data_breakfast_temp = []
        menu_data_lunch_temp = []
        menu_data_dinner_temp = []
        
        # get request from url
        page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=03&locationName=Glasgow&naFlag=1&_gl=1*1iyhhso*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        # scrape for data and put into db
        full_table = soup.find("table", attrs={"bordercolorlight": "black"})
        food_day_tables = full_table.findAll("td", attrs={"width": "30%"})
        
        for table in food_day_tables:
            food_day = table.find("div", attrs={"class": "shortmenumeals"}).text #time of day
            foods = table.findAll('a', attrs={"name": "Recipe_Desc"}) #each food
            food_rows = table.findAll('div')
            for category in food_rows:
                if food_day == "Breakfast":
                    if category['class'][0] == 'shortmenucats' or category['class'][0] == 'shortmenurecipes':
                        menu_data_breakfast_temp.append(category.text)
                elif food_day == "Lunch":
                    if category['class'][0] == 'shortmenucats' or category['class'][0] == 'shortmenurecipes':
                        menu_data_lunch_temp.append(category.text)
                elif food_day == "Dinner":
                    if category['class'][0] == 'shortmenucats' or category['class'][0] == 'shortmenurecipes':
                        menu_data_dinner_temp.append(category.text)
                        
        #breakfast category append
        menu_fresh_baked_pastries = np.append(menu_data_breakfast_temp[menu_data_breakfast_temp.index('-- Fresh Baked Pastries --')+1:menu_data_breakfast_temp.index('-- Cereal Station --')], menu_fresh_baked_pastries)
        menu_cereal_station = np.append(menu_data_breakfast_temp[menu_data_breakfast_temp.index('-- Cereal Station --')+1:menu_data_breakfast_temp.index('-- Breakfast Offerings --')], menu_cereal_station)
        menu_breakfast_offerings = np.append(menu_data_breakfast_temp[menu_data_breakfast_temp.index('-- Breakfast Offerings --')+1:len(menu_data_breakfast_temp)], menu_breakfast_offerings)
        
        #lunch category append
        menu_salad_deli_and_more_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Salad, Deli and More --')+1:menu_data_lunch_temp.index('-- Wok Kitchen --')], menu_salad_deli_and_more_lunch)
        menu_wok_kitchen_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Wok Kitchen --')+1:menu_data_lunch_temp.index('-- Hot Plate --')], menu_wok_kitchen_lunch)
        menu_hot_plate_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Hot Plate --')+1:menu_data_lunch_temp.index('-- Three-Sixty Grill --')], menu_hot_plate_lunch)
        menu_three_sixty_grill_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Three-Sixty Grill --')+1:menu_data_lunch_temp.index('-- The Carvery --')], menu_three_sixty_grill_lunch)
        menu_the_carvery_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- The Carvery --')+1:menu_data_lunch_temp.index('-- Sweets & Treats --')], menu_the_carvery_lunch)
        menu_sweets_and_treats_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Sweets & Treats --')+1:menu_data_lunch_temp.index('-- Build Your Own Vegan Bowl --')],menu_sweets_and_treats_lunch)
        menu_build_your_own_vegan_bowl_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Build Your Own Vegan Bowl --')+1:len(menu_data_lunch_temp)], menu_build_your_own_vegan_bowl_lunch)
        
        #dinner category append
        menu_salad_deli_and_more_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Salad, Deli and More --')+1:menu_data_dinner_temp.index('-- Wok Kitchen --')], menu_salad_deli_and_more_dinner)
        menu_wok_kitchen_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Wok Kitchen --')+1:menu_data_dinner_temp.index('-- Hot Plate --')], menu_wok_kitchen_dinner)
        menu_hot_plate_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Hot Plate --')+1:menu_data_dinner_temp.index('-- Three-Sixty Grill --')], menu_hot_plate_dinner)
        menu_three_sixty_grill_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Three-Sixty Grill --')+1:menu_data_dinner_temp.index('-- The Carvery --')], menu_three_sixty_grill_dinner)
        menu_the_carvery_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- The Carvery --')+1:menu_data_dinner_temp.index('-- Sweets & Treats --')], menu_the_carvery_dinner)
        menu_sweets_and_treats_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Sweets & Treats --')+1:menu_data_dinner_temp.index('-- Build Your Own Vegan Bowl --')],menu_sweets_and_treats_dinner)
        menu_build_your_own_vegan_bowl_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Build Your Own Vegan Bowl --')+1:len(menu_data_dinner_temp)], menu_build_your_own_vegan_bowl_dinner)
        
    # render html to django localhost
    return render(request, 'index.html', {'FreshBakedPastries': menu_fresh_baked_pastries,
                                          'CerealStation': menu_cereal_station,
                                          'BreakfastOfferings': menu_breakfast_offerings,
                                          
                                          'SaladDeliAndMoreLunch': menu_salad_deli_and_more_lunch,
                                          'WokKitchenLunch': menu_wok_kitchen_lunch,
                                          'HotPlateLunch': menu_hot_plate_lunch,
                                          'ThreeSixtyGrillLunch': menu_three_sixty_grill_lunch,
                                          'TheCarveryLunch': menu_the_carvery_lunch,
                                          'SweetsAndTreatsLunch': menu_sweets_and_treats_lunch,
                                          'BuildYourOwnVeganGrillLunch': menu_build_your_own_vegan_bowl_lunch,
                                          
                                          'SaladDeliAndMoreDinner': menu_salad_deli_and_more_dinner,
                                          'WokKitchenDinner': menu_wok_kitchen_dinner,
                                          'HotPlatDinner': menu_hot_plate_dinner,
                                          'ThreeSixtyGrillDinner': menu_three_sixty_grill_dinner,
                                          'TheCarveryDinner': menu_the_carvery_dinner,
                                          'SweetsAndTreatsDinner': menu_sweets_and_treats_dinner,
                                          'BuildYourOwnVeganGrillDinner': menu_build_your_own_vegan_bowl_dinner,})
