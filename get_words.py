import grequests
from bs4 import BeautifulSoup
import time
import os

path = os.getcwd() + "\\lib\\edipo_re\\"

base_url = "http://www.perseus.tufts.edu/hopper/"

urls = []

n = 0

while True:

    file_name = str(n) + ".html"

    try:

        with open(path + "pages\\" + file_name, 'r', encoding="utf-8") as file:

            html = file.read()
            soup = BeautifulSoup(html, "html.parser")

            div = soup.find("div", {"class": "text"})

            for element in div.findAll("a", recursive=False):
                urls.append(base_url + element['href'])

        #if n > 1:
            #break


    except FileNotFoundError:
        break

    n += 1


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


print("Fetching ", len(urls), "urls")

start = 0

concurrent = 30

n = start
for targets in chunks(urls[start:], concurrent):

        rs = (grequests.get(u) for u in targets)
        responses = grequests.map(rs)

        print(str(n/len(urls)*100) + '%', n)

        for response in responses:
            try:
                file_name = str(n) + ".html"
                with open(path + "words\\" + file_name, 'w', encoding="utf-8") as file:
                    file.write(str(response.content, "utf-8"))
            except:
                print("Something went wrong", n)

            n += 1

