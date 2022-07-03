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
OUTPUT_JSON_PATH = (BASE_PATH / "important_literature_words.json").absolute().as_posix()
# with open(OUTPUT_JSON_PATH, "r") as f:
#     FINAL_DICTIONARY = eval(f.read())

# VOCABULARY_LIST = []
# for all_words in FINAL_DICTIONARY['all_words']:
#     for words in all_words:
#         VOCABULARY_LIST.extend([word.lower().strip() for word in words])

with open(IMPORTANT_WORDS_PATH, "r") as f:
    IMPORTANT_WORDS_DICT = eval(f.read())

IMPORTANT_WORD_LIST = []
for all_words in IMPORTANT_WORDS_DICT["all_words"]:
    for word in all_words:
        IMPORTANT_WORD_LIST.append(word)


ssl._create_default_https_context = ssl._create_unverified_context


# coding:utf-8
# author LuShan
# version : 1.1.9
from urllib.parse import quote
import urllib3
import logging

LANGUAGES = {
    "af": "afrikaans",
    "sq": "albanian",
    "am": "amharic",
    "ar": "arabic",
    "hy": "armenian",
    "az": "azerbaijani",
    "eu": "basque",
    "be": "belarusian",
    "bn": "bengali",
    "bs": "bosnian",
    "bg": "bulgarian",
    "ca": "catalan",
    "ceb": "cebuano",
    "ny": "chichewa",
    "zh-cn": "chinese (simplified)",
    "zh-tw": "chinese (traditional)",
    "co": "corsican",
    "hr": "croatian",
    "cs": "czech",
    "da": "danish",
    "nl": "dutch",
    "en": "english",
    "eo": "esperanto",
    "et": "estonian",
    "tl": "filipino",
    "fi": "finnish",
    "fr": "french",
    "fy": "frisian",
    "gl": "galician",
    "ka": "georgian",
    "de": "german",
    "el": "greek",
    "gu": "gujarati",
    "ht": "haitian creole",
    "ha": "hausa",
    "haw": "hawaiian",
    "iw": "hebrew",
    "he": "hebrew",
    "hi": "hindi",
    "hmn": "hmong",
    "hu": "hungarian",
    "is": "icelandic",
    "ig": "igbo",
    "id": "indonesian",
    "ga": "irish",
    "it": "italian",
    "ja": "japanese",
    "jw": "javanese",
    "kn": "kannada",
    "kk": "kazakh",
    "km": "khmer",
    "ko": "korean",
    "ku": "kurdish (kurmanji)",
    "ky": "kyrgyz",
    "lo": "lao",
    "la": "latin",
    "lv": "latvian",
    "lt": "lithuanian",
    "lb": "luxembourgish",
    "mk": "macedonian",
    "mg": "malagasy",
    "ms": "malay",
    "ml": "malayalam",
    "mt": "maltese",
    "mi": "maori",
    "mr": "marathi",
    "mn": "mongolian",
    "my": "myanmar (burmese)",
    "ne": "nepali",
    "no": "norwegian",
    "or": "odia",
    "ps": "pashto",
    "fa": "persian",
    "pl": "polish",
    "pt": "portuguese",
    "pa": "punjabi",
    "ro": "romanian",
    "ru": "russian",
    "sm": "samoan",
    "gd": "scots gaelic",
    "sr": "serbian",
    "st": "sesotho",
    "sn": "shona",
    "sd": "sindhi",
    "si": "sinhala",
    "sk": "slovak",
    "sl": "slovenian",
    "so": "somali",
    "es": "spanish",
    "su": "sundanese",
    "sw": "swahili",
    "sv": "swedish",
    "tg": "tajik",
    "ta": "tamil",
    "tt": "tatar",
    "te": "telugu",
    "th": "thai",
    "tr": "turkish",
    "tk": "turkmen",
    "uk": "ukrainian",
    "ur": "urdu",
    "ug": "uyghur",
    "uz": "uzbek",
    "vi": "vietnamese",
    "cy": "welsh",
    "xh": "xhosa",
    "yi": "yiddish",
    "yo": "yoruba",
    "zu": "zulu",
}

