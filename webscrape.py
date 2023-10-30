#
# this is a test file for webscraping to mySQL database
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
page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=03&locationName=Glasgow&naFlag=1&_gl=1*1iyhhso*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODU1ODE0Mi44NC4xLjE2OTg1NTgxNDUuMC4wLjA.")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

#find all div elements inside the table
food_table = soup.find('table', attrs={"bordercolorlight":"black"})
food_rows = food_table.findAll('div')

#iterate through every single div element to check for category/food
for category in food_rows:
    i=0
    #if the div class is a category set it equal to cats
    if category['class'][i] == 'shortmenucats':
        cats = category.find('span', attrs={"style":"color: "})
    #if the div class is a food set it equal to food and add it to database
    elif category['class'][i] == 'shortmenurecipes':
        food = category.find('a', attrs={"name":"Recipe_Desc"})
        val = (food.text, cats.text)
        mycursor.execute(sql,val)
    i+=1
    
#commit changes
mydb.commit()