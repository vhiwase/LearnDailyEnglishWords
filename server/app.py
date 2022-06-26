import ssl
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import (
    ChromeDriverManager,
)  # use to initialize driver in a better way without having chromedriver path mentioned.

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


def get_description(content):
    soup = BeautifulSoup(content)
    meta_content_list = soup.findAll("meta", {"name": "description"})
    meta_content = meta_content_list and meta_content_list[0]
    return meta_content.attrs


def get_definition(content, get_type):
    soup = BeautifulSoup(content)
    short_def_div = soup.findAll("p", {"class": get_type})
    if len(short_def_div) == 0:
        return ""
    assert len(short_def_div) == 1
    short_def_div = short_def_div[0]
    return short_def_div.get_text()


def get_short_definition(content):
    return get_definition(content, "short")


def get_long_definition(content):
    return get_definition(content, "long")


def get_instance(content, ins_type):
    soup = BeautifulSoup(content)
    instance_div = soup.findAll("dl", {"class": "instances"})
    if ins_type == "synonym":
        ch_type = "Synonyms:"
    if ins_type == "antonym":
        ch_type = "Antonyms:"
    if ins_type == "type_of":
        ch_type = "Type of:"
    res = {}
    for instance in instance_div:
        dt_div = instance.findAll("dt")
        if not dt_div:
            return []
        assert len(dt_div) == 1
        dt_div = dt_div[0]
        if dt_div.get_text() != "":
            current_type = dt_div.get_text()
        if current_type == ch_type:
            a_div = instance.findAll("a", {"class": "word"})
        for word_div in a_div:
            word = word_div.get_text()
            res[word] = ""
    ret = []
    for key in res:
        ret.append(key)
    return ret


def get_synonym(content):
    return get_instance(content, "synonym")


def get_type_of(content):
    return get_instance(content, "type_of")


def get_antonym(content):
    return get_instance(content, "antonym")


def get_json(word):
    json_dict = {}
    page = get_page(word)
    description = get_description(page)
    short_def = get_short_definition(page)
    long_def = get_long_definition(page)
    synonym = get_synonym(page)
    type_of = get_type_of(page)
    antonym = get_antonym(page)
    json_dict["description"] = description["content"]
    json_dict["short"] = short_def
    json_dict["long"] = long_def
    json_dict["synonym"] = synonym
    json_dict["antonym"] = antonym
    json_dict["type_of"] = type_of
    # json.dumps(json_dict, indent = 4)
    return json_dict


def imagescrape(search_term):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
        except Exception as e:
            print(e)
            driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=chrome_options
            )  # chrome_options is deprecated
            driver.maximize_window()
        url = (
            "https://www.shutterstock.com/search?search_term="
            + search_term
            + "&sort=popular&image_type="
            + "photo"
            + "&search_source=base_landing_page&language=en&page="
            + str(1)
        )
        driver.get(url)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight)"
        )  # Scroll to the bottom of the page
        time.sleep(4)  # Wait 4 seconds for all the images to load
        data = driver.execute_script("return document.documentElement.outerHTML")
        scraper = BeautifulSoup(data, "lxml")
        img_container = scraper.find_all("img")
        image_links = []
        for j in range(15):
            if img_container[j].has_attr("src"):
                img_src = img_container[j].get("src")
                if "logo" not in img_src:
                    image_links.append(img_src)
        driver.close()
        return image_links
    except Exception as e:
        print(e)


if __name__ == "__main__":
    word = "photo"
    word_meaning = get_json(word)
    image_links = imagescrape(word)
    print(image_links)
    print(word_meaning)