DEFAULT_SERVICE_URLS = (
    "translate.google.ac",
    "translate.google.ad",
    "translate.google.ae",
    "translate.google.al",
    "translate.google.am",
    "translate.google.as",
    "translate.google.at",
    "translate.google.az",
    "translate.google.ba",
    "translate.google.be",
    "translate.google.bf",
    "translate.google.bg",
    "translate.google.bi",
    "translate.google.bj",
    "translate.google.bs",
    "translate.google.bt",
    "translate.google.by",
    "translate.google.ca",
    "translate.google.cat",
    "translate.google.cc",
    "translate.google.cd",
    "translate.google.cf",
    "translate.google.cg",
    "translate.google.ch",
    "translate.google.ci",
    "translate.google.cl",
    "translate.google.cm",
    "translate.google.cn",
    "translate.google.co.ao",
    "translate.google.co.bw",
    "translate.google.co.ck",
    "translate.google.co.cr",
    "translate.google.co.id",
    "translate.google.co.il",
    "translate.google.co.in",
    "translate.google.co.jp",
    "translate.google.co.ke",
    "translate.google.co.kr",
    "translate.google.co.ls",
    "translate.google.co.ma",
    "translate.google.co.mz",
    "translate.google.co.nz",
    "translate.google.co.th",
    "translate.google.co.tz",
    "translate.google.co.ug",
    "translate.google.co.uk",
    "translate.google.co.uz",
    "translate.google.co.ve",
    "translate.google.co.vi",
    "translate.google.co.za",
    "translate.google.co.zm",
    "translate.google.co.zw",
    "translate.google.co",
    "translate.google.com.af",
    "translate.google.com.ag",
    "translate.google.com.ai",
    "translate.google.com.ar",
    "translate.google.com.au",
    "translate.google.com.bd",
    "translate.google.com.bh",
    "translate.google.com.bn",
    "translate.google.com.bo",
    "translate.google.com.br",
    "translate.google.com.bz",
    "translate.google.com.co",
    "translate.google.com.cu",
    "translate.google.com.cy",
    "translate.google.com.do",
    "translate.google.com.ec",
    "translate.google.com.eg",
    "translate.google.com.et",
    "translate.google.com.fj",
    "translate.google.com.gh",
    "translate.google.com.gi",
    "translate.google.com.gt",
    "translate.google.com.hk",
    "translate.google.com.jm",
    "translate.google.com.kh",
    "translate.google.com.kw",
    "translate.google.com.lb",
    "translate.google.com.lc",
    "translate.google.com.ly",
    "translate.google.com.mm",
    "translate.google.com.mt",
    "translate.google.com.mx",
    "translate.google.com.my",
    "translate.google.com.na",
    "translate.google.com.ng",
    "translate.google.com.ni",
    "translate.google.com.np",
    "translate.google.com.om",
    "translate.google.com.pa",
    "translate.google.com.pe",
    "translate.google.com.pg",
    "translate.google.com.ph",
    "translate.google.com.pk",
    "translate.google.com.pr",
    "translate.google.com.py",
    "translate.google.com.qa",
    "translate.google.com.sa",
    "translate.google.com.sb",
    "translate.google.com.sg",
    "translate.google.com.sl",
    "translate.google.com.sv",
    "translate.google.com.tj",
    "translate.google.com.tr",
    "translate.google.com.tw",
    "translate.google.com.ua",
    "translate.google.com.uy",
    "translate.google.com.vc",
    "translate.google.com.vn",
    "translate.google.com",
    "translate.google.cv",
    "translate.google.cx",
    "translate.google.cz",
    "translate.google.de",
    "translate.google.dj",
    "translate.google.dk",
    "translate.google.dm",
    "translate.google.dz",
    "translate.google.ee",
    "translate.google.es",
    "translate.google.eu",
    "translate.google.fi",
    "translate.google.fm",
    "translate.google.fr",
    "translate.google.ga",
    "translate.google.ge",
    "translate.google.gf",
    "translate.google.gg",
    "translate.google.gl",
    "translate.google.gm",
    "translate.google.gp",
    "translate.google.gr",
    "translate.google.gy",
    "translate.google.hn",
    "translate.google.hr",
    "translate.google.ht",
    "translate.google.hu",
    "translate.google.ie",
    "translate.google.im",
    "translate.google.io",
    "translate.google.iq",
    "translate.google.is",
    "translate.google.it",
    "translate.google.je",
    "translate.google.jo",
    "translate.google.kg",
    "translate.google.ki",
    "translate.google.kz",
    "translate.google.la",
    "translate.google.li",
    "translate.google.lk",
    "translate.google.lt",
    "translate.google.lu",
    "translate.google.lv",
    "translate.google.md",
    "translate.google.me",
    "translate.google.mg",
    "translate.google.mk",
    "translate.google.ml",
    "translate.google.mn",
    "translate.google.ms",
    "translate.google.mu",
    "translate.google.mv",
    "translate.google.mw",
    "translate.google.ne",
    "translate.google.nf",
    "translate.google.nl",
    "translate.google.no",
    "translate.google.nr",
    "translate.google.nu",
    "translate.google.pl",
    "translate.google.pn",
    "translate.google.ps",
    "translate.google.pt",
    "translate.google.ro",
    "translate.google.rs",
    "translate.google.ru",
    "translate.google.rw",
    "translate.google.sc",
    "translate.google.se",
    "translate.google.sh",
    "translate.google.si",
    "translate.google.sk",
    "translate.google.sm",
    "translate.google.sn",
    "translate.google.so",
    "translate.google.sr",
    "translate.google.st",
    "translate.google.td",
    "translate.google.tg",
    "translate.google.tk",
    "translate.google.tl",
    "translate.google.tm",
    "translate.google.tn",
    "translate.google.to",
    "translate.google.tt",
    "translate.google.us",
    "translate.google.vg",
    "translate.google.vu",
    "translate.google.ws",
)

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URLS_SUFFIX = [
    re.search("translate.google.(.*)", url.strip()).group(1)
    for url in DEFAULT_SERVICE_URLS
]
URL_SUFFIX_DEFAULT = "cn"


