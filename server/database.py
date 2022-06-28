import json
import pathlib

ROOT_PATH = pathlib.Path(__file__)
BASE_PATH = ROOT_PATH.parent
pathlib.sys.path.insert(0, BASE_PATH)

# import os
import pathlib
import ssl
import time
from collections import defaultdict

# from io import BytesIO
# from shutil import rmtree
# import filetype
import requests
from bs4 import BeautifulSoup

# from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import (
    ChromeDriverManager,
)  # use to initialize driver in a better way without having chromedriver path mentioned.

JSON_PATH = (BASE_PATH / "important_words.json").absolute().as_posix()
DATABASE_PATH = (BASE_PATH / "database.json").absolute().as_posix()

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
try:
    driver = webdriver.Chrome(options=chrome_options)
except Exception as e:
    print(e)
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options
    )  # chrome_options is deprecated
    driver.maximize_window()

ROOT_PATH = pathlib.Path(__file__)
BASE_PATH = ROOT_PATH.parent

"""
pip install beautifulsoup4
pip install selenium
pip install lxml
pip install webdriver-manager
"""

ssl._create_default_https_context = ssl._create_unverified_context


def get_link(word):
    link = "https://www.vocabulary.com/dictionary/" + word
    return link


def get_page(word):
    link = get_link(word)
    page = requests.get(link)
    return page.text


def get_page_for_sentence(word):
    url = get_link(word)
    driver.get(url)
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight)"
    )  # Scroll to the bottom of the page
    time.sleep(1)  # Wait 4 seconds for all the images to load
    data = driver.execute_script("return document.documentElement.outerHTML")
    scraper = BeautifulSoup(data, features="lxml")
    return str(scraper)


def get_description(content):
    soup = BeautifulSoup(content, features="lxml")
    meta_content_list = soup.findAll("meta", {"name": "description"})
    meta_content = meta_content_list and meta_content_list[0]
    return meta_content.attrs


def get_definition(content, get_type):
    soup = BeautifulSoup(content, features="lxml")
    def_div = soup.findAll("p", {"class": get_type})
    if len(def_div) == 0:
        return ""
    assert len(def_div) == 1
    def_div = def_div[0]
    return def_div.get_text()


def get_part_of_speech_and_short_definition(content):
    soup = BeautifulSoup(content, features="lxml")
    div_definitions = soup.findAll("div", {"class": "definition"})
    if not div_definitions:
        div_definitions = soup.findAll("span", {"class": "definition"})
    if len(div_definitions) == 0:
        return dict()
    pos_sentence_dict = defaultdict(list)
    for div_definition in div_definitions:
        text = div_definition.text
        split_list = "".join("".join(text.split("\n")).split("\r")).split("\t")
        split_list = [i.strip() for i in split_list]
        split_list = list(filter(None, split_list))
        if len(split_list) == 2:
            pos_sentence_dict[split_list[0]].append(split_list[1])
        elif len(split_list) == 1:
            split_list = [""] + split_list
            pos_sentence_dict[split_list[0]].append(split_list[1])
    return dict(pos_sentence_dict)


def get_long_definition(content):
    return get_definition(content, "long")


def get_instance(content, ins_type):
    soup = BeautifulSoup(content, features="lxml")
    instance_div = soup.findAll("dl", {"class": "instances"})
    if ins_type == "synonym":
        ch_type = "Synonyms:"
    if ins_type == "antonym":
        ch_type = "Antonyms:"
    if ins_type == "type_of":
        ch_type = "Type of:"
    # res = {}
    for instance in instance_div:
        if ch_type in instance.get_text().split():
            a_div = instance.findAll("a", {"class": "word"})
            word_divs = []
            for word_div in a_div:
                word_div_text = word_div.get_text()
                word_divs.append(word_div_text)
            return word_divs
    else:
        return []
        # dd_div = instance.findAll("dd")
        # for each_dd_div in dd_div:
        #     if not dd_div:
        #         break
        #         # return []
        # if each_dd_div.get_text() != "":
        #     current_type = each_dd_div.get_text()
        #     a_div = instance.findAll("a", {"class": "word"})
        #     for word_div in a_div:
        #         word = word_div.get_text()
        #         res[word] = ""
    # ret = []
    # for key in res:
    #     ret.append(key)
    # return ret


def get_synonym(content):
    return get_instance(content, "synonym")


def get_type_of(content):
    return get_instance(content, "type_of")


def get_antonym(content):
    return get_instance(content, "antonym")


