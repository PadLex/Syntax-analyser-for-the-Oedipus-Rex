from bs4 import BeautifulSoup

import os


path = os.getcwd() + "\\lib\\edipo_re\\words\\"

content = ""

n = 0
while True:

    file_name = str(n) + ".html"

    try:

        with open(path + file_name, 'r', encoding="utf-8") as file:
            try:
                html = file.read()

                soup = BeautifulSoup(html, "html.parser")

                div = soup.find("div", {"class": "text"})

                for element in div.findChildren():
                     #print(element.text)

                    if element.name == 'a':
                        content += element.text + ' '
                    elif element.name == 'br':
                        content += '\n'

                content += '-' + str(n) + '-'

            except:
                print("ERROR" + file_name)

            n += 1

    except FileNotFoundError:
        break


with open(os.getcwd() + "\\lib\\edipo_re\\word_referencer", 'w', encoding="utf-8") as file:
    file.write(content)

print(content)