class google_new_transError(Exception):
    """Exception that uses context to present a meaningful error message"""

    def __init__(self, msg=None, **kwargs):
        self.tts = kwargs.pop("tts", None)
        self.rsp = kwargs.pop("response", None)
        if msg:
            self.msg = msg
        elif self.tts is not None:
            self.msg = self.infer_msg(self.tts, self.rsp)
        else:
            self.msg = None
        super(google_new_transError, self).__init__(self.msg)

    def infer_msg(self, tts, rsp=None):
        cause = "Unknown"

        if rsp is None:
            premise = "Failed to connect"

            return "{}. Probable cause: {}".format(premise, "timeout")
            # if tts.tld != 'com':
            #     host = _translate_url(tld=tts.tld)
            #     cause = "Host '{}' is not reachable".format(host)

        else:
            status = rsp.status_code
            reason = rsp.reason

            premise = "{:d} ({}) from TTS API".format(status, reason)

            if status == 403:
                cause = "Bad token or upstream API changes"
            elif status == 200 and not tts.lang_check:
                cause = (
                    "No audio stream in response. Unsupported language '%s'"
                    % self.tts.lang
                )
            elif status >= 500:
                cause = "Uptream API error. Try again later."

        return "{}. Probable cause: {}".format(premise, cause)