def get_sentence(word):
    page = get_page_for_sentence(word)
    soup = BeautifulSoup(page, features="lxml")
    sentence_example_div = soup.findAll("div", {"class": "sentence"})
    examples = []
    for sentence_div in sentence_example_div:
        examples.append(str(sentence_div.text))
    examples = sorted(examples, key=lambda x: len(x))
    return examples


def get_json(word):
    word = word and word.strip()
    json_dict = {}
    if not word:
        json_dict["description"] = ""
        json_dict["shorts"] = []
        json_dict["long"] = ""
        json_dict["synonym"] = []
        json_dict["antonym"] = []
        json_dict["type_of"] = []
        json_dict["examples"] = []
        json_dict["part_of_speech"] = []
        return json_dict
    page = get_page(word)
    description = get_description(page)
    pos_sentence_dict = get_part_of_speech_and_short_definition(page)
    pos = []
    if pos_sentence_dict:
        pos = list(filter(None, pos_sentence_dict.keys()))
    shorts = []
    for k, v in pos_sentence_dict.items():
        if k and v:
            short_def_text = "({}) {}".format(k, v[0])
            shorts.append(short_def_text)
    if not shorts:
        for values in pos_sentence_dict.values():
            shorts = values
            if shorts:
                break
    long_def = get_long_definition(page)
    synonym = get_synonym(page)
    type_of = get_type_of(page)
    antonym = get_antonym(page)
    examples = get_sentence(word)
    json_dict["description"] = description["content"]
    json_dict["shorts"] = shorts
    json_dict["long"] = long_def
    json_dict["synonym"] = synonym
    json_dict["antonym"] = antonym
    json_dict["type_of"] = type_of
    json_dict["examples"] = examples
    json_dict["part_of_speech"] = pos
    # json.dumps(json_dict, indent = 4)
    return json_dict


def imagescrape(search_term):
    try:
        url = "https://www.shutterstock.com/search/{}".format(search_term)
        driver.get(url)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight)"
        )  # Scroll to the bottom of the page
        # time.sleep(4)  # Wait 4 seconds for all the images to load
        data = driver.execute_script("return document.documentElement.outerHTML")
        scraper = BeautifulSoup(data, "lxml")
        img_container = scraper.find_all("img")
        image_links = []
        for j in range(20):
            if img_container[j].has_attr("src"):
                img_src = img_container[j].get("src")
                if "logo" not in img_src:
                    image_links.append(img_src)
        # driver.close()
        return image_links
    except Exception as e:
        print(e)


def api_request(word):
    word = word.strip()
    word_meaning = get_json(word)
    word_meaning["word"] = word
    image_links = imagescrape(word)
    word_meaning["image_links"] = image_links
    image_links = word_meaning["image_links"]
    if image_links is None:
        image_links = []
    return word_meaning


def run():
    with open(JSON_PATH, "r") as f:
        important_vocabulary_dict = json.load(f)
        all_words = important_vocabulary_dict["all_words"]
    word_meaning_outer_list = []
    c = sum([len(i) for i in all_words])
    if pathlib.Path(DATABASE_PATH).is_file():
        with open(DATABASE_PATH, "r") as f:
            vocabulary_dict = json.load(f)
    else:
        vocabulary_dict = dict()
    for word_list in all_words:
        word_meaning_inner_list = []
        for enum, word in enumerate(word_list):
            word = word.strip()
            word = word.lower()
            c -= 1
            if word in vocabulary_dict:
                continue
            word_meaning_dictionary = api_request(word)
            if (
                word_meaning_dictionary["description"]
                == "We're sorry, your request has been denied."
            ):
                with open(DATABASE_PATH, "w") as f:
                    f.write(json.dumps(vocabulary_dict, indent=4))
                return
            vocabulary_dict[word] = word_meaning_dictionary
            word_meaning_inner_list.append(word_meaning_dictionary)
            print("*" * 100)
            print("*" * 100)
            print("'{}' word is processing".format(word))
            print("{} word are remaining".format(c))
            print("Next checkpoint after {} words".format(len(word_list) - enum))
            print("*" * 100)
            print("*" * 100)
        word_meaning_outer_list.append(word_meaning_inner_list)
        with open(DATABASE_PATH, "w") as f:
            f.write(json.dumps(vocabulary_dict, indent=4))
            total = sum([len(i) for i in all_words])
            print()
            print()
            print("#" * 100)
            print("#" * 100)
            print("*" * 100)
            print("*" * 100)
            print(
                "{} words are saved successfully\n{} word list are remaining...".format(
                    total - c, c
                )
            )
            print("*" * 100)
            print("*" * 100)
            print("#" * 100)
            print("#" * 100)
            print()
            print()


if __name__ == "__main__":
    run()
