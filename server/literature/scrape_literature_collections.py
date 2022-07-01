import json
import pathlib
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
import re

ROOT_PATH = pathlib.Path(__file__)
BASE_PATH = ROOT_PATH.parent

OUTPUT_JSON_PATH = (BASE_PATH / "important_literature_words.json").absolute().as_posix()
LITERATURE_VOCABULARY = (
    (BASE_PATH / "Vocabulary_Lists_Literature_Vocabulary.com.html")
    .absolute()
    .as_posix()
)


def scrape_and_generate_important_literature_words():
    try:
        with open(LITERATURE_VOCABULARY, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, features="lxml")
        button_learn_div_list = soup.findAll("a", {"class": "button learn"})
        book_words_list = []
        link_words = defaultdict(list)
        all_words = []
        for enum, link_div in enumerate(button_learn_div_list):
            book_words = defaultdict(list)
            link = link_div.attrs["href"]
            page = requests.get(link)
            page_text = page.text
            page_soup = BeautifulSoup(page_text, features="lxml")
            blockquote_list = page_soup.findAll("blockquote")
            blockquote = blockquote_list and blockquote_list[0]
            blockquote = (
                blockquote
                and blockquote.text.split("\n")
                and blockquote.text.split("\n")[0]
            )
            img_cover_div_list = page_soup.findAll("img", {"class": "cover"})
            if img_cover_div_list:
                img_cover_div_list = img_cover_div_list[0]
            if img_cover_div_list:
                book_words["cover_image_link"] = img_cover_div_list.attrs["src"]
            else:
                book_name = link

            collection_class_div_list = page_soup.findAll("span", {"class": "title"})
            if collection_class_div_list:
                collection_class_div_list = collection_class_div_list[0]
            words = []
            words_list = []
            list_section = page_soup.findAll("section", {"class": "wordlists"})
            for section in list_section:
                wordlists = section.findAll("li", {"class": "wordlist"})
                level_2_list = []
                for wordlist in wordlists:
                    wordlist = wordlist.findAll("li")
                    level_3_list = []
                    for word_div in wordlist:
                        level_3_list.append(word_div.text)
                    level_2_list.append(level_3_list)
                    words_list.extend(level_3_list)
                all_words.append(level_2_list)
                words.extend(level_2_list)
            book_words["blockquote"] = blockquote
            book_name = collection_class_div_list.text
            match = re.search("[A-Za-z0-9 \\//'\"]+", book_name)
            match_span = match and match.span()
            if match:
                start = match_span[0]
                end = match_span[-1]
                book_name = match.string[start:end]
            book_words["book_name"] = book_name
            book_words["book_words"] = words_list
            if book_words and book_words not in book_words_list:
                book_words_list.append(dict(book_words))
            link_words[book_name] = words
            print(len(button_learn_div_list) - enum)
        final_dictionary = dict()
        final_dictionary["book_words_list"] = book_words_list
        final_dictionary["link_words"] = dict(link_words)
        final_dictionary["all_words"] = all_words
        with open(OUTPUT_JSON_PATH, "w") as f:
            f.write(json.dumps(final_dictionary, indent=4))
    except:
        final_dictionary = dict()
        final_dictionary["book_words_list"] = book_words_list
        final_dictionary["link_words"] = link_words
        final_dictionary["all_words"] = all_words
        with open(OUTPUT_JSON_PATH, "w") as f:
            f.write(json.dumps(final_dictionary, indent=4))


if __name__ == "__main__":
    scrape_and_generate_important_literature_words()
    OUTPUT_JSON_PATH = (
        (BASE_PATH / "important_literature_words.json").absolute().as_posix()
    )
    with open(OUTPUT_JSON_PATH, "r") as f:
        final_dictionary = eval(f.read())

    OUTPUT_JSON_PATH2 = (BASE_PATH / "important_words.json").absolute().as_posix()
    with open(OUTPUT_JSON_PATH2, "r") as f:
        final_dictionary2 = eval(f.read())
