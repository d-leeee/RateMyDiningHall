import mysql.connector
from bs4 import BeautifulSoup
import requests
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="!DaNiEl1807",
    database="menu_db"
)
mycursor = mydb.cursor()

sql="INSERT IGNORE INTO food(name,category) VALUES(%s,%s)"

#get URL from UCR dining hall menu
page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University+of+California%2C+Riverside+Dining+Services&locationNum=03&locationName=Glasgow&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=10%2F20%2F2023")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

#scrape daily food menu
for food in soup.findAll("a", attrs={"name":"Recipe_Desc"}):
    val=(food.text, "")
    mycursor.execute(sql,val)

mydb.commit()
#menu = soup.findAll("a", attrs={"name":"Recipe_Desc"})
