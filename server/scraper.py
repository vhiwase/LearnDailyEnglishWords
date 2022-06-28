import json
import pathlib
import re
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

ROOT_PATH = pathlib.Path(__file__)
BASE_PATH = ROOT_PATH.parent

JSON_PATH = (BASE_PATH / "vocabulary_list.json").absolute().as_posix()
OUTPUT_JSON_PATH = (BASE_PATH / "important_words.json").absolute().as_posix()

with open(JSON_PATH, "r") as f:
    vocabulary_dict = json.load(f)
    vocabulary_list = vocabulary_dict["links_list"]

vocabulary_list = vocabulary_list[:5]

book_words_list = []
link_words = defaultdict(list)
all_words = []
c = len(vocabulary_list)
for link in vocabulary_list:
    c -= 1
    print(c)
    page = requests.get(link)
    page_text = page.text
    dictionary_words = re.findall(r"/dictionary/[a-zA-Z0-9]+", page_text)
    soup = BeautifulSoup(page_text, features="lxml")
    collection_class_div_list = soup.findAll("span", {"class": "collection"})
    img_cover_div_list = soup.findAll("img", {"class": "cover"})
    if img_cover_div_list:
        img_cover_div_list = img_cover_div_list[0]
    if collection_class_div_list:
        collection_class_div_list = collection_class_div_list[0]
    word_class_div_list = soup.findAll("a", {"class": "word"})
    words = []
    book_words = defaultdict(list)
    for word_class_div in word_class_div_list:
        if collection_class_div_list:
            book_name = collection_class_div_list.text
            book_words["book_name"] = book_name
            book_words["book_words"].append(word_class_div.text)
            if img_cover_div_list:
                book_words["cover_image_link"] = img_cover_div_list.attrs["src"]
        else:
            book_name = link
        if book_words:
            book_words_list.append(book_words)
        link_words[book_name].append(word_class_div.text)
        words.append(word_class_div.text)
    all_words.append(words)

final_dictionary = dict()
final_dictionary["book_words_list"] = book_words_list
final_dictionary["link_words"] = link_words
final_dictionary["all_words"] = all_words

with open(OUTPUT_JSON_PATH, "w") as f:
    f.write(json.dumps(final_dictionary, indent=4))