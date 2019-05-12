from bs4 import BeautifulSoup

import os
import re

path = os.getcwd() + "\\lib\\edipo_re\\pages\\"

content = ""

n = 0
while True:

    file_name = str(n) + ".html"

    try:

        with open(path + file_name, 'r', encoding="utf-8") as file:
            #try:
            html = file.read()

            soup = BeautifulSoup(html, "html.parser")

            div = soup.find("div", {"class": "text"})

            for element in div:
                #print(element)
                if isinstance(element, str):
                    content += element
                elif element.name == 'b':
                    content += '</p>\n\n<p character=\"' + list(element.children)[0].text + '\">'
                elif element.name == 'a':
                    content += element.text
                elif element.name == 'br':
                    content += ''
                elif element.name != 'span' and element.name != 'hr' and element.name != 'p':
                    print("What:", element)

            #content += '-' + str(n) + '-'

            #except:
                #print("ERROR" + file_name)

            n += 1

    except FileNotFoundError:
        break

content += "</p>"
content = re.sub('\">[\n\s]*', '\">\n', content)
content = re.sub('[\n\s]*<\/p>', '\n</p>', content)

with open(os.getcwd() + "\\lib\\edipo_re\\text.txt", 'w', encoding="utf-8") as file:
    file.write(content)
    pass

#print(content)


'''
            for paragraph in div:
                for element in paragraph:
                    if not isinstance(element, str):
                        print("paragraph:", paragraph, "element:", element)

                        if element.name == 'b':
                            content += '</p>\n\n<p title=\"' + element[0].text + '\">'
                        elif element.name == 'a':
                            content += element.text + ' '
                        elif element.name == 'br' or element.name == 'p':
                            content += '\n'
                        elif element.name != 'span':
                            print("What is this: " + element)'''