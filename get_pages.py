import requests
from bs4 import BeautifulSoup
import time


url = "http://www.perseus.tufts.edu/hopper/"

par = "text?doc=Perseus%3Atext%3A1999.01.0191%3Acard%3D1"


n = 0
while True:
    html = requests.get(url+par).content
    soup = BeautifulSoup(html, "html.parser")

    #uni = unicode(html)

    with open("lib/edipo_re" + str(n) + ".html", 'w', encoding="utf-8") as file:
        file.write()

    button = soup.findAll("img", {"alt": "next"})

    print(n)

    if len(button) < 1:
        break

    n += 1

    par = button[0].parent['href']





