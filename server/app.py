# import os
import pathlib
import ssl
import time

# from io import BytesIO
# from shutil import rmtree
# import filetype
import requests
from bs4 import BeautifulSoup
from flask import Flask, redirect, render_template, request, url_for

# from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import (
    ChromeDriverManager,
)  # use to initialize driver in a better way without having chromedriver path mentioned.

app = Flask(__name__)

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
    scraper = BeautifulSoup(data, "lxml")
    return str(scraper)


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
    soup = BeautifulSoup(page)
    sentence_example_div = soup.findAll("div", {"class": "sentence"})
    examples = []
    for sentence_div in sentence_example_div:
        examples.append(str(sentence_div.text))
    return examples


def get_json(word):
    json_dict = {}
    page = get_page(word)
    description = get_description(page)
    short_def = get_short_definition(page)
    long_def = get_long_definition(page)
    synonym = get_synonym(page)
    type_of = get_type_of(page)
    antonym = get_antonym(page)
    examples = get_sentence(word)
    json_dict["description"] = description["content"]
    json_dict["short"] = short_def
    json_dict["long"] = long_def
    json_dict["synonym"] = synonym
    json_dict["antonym"] = antonym
    json_dict["type_of"] = type_of
    json_dict["examples"] = examples
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
        for j in range(15):
            if img_container[j].has_attr("src"):
                img_src = img_container[j].get("src")
                if "logo" not in img_src:
                    image_links.append(img_src)
        # driver.close()
        return image_links
    except Exception as e:
        print(e)


@app.route("/check")
def check():
    return "Application is up"


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        word = request.form["text"]
        return redirect(url_for("word_dict", word=word))
    else:
        word = request.args.get("text")
        return render_template("home.html")


@app.route("/scrap/<word>")
def word_dict(word):
    # image_folder = BASE_PATH / "temp"
    # os.makedirs(image_folder, exist_ok=True)
    # rmtree(image_folder)
    # os.makedirs(image_folder, exist_ok=True)
    word_meaning = get_json(word)
    word_meaning["word"] = word
    image_links = imagescrape(word)
    word_meaning["image_links"] = image_links
    # local_image_files = []
    # for url in image_links:
    #     response = requests.get(url)
    #     byte_data = BytesIO(response.content)
    #     extension = filetype.guess_extension(byte_data)
    #     img = Image.open(byte_data).convert("RGB")
    #     url_pathlib = pathlib.Path(url)
    #     image_file = image_folder / url_pathlib.name
    #     image_file = image_file.as_posix()
    #     if extension=='jpg':
    #         extension = 'jpeg'
    #     img.save(image_file, extension)
    #     local_image_files.append(image_file)
    # word_meaning["local_image_files"] = local_image_files
    image_links = word_meaning["image_links"]
    if image_links is None:
        image_links = []
    print("word_meaning", word_meaning)
    return render_template(
        "index.html",
        word=word_meaning["word"].upper(),
        antonym=word_meaning["antonym"],
        description=word_meaning["description"],
        image_links=image_links,
        # local_image_files = word_meaning['local_image_files'],
        long=word_meaning["long"],
        short=word_meaning["short"],
        synonym=word_meaning["synonym"],
        type_of=word_meaning["type_of"],
        examples=word_meaning["examples"],
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
