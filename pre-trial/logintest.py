from bs4 import BeautifulSoup

with open('loginPage.html', 'r') as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'lxml')
form = soup.find('form')
token = soup.find('input', attrs={"name": "logintoken"})

print(token["value"])