class google_translator:
    """
    You can use 108 language in target and source,details view LANGUAGES.
    Target language: like 'en'、'zh'、'th'...

    :param url_suffix: The source text(s) to be translated. Batch translation is supported via sequence input.
                       The value should be one of the url_suffix listed in : `DEFAULT_SERVICE_URLS`
    :type url_suffix: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)

    :param text: The source text(s) to be translated.
    :type text: UTF-8 :class:`str`; :class:`unicode`;

    :param lang_tgt: The language to translate the source text into.
                     The value should be one of the language codes listed in : `LANGUAGES`
    :type lang_tgt: :class:`str`; :class:`unicode`

    :param lang_src: The language of the source text.
                    The value should be one of the language codes listed in :const:`googletrans.LANGUAGES`
                    If a language is not specified,
                    the system will attempt to identify the source language automatically.
    :type lang_src: :class:`str`; :class:`unicode`

    :param timeout: Timeout Will be used for every request.
    :type timeout: number or a double of numbers

    :param proxies: proxies Will be used for every request.
    :type proxies: class : dict; like: {'http': 'http:171.112.169.47:19934/', 'https': 'https:171.112.169.47:19934/'}

    """

    def __init__(self, url_suffix="cn", timeout=5, proxies=None):
        self.proxies = proxies
        if url_suffix not in URLS_SUFFIX:
            self.url_suffix = URL_SUFFIX_DEFAULT
        else:
            self.url_suffix = url_suffix
        url_base = "https://translate.google.{}".format(self.url_suffix)
        self.url = url_base + "/_/TranslateWebserverUi/data/batchexecute"
        self.timeout = timeout

    def _package_rpc(self, text, lang_src="auto", lang_tgt="auto"):
        GOOGLE_TTS_RPC = ["MkEWBc"]
        parameter = [[text.strip(), lang_src, lang_tgt, True], [1]]
        escaped_parameter = json.dumps(parameter, separators=(",", ":"))
        rpc = [[[random.choice(GOOGLE_TTS_RPC), escaped_parameter, None, "generic"]]]
        espaced_rpc = json.dumps(rpc, separators=(",", ":"))
        # text_urldecode = quote(text.strip())
        freq_initial = "f.req={}&".format(quote(espaced_rpc))
        freq = freq_initial
        return freq

    def translate(self, text, lang_tgt="auto", lang_src="auto", pronounce=False):
        try:
            lang = LANGUAGES[lang_src]
        except:
            lang_src = "auto"
        try:
            lang = LANGUAGES[lang_tgt]
        except:
            lang_src = "auto"
        text = str(text)
        if len(text) >= 5000:
            return "Warning: Can only detect less than 5000 characters"
        if len(text) == 0:
            return ""
        headers = {
            "Referer": "http://translate.google.{}/".format(self.url_suffix),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/47.0.2526.106 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        freq = self._package_rpc(text, lang_src, lang_tgt)
        response = requests.Request(
            method="POST",
            url=self.url,
            data=freq,
            headers=headers,
        )
        try:
            if self.proxies == None or type(self.proxies) != dict:
                self.proxies = {}
            with requests.Session() as s:
                s.proxies = self.proxies
                r = s.send(
                    request=response.prepare(), verify=False, timeout=self.timeout
                )
            for line in r.iter_lines(chunk_size=1024):
                decoded_line = line.decode("utf-8")
                if "MkEWBc" in decoded_line:
                    try:
                        response = decoded_line
                        response = json.loads(response)
                        response = list(response)
                        response = json.loads(response[0][2])
                        response_ = list(response)
                        response = response_[1][0]
                        if len(response) == 1:
                            if len(response[0]) > 5:
                                sentences = response[0][5]
                            else:  ## only url
                                sentences = response[0][0]
                                if pronounce == False:
                                    return sentences
                                elif pronounce == True:
                                    return [sentences, None, None]
                            translate_text = ""
                            for sentence in sentences:
                                sentence = sentence[0]
                                translate_text += sentence.strip() + " "
                            translate_text = translate_text
                            if pronounce == False:
                                return translate_text
                            elif pronounce == True:
                                pronounce_src = response_[0][0]
                                pronounce_tgt = response_[1][0][0][1]
                                return [translate_text, pronounce_src, pronounce_tgt]
                        elif len(response) == 2:
                            sentences = []
                            for i in response:
                                sentences.append(i[0])
                            if pronounce == False:
                                return sentences
                            elif pronounce == True:
                                pronounce_src = response_[0][0]
                                pronounce_tgt = response_[1][0][0][1]
                                return [sentences, pronounce_src, pronounce_tgt]
                    except Exception as e:
                        raise e
            r.raise_for_status()
        except requests.exceptions.ConnectTimeout as e:
            raise e
        except requests.exceptions.HTTPError as e:
            # Request successful, bad response
            raise google_new_transError(tts=self, response=r)
        except requests.exceptions.RequestException as e:
            # Request failed
            raise google_new_transError(tts=self)

    def detect(self, text):
        text = str(text)
        if len(text) >= 5000:
            return log.debug("Warning: Can only detect less than 5000 characters")
        if len(text) == 0:
            return ""
        headers = {
            "Referer": "http://translate.google.{}/".format(self.url_suffix),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/47.0.2526.106 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        freq = self._package_rpc(text)
        response = requests.Request(
            method="POST", url=self.url, data=freq, headers=headers
        )
        try:
            if self.proxies == None or type(self.proxies) != dict:
                self.proxies = {}
            with requests.Session() as s:
                s.proxies = self.proxies
                r = s.send(
                    request=response.prepare(), verify=False, timeout=self.timeout
                )

            for line in r.iter_lines(chunk_size=1024):
                decoded_line = line.decode("utf-8")
                if "MkEWBc" in decoded_line:
                    # regex_str = r"\[\[\"wrb.fr\",\"MkEWBc\",\"\[\[(.*).*?,\[\[\["
                    try:
                        # data_got = re.search(regex_str,decoded_line).group(1)
                        response = decoded_line
                        response = json.loads(response)
                        response = list(response)
                        response = json.loads(response[0][2])
                        response = list(response)
                        detect_lang = response[0][2]
                    except Exception:
                        raise Exception
                    # data_got = data_got.split('\\\"]')[0]
                    return [detect_lang, LANGUAGES[detect_lang.lower()]]
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # Request successful, bad response
            log.debug(str(e))
            raise google_new_transError(tts=self, response=r)
        except requests.exceptions.RequestException as e:
            # Request failed
            log.debug(str(e))
            raise google_new_transError(tts=self)


translator = google_translator()


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
        return image, ""
    top = y1 + top
    if top >= y2:
        print("please check top value.")
        return image, ""
    right = x2 - right
    if right <= left:
        print("please check right value.")
        return image, ""
    bottom = y2 - bottom
    if bottom <= top:
        print("please check bottom value.")
        return image, ""
    image = image.crop((left, top, right, bottom))
    cropped_image_url = "data:image/jpeg;base64," + pillow_image_to_base64_string(image)
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
    if (
        "Try the world's fastest, smartest dictionary:".lower()
        in description["content"].lower()
    ):
        description_sentence = ""
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
    bool_list = [item[3] == s[3] for s in stack]
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
        word = item[3]
    else:
        word = ""
    return redirect(url_for("post_request", word=word))


@app.route("/next_word/", methods=["GET", "POST"], defaults={"word": "random_word"})
@app.route("/next_word/<word>", methods=["GET", "POST"])
def next_word(word):
    if pathlib.Path(DATABASE_PATH).is_file():
        with open(DATABASE_PATH, "r") as f:
            vocabulary_dict = json.load(f)
        if word == "random_word":
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
    if word == "favicon.ico":
        return render_template(
            "index.html",
            word="",
            antonym=[],
            description="",
            image_links=[],
            # local_image_files = word_meaning['local_image_files'],
            long="",
            shorts="",
            synonym=[],
            type_of=[],
            examples=[],
            part_of_speech=[],
            stack=stack[::-1],
            vocabulary="",
            next_word="random_word",
        )
    # if word == "book_read":
    #     redirect(url_for("book"))
    if pathlib.Path(DATABASE_PATH).is_file():
        with open(DATABASE_PATH, "r") as f:
            vocabulary_dict = json.load(f)
    if "hindi_translated_word" not in vocabulary_dict[word].keys():
        hindi_translated_word = translator.translate(word, lang_tgt="hi")
        vocabulary_dict[word]["hindi_translated_word"] = hindi_translated_word
    if not (word in vocabulary_dict.keys()):
        # image_folder = BASE_PATH / "temp"
        # os.makedirs(image_folder, exist_ok=True)
        # rmtree(image_folder)
        # os.makedirs(image_folder, exist_ok=True)
        tic = time.time()
        word_meaning = get_json(word)
        toc = time.time()
        print(toc - tic)
        tic = time.time()
        image_links = imagescrape(word)
        toc = time.time()
        print(toc - tic)
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
    if word_meaning["image_links"] is None:
        word_meaning["image_links"] = []
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
    image_links = (
        "image_links" in word_meaning and word_meaning["image_links"][:IMAGE_NUMBERS]
    )
    item = word_meaning
    image_links_index = len(image_links) and random.randint(0, len(image_links) - 1)
    url = image_links and image_links[image_links_index]
    if url:
        _, cropped_image_url = read_image_from_url(
            url, left=0, top=0, right=0, bottom=20
        )
    else:
        cropped_image_url = (
            "https://cdn.vocab.com/units/kpfxttrx/feature.png?width=500&v=1812a20f6cb"
        )
    item["cropped_image_url"] = cropped_image_url
    if word_meaning["examples"]:
        examples_index = random.randint(0, len(word_meaning["examples"]) - 1)
        example = word_meaning["examples"][examples_index]
    else:
        example = ""
    # related_words = ''
    # related_words += word_meaning['description']
    # related_words += ' '
    # for w in word_meaning['shorts']:
    #     related_words += w
    #     related_words += ' '
    # related_words += word_meaning['long']
    # related_words += ' '
    # for w in word_meaning['synonym']:
    #     related_words += w
    #     related_words += ' '
    # for w in word_meaning['antonym']:
    #     related_words += w
    #     related_words += ' '
    # for example in word_meaning['examples']:
    #     related_words += example
    #     related_words += ' '
    # re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    # re_print = re.compile('[^%s]' % re.escape(string.printable))
    # line = normalize('NFD', related_words).encode('ascii', 'ignore')
    # line = line.decode('UTF-8')
    # tokens = line.split()
    # tokens = [word.lower() for word in tokens]
    # tokens = [re_punc.sub('', w) for w in tokens]
    # tokens = [re_print.sub('', w) for w in tokens]
    # tokens = [word for word in tokens if word.isalpha()]
    # tokens = [w for w in tokens if not w in STOPWORDS]
    # token_dictionary = Counter(tokens)
    # vocabulary = dict()
    # for k, v in token_dictionary.items():
    #     if k != word and k not in ['noun', 'pronoun',
    #                                'verb', 'adjective',
    #                                'adverb', 'preposition',
    #                                'conjunction']:
    #             if k not in [stack_item[3].lower() for stack_item in stack]:
    #                 if k in IMPORTANT_WORD_LIST:
    #                     vocabulary[k]=v
    # vocabulary = sorted(token_dictionary, key=lambda x: len(x))[::-1]
    # if word in vocabulary:
    #     del vocabulary[word]
    if "vocabulary" not in vocabulary_dict[word].keys():
        word_url = "http://wordnetweb.princeton.edu/perl/webwn?s={}".format(word)
        wordnet_api = requests.get(word_url)
        vocabulary = []
        wordnet_soup = BeautifulSoup(wordnet_api.text, features="lxml")
        for a_div in wordnet_soup.findAll("a"):
            if "href" in a_div.attrs and a_div.attrs["href"].startswith("webwn?"):
                text = a_div.text
                if text in [stack_item[3].lower() for stack_item in stack]:
                    continue
                if text != "S:":
                    vocabulary.append(text)
        vocabulary_dict[word]["vocabulary"] = vocabulary

    if word in vocabulary_dict[word]["vocabulary"]:
        vocabulary_dict[word]["vocabulary"].remove(word)
    if word_meaning["word"].upper() != "FAVICON.ICO":
        memory = [
            cropped_image_url,
            word_meaning["description"],
            example,
            word_meaning["word"],
            vocabulary_dict[word]["vocabulary"],
            vocabulary_dict[word]["hindi_translated_word"],
        ]
        push(memory, stack, CACHE_LENGTH)

    vocab_words = vocabulary_dict[word]["vocabulary"]
    vocab_words = sorted(vocab_words, key=lambda x: len(x))[::-1]
    next_word = vocab_words and vocab_words[0]
    while next_word:
        if next_word in [stack_item[3].lower() for stack_item in stack]:
            next_word = vocab_words and vocab_words[0]
            continue
        else:
            break
    if not next_word:
        next_word = "random_word"
    if not vocabulary_dict[word]["vocabulary"]:
        next_word = "random_word"
    if not next_word or next_word.upper() == "FAVICON.ICO":
        next_word = "random_word"
    print("*****************")
    print("word_meaning", word_meaning)
    print("*****************")
    print("next_word", next_word)
    print()
    with open(DATABASE_PATH, "w") as f:
        f.write(json.dumps(vocabulary_dict, indent=4))
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
        stack=stack[::-1],
        vocabulary=vocabulary_dict[word]["vocabulary"],
        next_word=next_word,
        hindi_translated_word=vocabulary_dict[word]["hindi_translated_word"],
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
    if "vocabulary" not in vocabulary_dict[word].keys():
        word_url = "http://wordnetweb.princeton.edu/perl/webwn?s={}".format(word)
        wordnet_api = requests.get(word_url)
        vocabulary = []
        wordnet_soup = BeautifulSoup(wordnet_api.text, features="lxml")
        for a_div in wordnet_soup.findAll("a"):
            if "href" in a_div.attrs and a_div.attrs["href"].startswith("webwn?"):
                text = a_div.text
                if text in [stack_item[3].lower() for stack_item in stack]:
                    continue
                if text != "S:":
                    vocabulary.append(text)
        vocabulary_dict[word]["vocabulary"] = vocabulary
    if "hindi_translated_word" not in vocabulary_dict[word].keys():
        hindi_translated_word = translator.translate(word, lang_tgt="hi")
        vocabulary_dict[word]["hindi_translated_word"] = hindi_translated_word
    if not (word in vocabulary_dict.keys()):
        word_meaning = get_json(word)
        word_meaning["word"] = word
        image_links = imagescrape(word)
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
