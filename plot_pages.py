from plotter import *
from bs4 import BeautifulSoup
import numpy as np
from itertools import groupby
import pickle

input_path = "lib/edipo_re/"


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


def paragraph_length(characters=list(characters_translated.values()), verbose = True):
    def paragraph_length_func(text):

        lengths = {}

        for character in characters:
            lengths[character] = []

        for i, paragraph in enumerate(text):
            words = paragraph[1].replace('\n', ' ').replace('  ', ' ').strip().count(' ') + 1

            #Debug
            if verbose:
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


def grammar_density(text, gram = "adj", mode="possibility", characters=list(characters_translated.values())):
    def grammar_density_func(usles = None):
        paragraphs = {}
        densities = {}

        for character in characters:
            paragraphs[character] = []
            densities[character] = []

        # Could have avoided grouping... whatever it's clearer this way
        for key, group in groupby(text, lambda x: x[1]):
            group = list(group)

            paragraph_character = characters_translated[group[0][0]]

            for character in characters:
                paragraphs[character].append([])

            for word in group:
                possibilities = word[3]

                for character in characters:
                    p = len(paragraphs[character]) - 1
                    if character == paragraph_character or character == "Tutti":
                        paragraphs[character][p].append(possibilities)
                    else:
                        paragraphs[character][p].append([None])

        #print(text)
        print(paragraphs)

        for character in characters:
            for paragraph in paragraphs[character]:
                n = 0
                for word in paragraph:
                    #print(word)
                    if gram in word: n+=1

                densities[character].append(n/len(paragraph))

        return densities

    return grammar_density_func


def get_paragraphs():
    text = []

    with open(input_path + "text.txt", 'r', encoding="utf-8") as file:
        html = file.read()

        soup = BeautifulSoup(html, "html.parser")

        #print(list(soup.children))
        for paragraph in soup.children:
            if not isinstance(paragraph, str):
                text.append((paragraph['character'], paragraph.text))
            else:
                pass
                #print("paragraph: ", paragraph)

    return text


def get_grammar():
    # It's a slow function, if output has already been computed read it
    try:
        with open(input_path + "words/backup.pkl", 'rb') as file:
            grammar = pickle.load(file)
            return grammar
    except:
        pass



    grammar = []

    words = {}
    tpls = get_paragraphs()
    j = 0
    for i, tpl in enumerate(tpls):
        paragraph = tpl[1].replace('\n', ' ').replace('᾽', ' ').replace("'", ' ').replace('—', ' ').replace('-', ' ').replace('¯', ' ').replace('˘', ' ').replace(',', ' ').replace(';', ' ').replace('.', ' ').replace(':', ' ').replace('  ', ' ').strip().split()

        paragraph = [x.strip() for x in paragraph if len(x.strip())>0]

        for word in paragraph:
            words[j] = (tpl[0], i, word)
            j+=1



    types = ["noun", "adj", "verb", "article", "pron", "irreg", "partic", "conj"]

    #10216
    for n in range(0, 200):
        # Debug
        if n % 100 == 0:
            print(n, n/10216*100)
            pass

        try:
            with open(input_path + "words/" + str(n) + ".html", 'r', encoding="utf-8") as file:
                html = file.read()

                soup = BeautifulSoup(html, "html.parser")

                possibilities = []

                try:
                    classes = soup.findAll("td", {"class": "greek"})
                    word = classes[0].text.replace('᾽', '').strip()
                    if len(word) != len(words[n][2]):
                        print("Ouch", n, word, words[n][2], len(word), len(words[n][2]))
                except:
                    print("Welp", n)

                for greek in soup.findAll("td", {"class": "greek"}):
                    for td in greek.parent:
                        if not isinstance(td, str) and not td.has_attr("class"):
                            for type in types:
                                if type in td.text:
                                    possibilities.append(type)

                possibilities = list(set(possibilities))

                if len(possibilities) == 0:
                    possibilities.append("Unrecognised")

        except FileNotFoundError:
            possibilities = ["No File"]

        grammar.append((words[n][0], words[n][1], words[n][2], possibilities))

    with open(input_path + "words/backup.pkl", 'wb') as file:
        pickle.dump(grammar, file, pickle.HIGHEST_PROTOCOL)

    return grammar


#grammar_data = grammar_density(text=get_grammar(), characters=["Edipo"], gram="adj")()
#print(raw_data)
#'''
paragraph_data = paragraph_length(characters=["Edipo", "Nunzio"], verbose=False)(get_paragraphs())
#raw_data = {character: list(np.random.randint(100, size=(1, 489))[0]) for character in ["Edipo", "Tutti"]}
#print(raw_data)
#build_graph(raw_data, direct())

#build_graph(grammar_data, derivative(exponential_decay(alpha=0.5, scale_type="percentage", scale_function=maximum), 1))
build_graph(paragraph_data, derivative(exponential_decay(alpha=10, scale_type="approximate", scale_function=maximum), 1))

#build_graph(raw_data, continuous_mean(2))
#build_graph(sentence_length, continuous_median(40))

show_graph()
#'''