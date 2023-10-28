from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

def home(request):
    if 'lothian' in request.GET:
        #get URL from UCR dining hall menu
        page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University+of+California%2C+Riverside+Dining+Services&locationNum=03&locationName=Glasgow&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=10%2F20%2F2023")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        #scrape daily food menu
        menu = soup.findAll("div", attrs={"class":"shortmenurecipes"})
        pass
    
    if 'glasgow' in request.GET:
        #get URL from UCR dining hall menu
        page_to_scrape = requests.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University%20of%20California%2C%20Riverside%20Dining%20Services&locationNum=02&locationName=Lothian%20Residential%20Restaurant&naFlag=1&_gl=1*152ppae*_ga*NTQ4ODY0ODA5LjE2ODQxODUxNDQ.*_ga_S8BZQKWST2*MTY5ODQ2OTg1My44MC4wLjE2OTg0Njk5MjEuMC4wLjA.*_ga_Z1RGSBHBF7*MTY5ODQ2OTg1My44MC4wLjE2OTg0Njk5MjEuMC4wLjA.")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        #scrape daily food menu
        menu = soup.findAll("div", attrs={"class":"shortmenurecipes"})
        pass
    return render(request, 'index.html')