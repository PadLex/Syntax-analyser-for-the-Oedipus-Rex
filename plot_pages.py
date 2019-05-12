
from plotter import *
from bs4 import BeautifulSoup
import numpy as np

input_path = "lib/edipo_re/text.txt"


# characters = ["Οἰδίπους", "Ἱερεύς", "Κρέων", "Χορός", "Τειρεσίας", "Ἰοκάστη", "Ἄγγελος", "Θεράπων", "Ἐξάγγελος"]
characters_translated = {"Tutti": "Tutti", "Οἰδίπους": "Edipo", "Ἱερεύς": "Sacerdote", "Κρέων": "Creonte", "Χορός": "Coro", "Τειρεσίας": "Tiresia", "Ἰοκάστη": "Giocasta", "Ἄγγελος": "Nunzio", "Θεράπων": "Servo", "Ἐξάγγελος": "Nunzio II"}
# characters_english_greek = {v: k for k, v in characters_greek_english.items()}

def sentence_length(characters=characters_translated.values()):
    def sentence_length_func(text):
        lengths = {}

        for character in characters:
            lengths[character] = []

        for paragraph in text:
            lines = paragraph[1].replace('\n', ' ').replace('  ', ' ').replace(';', '.').replace(':', '.').strip().split('.')

            for i, line in enumerate(lines):
                if len(line) > 0:
                    words = line.strip().count(' ') + 1

                    if words < 1:
                        #lengths.append(lengths[i - 1])
                        print("Is this right?", line)
                    else:
                        for character in characters:
                            #print(character[0])
                            if character == characters_translated[paragraph[0]] or character == "Tutti":
                                lengths[character].append(words)
                            else:
                                lengths[character].append(None)

                #print(i, line)

        return lengths

    return sentence_length_func


def paragraph_length(characters=list(characters_translated.values())):
    def paragraph_length_func(text):

        lengths = {}

        for character in characters:
            lengths[character] = []

        for i, paragraph in enumerate(text):
            words = paragraph[1].replace('\n', ' ').replace('  ', ' ').strip().count(' ') + 1

            #Debug
            start = 49
            end = 141
            total = end-start
            percentage = i/len(text)
            page = start + percentage*total
            print(i, int(page), characters_translated[paragraph[0]], paragraph[1])

            if words < 1:
                #lengths.append(lengths[i - 1])
                print("Is this right?", paragraph[1])
            else:
                for character in characters:
                    if character == characters_translated[paragraph[0]] or character == "Tutti":
                        lengths[character].append(words)
                    else:
                        lengths[character].append(None)

                #print(i, line)

        return lengths

    return paragraph_length_func


text = []
with open(input_path, 'r', encoding="utf-8") as file:
    html = file.read()

    soup = BeautifulSoup(html, "html.parser")

    #print(list(soup.children))
    for paragraph in soup.children:
        if not isinstance(paragraph, str):
            text.append((paragraph['character'], paragraph.text))
        else:
            pass
            #print("paragraph: ", paragraph)


raw_data = paragraph_length(["Tutti", "Coro"])(text)
#raw_data = {character: list(np.random.randint(100, size=(1, 489))[0]) for character in ["Edipo", "Tutti"]}
#print(raw_data)
#build_graph(raw_data, exponential_decay(1))

build_graph(raw_data, derivative(exponential_decay(alpha=10, scale_type="percentage"), 0))

#build_graph(raw_data, continuous_mean(90))
#build_graph(sentence_length, continuous_median(40))

show_graph()