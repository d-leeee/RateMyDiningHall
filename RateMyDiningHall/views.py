from django.shortcuts import render

def get_html():
    import requests
    html_content=session.get("https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University+of+California%2C+Riverside+Dining+Services&locationNum=03&locationName=Glasgow&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=10%2F20%2F2023")
def home(request):
    if 'lothian' in request.GET:
        pass
    if 'glasgow' in request.GET:
        pass
    return render(request, 'index.html')