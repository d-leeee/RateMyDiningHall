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
from .models import Database 
from django.shortcuts import render
import numpy as np
import functools

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



def home(request):

    page_to_scrape = None
    # if glasgow, get request from glasgow menu

    # keep these variables at none so that we dont get unassigned errors
    menu_build_your_own_bowl_lunch = np.array([])
    menu_soup_and_deli_bar_lunch = np.array([])
    menu_global_sizzle_lunch = np.array([])
    menu_urban_kitchen_lunch = np.array([])
    menu_the_grill_lunch = np.array([])
    menu_comfort_table_lunch = np.array([])
    menu_desserts_lunch = np.array([])
    menu_village_garden_lunch = np.array([])
    
    menu_build_your_own_bowl_dinner = np.array([])
    menu_soup_and_deli_bar_dinner = np.array([])
    menu_global_sizzle_dinner = np.array([])
    menu_urban_kitchen_dinner = np.array([])
    menu_the_grill_dinner = np.array([])
    menu_comfort_table_dinner = np.array([])
    menu_desserts_dinner = np.array([])
    menu_village_garden_dinner = np.array([])
    
    menu_data_lunch_temp = []
    menu_data_dinner_temp = []
    
    # get request from url
    page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=02&locationName=Lothian%20Residential%20Restaurant&naFlag=1&_gl=1*1hlufbx*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5OTk1Nzc3Mi4xMDYuMS4xNjk5OTU5NTUxLjAuMC4w*_ga_Z1RGSBHBF7*MTY5OTk1Nzc3Mi4xMDYuMS4xNjk5OTU5NTUxLjAuMC4w")
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")

    # scrape for data and put into db
    full_table = soup.find("table", attrs={"bordercolorlight": "black"})
    if full_table:
        food_day_tables = full_table.findAll("td", attrs={"width": "30%"})
    
        for table in food_day_tables:
            food_day = table.find("div", attrs={"class": "shortmenumeals"}).text #time of day
            foods = table.findAll('a', attrs={"name": "Recipe_Desc"}) #each food
            food_rows = table.findAll('div')
            for category in food_rows:
                if food_day == "Lunch":
                    if category['class'][0] == 'shortmenucats' or category['class'][0] == 'shortmenurecipes':
                        menu_data_lunch_temp.append(category.text)
                elif food_day == "Dinner":
                    if category['class'][0] == 'shortmenucats' or category['class'][0] == 'shortmenurecipes':
                        menu_data_dinner_temp.append(category.text)
        
        if '-- BYOB (Build Your Own Bowl) --' in menu_build_your_own_bowl_lunch:
            #lunch category append
            menu_build_your_own_bowl_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- BYOB (Build Your Own Bowl) --')+1:menu_data_lunch_temp.index('-- Soup & Deli Bar --')], menu_build_your_own_bowl_lunch)
            menu_soup_and_deli_bar_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Soup & Deli Bar --')+1:menu_data_lunch_temp.index('-- Global Sizzle --')], menu_soup_and_deli_bar_lunch)
            menu_global_sizzle_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Global Sizzle --')+1:menu_data_lunch_temp.index('-- Urban Kitchen --')], menu_global_sizzle_lunch)
            menu_urban_kitchen_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Urban Kitchen --')+1:menu_data_lunch_temp.index('-- The Grill --')], menu_urban_kitchen_lunch)
            menu_the_grill_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- The Grill --')+1:menu_data_lunch_temp.index('-- Comfort Table --')], menu_the_grill_lunch)
            menu_comfort_table_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Comfort Table --')+1:menu_data_lunch_temp.index('-- Desserts --')],menu_comfort_table_lunch)
            menu_desserts_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Desserts --')+1:menu_data_lunch_temp.index('-- Village Garden --')],menu_desserts_lunch)
            menu_village_garden_lunch = np.append(menu_data_lunch_temp[menu_data_lunch_temp.index('-- Village Garden --')+1:len(menu_data_lunch_temp)], menu_village_garden_lunch)

            #dinner category append
            menu_build_your_own_bowl_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- BYOB (Build Your Own Bowl) --')+1:menu_data_dinner_temp.index('-- Soup & Deli Bar --')], menu_build_your_own_bowl_dinner)
            menu_soup_and_deli_bar_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Soup & Deli Bar --')+1:menu_data_dinner_temp.index('-- Global Sizzle --')], menu_soup_and_deli_bar_dinner)
            menu_global_sizzle_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Global Sizzle --')+1:menu_data_dinner_temp.index('-- Urban Kitchen --')], menu_global_sizzle_dinner)
            menu_urban_kitchen_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Urban Kitchen --')+1:menu_data_dinner_temp.index('-- The Grill --')], menu_urban_kitchen_dinner)
            menu_the_grill_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- The Grill --')+1:menu_data_dinner_temp.index('-- Comfort Table --')], menu_the_grill_dinner)
            menu_comfort_table_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Comfort Table --')+1:menu_data_dinner_temp.index('-- Desserts --')],menu_comfort_table_dinner)
            menu_desserts_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Desserts --')+1:menu_data_dinner_temp.index('-- Village Garden --')],menu_desserts_dinner)
            menu_village_garden_dinner = np.append(menu_data_dinner_temp[menu_data_dinner_temp.index('-- Village Garden --')+1:len(menu_data_dinner_temp)], menu_village_garden_dinner)
            
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
    page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=03&locationName=Glasgow&naFlag=1&_gl=1*11j1pjy*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5OTk1Nzc3Mi4xMDYuMS4xNjk5OTU5NjA2LjAuMC4w*_ga_Z1RGSBHBF7*MTY5OTk1Nzc3Mi4xMDYuMS4xNjk5OTU5NjA2LjAuMC4w")
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
    try:
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
    except:
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
                                          'BuildYourOwnVeganBowlLunch': menu_build_your_own_vegan_bowl_lunch,
                                          
                                          'SaladDeliAndMoreDinner': menu_salad_deli_and_more_dinner,
                                          'WokKitchenDinner': menu_wok_kitchen_dinner,
                                          'HotPlatDinner': menu_hot_plate_dinner,
                                          'ThreeSixtyGrillDinner': menu_three_sixty_grill_dinner,
                                          'TheCarveryDinner': menu_the_carvery_dinner,
                                          'SweetsAndTreatsDinner': menu_sweets_and_treats_dinner,
                                          'BuildYourOwnVeganBowlDinner': menu_build_your_own_vegan_bowl_dinner,
                                          
                                          'BuildYourOwnBowlLunch': menu_build_your_own_bowl_lunch,
                                          'SoupAndDeliBarLunch': menu_soup_and_deli_bar_lunch,
                                          'GlobalSizzleLunch': menu_global_sizzle_lunch,
                                          'UrbanKitchenLunch': menu_urban_kitchen_lunch,
                                          'TheGrillLunch' : menu_the_grill_lunch,
                                          'ComfortTableLunch' : menu_comfort_table_lunch,
                                          'DessertsLunch' : menu_desserts_lunch,
                                          'VillageGardenLunch' : menu_village_garden_lunch,
                                          
                                          'BuildYourOwnBowlDinner': menu_build_your_own_bowl_dinner,
                                          'SoupAndDeliBarDinner': menu_soup_and_deli_bar_dinner,
                                          'GlobalSizzleDinner': menu_global_sizzle_dinner,
                                          'UrbanKitchenDinner': menu_urban_kitchen_dinner,
                                          'TheGrillDinner' : menu_the_grill_dinner,
                                          'ComfortTableDinner' : menu_comfort_table_dinner,
                                          'DessertsDinner' : menu_desserts_dinner,
                                          'VillageGardenDinner' : menu_village_garden_dinner })
                                 
def reviews(request):
    #after clicking hyperlink, recieve the food text
    request.session['getFoodText'] = request.GET.get("name")
    foods = Database.objects.all().values()
    return render(request,'reviews.html', {'foodItem' : request.session['getFoodText'], 'foodDatabase': foods})

def submitReview(request):
    if request.method=='POST':
        if request.POST.get('name') and request.POST.get('stars') and request.POST.get('review'):
            save = Database()
            save.name = request.POST.get('name')
            save.stars = request.POST.get('stars')
            save.review = request.POST.get('review')
            save.food_name = request.session['getFoodText']
            save.save()
            
    foods = Database.objects.all().values()
    
    return render(request,'reviews.html', {'foodItem' : request.session['getFoodText'],'foodDatabase': foods})