import json

# import os
import pathlib
import ssl
import time
import re
from collections import defaultdict
import random

# from io import BytesIO
# from shutil import rmtree
# import filetype
import requests
from bs4 import BeautifulSoup
from flask import Flask, redirect, render_template, request, url_for

# from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# use to initialize driver in a better way without
# having chromedriver path mentioned.
from webdriver_manager.chrome import ChromeDriverManager

from PIL import Image
import requests
from io import BytesIO
import base64

IMAGE_NUMBERS = 28
CACHE_LENGTH = 100
stack = []

app = Flask(__name__)

ROOT_PATH = pathlib.Path(__file__)
BASE_PATH = ROOT_PATH.parent
DATABASE_PATH = (BASE_PATH / "database.json").absolute().as_posix()
IMPORTANT_WORDS_PATH = (BASE_PATH / "important_words.json").absolute().as_posix()

ssl._create_default_https_context = ssl._create_unverified_context


def pillow_image_to_base64_string(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def base64_string_to_pillow_image(base64_str):
    return Image.open(BytesIO(base64.decodebytes(bytes(base64_str, "utf-8"))))
    
    
def read_image_from_url(url, left=0, top=0, right=0, bottom=0):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    x1, y1 = 0, 0
    x2, y2 = image.size
    # Setting the points for cropped image
    left = x1 + left
    if left >= x2:
        print("please check left value.")
        return image, ''
    top = y1 + top
    if top >= y2:
        print("please check top value.")
        return image, ''
    right = x2 - right
    if right <= left:
        print("please check right value.")
        return image, ''
    bottom = y2 - bottom
    if bottom <= top:
        print("please check bottom value.")
        return image, ''
    image = image.crop((left, top, right, bottom))
    cropped_image_url = 'data:image/jpeg;base64,' + pillow_image_to_base64_string(image)
    # You can put this data URL in the address bar of your browser to view the image
    return image, cropped_image_url 


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
    long_def = get_long_definition(page)
    synonym = get_synonym(page)
    type_of = get_type_of(page)
    antonym = get_antonym(page)
    examples = get_sentence(word)
    if "Try the world's fastest, smartest dictionary:".lower() in description["content"].lower():
        description_sentence = ''
    else:
        description_sentence = description["content"]
    json_dict["description"] = description_sentence
    json_dict["shorts"] = shorts
    json_dict["long"] = long_def
    json_dict["synonym"] = synonym
    json_dict["antonym"] = antonym
    json_dict["type_of"] = type_of
    json_dict["examples"] = examples
    json_dict["part_of_speech"] = pos
    return json_dict


def imagescrape(search_term, IMAGE_NUMBERS):
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
        for j in range(IMAGE_NUMBERS):
            if img_container[j].has_attr("src"):
                img_src = img_container[j].get("src")
                if "logo" not in img_src:
                    image_links.append(img_src)
        # if image_links and image_links[0].startswith('https://'):
        #     cropped_image_urls = []
        #     for url in image_links:
        #         image, cropped_image_url  = read_image_from_url(url, left=0, top=0, right=0, bottom=20)
        #         cropped_image_urls.append(cropped_image_url)
        #     image_links = cropped_image_urls
        return image_links
    except Exception as e:
        print(e)


def push(item, stack, length):
    bool_list = [item[3]==s[3] for s in stack]
    if any(bool_list):
        item_index = bool_list.index(True)
        stack.remove(stack[item_index])
        stack.append(item)
        return
    if len(stack) == length:
        stack.append(item)
        stack.pop(0)
    else:
        stack.append(item)
    return stack


def pop(stack):
    if len(stack) != 0:
        item = stack.pop(0)
    else:
        item = None
    return item


@app.route("/check")
def check():
    return "Application is up"

@app.route("/back")
def back():
    item = stack and stack[::-1][0]
    if item:
        word =  item[3]
    else:
        word = ""
    return redirect(url_for("post_request", word=word))

@app.route("/next_word", methods=["GET", "POST"])
def next_word():
    if pathlib.Path(DATABASE_PATH).is_file():
        with open(DATABASE_PATH, "r") as f:
            vocabulary_dict = json.load(f)
            random_number = random.randint(0, len(vocabulary_dict))
            word = sorted(vocabulary_dict.keys())[random_number]
        return redirect(url_for("post_request", word=word))
    else:
        redirect(url_for("book"))


@app.route("/flashback", methods=["GET", "POST"])
def flashback():
    return render_template("flashback.html", stack=stack[::-1])


@app.route("/book_read", methods=["GET", "POST"])
def book():
    if pathlib.Path(IMPORTANT_WORDS_PATH).is_file():
        with open(IMPORTANT_WORDS_PATH, "r") as f:
            important_words_dict = json.load(f)
        book_words_list = important_words_dict["book_words_list"]
        book_items = []
        for book in book_words_list:
            if "blockquote" in book:
                blockquote = book["blockquote"]
            else:
                blockquote = ""
            if "book_name" in book:
                book_name = book["book_name"]
            else:
                book_name = ""
            if "book_words" in book:
                book_words = book["book_words"]
            else:
                book_words = ""
            if "cover_image_link" in book:
                cover_image_link = book["cover_image_link"]
                match = re.search("[?]width=[0-9]{1,3}", cover_image_link)
                match_span = match.span()
                first_index = match_span[0]
                s_image = cover_image_link[:first_index]
                last_index = match_span[-1]
                l_image = cover_image_link[last_index:]
                cover_image_link = s_image + "?width=500" + l_image
            else:
                cover_image_link = "https://cdn.vocab.com/units/kpfxttrx/feature.png?width=500&v=1812a20f6cb"
            book_item = [book_name, book_words, cover_image_link, blockquote]
            book_items.append(book_item)
    else:
        book_items = []
    return render_template("book.html", book_items=book_items)


@app.route("/", methods=["GET", "POST"])
def get_request():
    if request.method == "POST":
        word = request.form["text"]
        return redirect(url_for("post_request", word=word))
    word = ""
    word_meaning = get_json(word)
    word_meaning["word"] = word.upper()
    image_links = []
    return render_template(
        "index.html",
        word=word_meaning["word"],
        antonym=word_meaning["antonym"],
        description=word_meaning["description"],
        image_links=image_links,
        # local_image_files = word_meaning['local_image_files'],
        long=word_meaning["long"],
        shorts=word_meaning["shorts"],
        synonym=word_meaning["synonym"],
        type_of=word_meaning["type_of"],
        examples=word_meaning["examples"],
        part_of_speech=word_meaning["part_of_speech"],
    )


@app.route("/<word>", methods=["GET"])
def post_request(word):
    word = word.strip()
    word = word.lower()
    # if word == "book_read":
    #     redirect(url_for("book"))
    if pathlib.Path(DATABASE_PATH).is_file():
        with open(DATABASE_PATH, "r") as f:
            vocabulary_dict = json.load(f)
    if not (word in vocabulary_dict.keys()):
        # image_folder = BASE_PATH / "temp"
        # os.makedirs(image_folder, exist_ok=True)
        # rmtree(image_folder)
        # os.makedirs(image_folder, exist_ok=True)
        word_meaning = get_json(word)
        image_links = imagescrape(word, IMAGE_NUMBERS)
        word_meaning["image_links"] = image_links
        vocabulary_dict[word.lower()] = word_meaning
        if (
            vocabulary_dict[word.lower()]["description"]
            != "We're sorry, your request has been denied."
        ):
            with open(DATABASE_PATH, "w") as f:
                f.write(json.dumps(vocabulary_dict, indent=4))
    else:
        word_meaning = vocabulary_dict[word]
    word_meaning["word"] = word.upper()
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
    image_links = word_meaning["image_links"][:IMAGE_NUMBERS]
    if image_links is None:
        image_links = []
    print("word_meaning", word_meaning)
    item = word_meaning
    image_links_index = random.randint(0, len(image_links)-1)
    url = image_links and image_links[image_links_index]
    _, cropped_image_url  = read_image_from_url(url, left=0, top=0, right=0, bottom=20)
    item['cropped_image_url'] = cropped_image_url
    
    if word_meaning["examples"]:
        examples_index = random.randint(0, len(word_meaning["examples"])-1)
        example = word_meaning["examples"][examples_index]
    else:
        example = ''
    if word_meaning["word"].upper() != 'FAVICON.ICO':
        memory = [
            cropped_image_url, 
            word_meaning["description"],
            example,
            word_meaning["word"],
            word_meaning["synonym"]
        ]
        
        push(memory, stack, CACHE_LENGTH)
    return render_template(
        "index.html",
        word=word_meaning["word"],
        antonym=word_meaning["antonym"],
        description=word_meaning["description"],
        image_links=image_links,
        # local_image_files = word_meaning['local_image_files'],
        long=word_meaning["long"],
        shorts=word_meaning["shorts"],
        synonym=word_meaning["synonym"],
        type_of=word_meaning["type_of"],
        examples=word_meaning["examples"],
        part_of_speech=word_meaning["part_of_speech"],
        stack = stack[::-1]
    )


@app.route("/api/<word>", methods=["GET"])
def api_request(word):
    word = word.strip()
    word = word.lower()
    if pathlib.Path(DATABASE_PATH).is_file():
        with open(DATABASE_PATH, "r") as f:
            vocabulary_dict = json.load(f)
    else:
        vocabulary_dict = {}
    if not (word in vocabulary_dict.keys()):
        word_meaning = get_json(word)
        word_meaning["word"] = word
        image_links = imagescrape(word, IMAGE_NUMBERS)
        word_meaning["image_links"] = image_links[:IMAGE_NUMBERS]
        image_links = word_meaning["image_links"]
        vocabulary_dict[word.lower()] = word_meaning
        if (
            vocabulary_dict[word.lower()]["description"]
            != "We're sorry, your request has been denied."
        ):
            with open(DATABASE_PATH, "w") as f:
                f.write(json.dumps(vocabulary_dict, indent=4))
    else:
        word_meaning = vocabulary_dict[word]
    return word_meaning


if __name__ == "__main__":
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
    app.run(host="0.0.0.0", port=5000)
    driver.close()
