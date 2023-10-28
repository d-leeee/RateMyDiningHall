from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app=Flask(__name__)

#get URL from UCR dining hall menu
page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University+of+California%2C+Riverside+Dining+Services&locationNum=03&locationName=Glasgow&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=10%2F20%2F2023")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

#scrape daily food menu
menu = soup.findAll("div", attrs={"class":"shortmenurecipes"})

@app.route('/')
def home():
    return render_template('index.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)