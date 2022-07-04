import json
import pathlib

ROOT_PATH = pathlib.Path(__file__)
BASE_PATH = ROOT_PATH.parent
pathlib.sys.path.insert(0, BASE_PATH)

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

# use to initialize driver in a better way without
# having chromedriver path mentioned.
from webdriver_manager.chrome import ChromeDriverManager

JSON_PATH = (BASE_PATH / "important_words.json").absolute().as_posix()
DATABASE_PATH = (BASE_PATH / "database.json").absolute().as_posix()


"""
pip install beautifulsoup4
pip install selenium
pip install lxml
pip install webdriver-manager
"""


# coding:utf-8
# author LuShan
# version : 1.1.9
from urllib.parse import quote
import urllib3
import logging
import re
import random

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
    c = sum([len(i) for i in all_words])
    if pathlib.Path(DATABASE_PATH).is_file():
        with open(DATABASE_PATH, "r") as f:
            vocabulary_dict = json.load(f)
    else:
        vocabulary_dict = dict()
    total = sum([len(i) for i in all_words])
    for word_list in all_words:
        adding_words = False
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
            adding_words = True
            print("*" * 100)
            print("*" * 100)
            print("'{}' word is processing".format(word))
            print("{} word are remaining".format(c))
            print("Next checkpoint after {} words".format(len(word_list) - enum))
            print("*" * 100)
            print("*" * 100)
        if adding_words:
            with open(DATABASE_PATH, "w") as f:
                f.write(json.dumps(vocabulary_dict, indent=4))
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
        else:
            print()
            print()
            print("#" * 100)
            print("#" * 100)
            print("*" * 100)
            print("*" * 100)
            print(
                "{} words are already saved successfully\n{} word list are remaining...".format(
                    total - c, c
                )
            )
            print("*" * 100)
            print("*" * 100)
            print("#" * 100)
            print("#" * 100)
            print()
            print()

    cc = len(vocabulary_dict.keys())
    for key_word in vocabulary_dict.keys():
        cc -= 1
        if "hindi_translated_word" not in vocabulary_dict[key_word].keys():
            try:
                hindi_translated_word = translator.translate(key_word, lang_tgt="hi")
            except:
                hindi_translated_word = ""
            vocabulary_dict[key_word]["hindi_translated_word"] = hindi_translated_word
        if "vocabulary" not in vocabulary_dict[key_word].keys():
            word_url = "http://wordnetweb.princeton.edu/perl/webwn?s={}".format(
                key_word
            )
            wordnet_api = requests.get(word_url)
            vocabulary = []
            wordnet_soup = BeautifulSoup(wordnet_api.text, features="lxml")
            for a_div in wordnet_soup.findAll("a"):
                if "href" in a_div.attrs and a_div.attrs["href"].startswith("webwn?"):
                    text = a_div.text
                    if text != "S:":
                        vocabulary.append(text)
            vocabulary_dict[key_word]["vocabulary"] = vocabulary
        if cc % len(vocabulary_dict.keys()) == 0:
            print()
            print("Saving files...")
            with open(DATABASE_PATH, "w") as f:
                f.write(json.dumps(vocabulary_dict, indent=4))
        print()
        print("****************")
        print(
            "{} out of {} files are updated cc is {}".format(
                (len(vocabulary_dict.keys()) - cc), len(vocabulary_dict.keys()), cc
            )
        )
        print("****************")
    with open(DATABASE_PATH, "w") as f:
        f.write(json.dumps(vocabulary_dict, indent=4))


def update_corpos(corpus_path):
    with open(DATABASE_PATH, "r") as f:
        vocabulary_dict = json.load(f)
    vocabulary_dict_keys = list(vocabulary_dict.keys())
    corpus = vocabulary_dict_keys[:]
    for key in vocabulary_dict_keys:
        corpus.extend(vocabulary_dict[key]["vocabulary"])
    corpus = sorted(set(corpus))
    c = len(corpus)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("***********************************")
    print()
    print("Corpus now increases to {}".format(len(corpus)))
    print()
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("***********************************")
    time.sleep(5)
    for word in corpus:
        word = word.strip()
        word = word.lower()
        c -= 1
        if word in vocabulary_dict:
            continue
        word_meaning_dictionary = api_request(word)
        if "hindi_translated_word" not in word_meaning_dictionary.keys():
            try:
                hindi_translated_word = translator.translate(word, lang_tgt="hi")
            except:
                hindi_translated_word = ""
            word_meaning_dictionary["hindi_translated_word"] = hindi_translated_word
        if "vocabulary" not in word_meaning_dictionary.keys():
            word_url = "http://wordnetweb.princeton.edu/perl/webwn?s={}".format(word)
            wordnet_api = requests.get(word_url)
            vocabulary = []
            wordnet_soup = BeautifulSoup(wordnet_api.text, features="lxml")
            for a_div in wordnet_soup.findAll("a"):
                if "href" in a_div.attrs and a_div.attrs["href"].startswith("webwn?"):
                    text = a_div.text
                    if text != "S:":
                        vocabulary.append(text)
            word_meaning_dictionary["vocabulary"] = vocabulary
        vocabulary_dict[word] = word_meaning_dictionary
        if (
            word_meaning_dictionary["description"]
            == "We're sorry, your request has been denied."
        ):
            with open(corpus_path, "w") as f:
                f.write(json.dumps(vocabulary_dict, indent=4))
            return
        if c % 20 == 0:
            print("*" * 100)
            print("*" * 100)
            print("'{}' word is processing".format(word))
            print("{} word are remaining".format(c))
            print("Next checkpoint after {} words".format(20 - c % 20))
            print("*" * 100)
            print("*" * 100)
            with open(corpus_path, "w") as f:
                f.write(json.dumps(vocabulary_dict, indent=4))
                print()
                print()
                print("#" * 100)
                print("#" * 100)
                print("*" * 100)
                print("*" * 100)
                print(
                    "{} words are saved successfully\n{} word list are remaining...".format(
                        len(corpus) - c, c
                    )
                )
                print("*" * 100)
                print("*" * 100)
                print("#" * 100)
                print("#" * 100)
                print()
                print()


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
    run()
    corpus_path = (BASE_PATH / "corpus.json").absolute().as_posix()
    update_corpos(corpus_path)
    driver.close()
