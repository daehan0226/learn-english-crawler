import time
import sys
import simplejson
import requests
from random import uniform

from retry import retry
from timeout_decorator import timeout, TimeoutError
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from libs.helper import get_verb_particle_from_keyword

from libs.logger import get_logger


json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)

# chrome과 함께 실행할 옵션 객체 생성
options = Options()

# chrome 브라우저 실행 환경 셋팅
prefs = {
    "profile.default_content_setting_values.notifications": 2,
    "profile.default_content_setting_values.popups": 2,
    "profile.default_content_settings.state.flash": 0,
    "profile.managed_default_content_settings.images": 2,
    "download.prompt_for_download": False,
}

options.add_experimental_option("prefs", prefs)
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")
options.add_argument("--ignore-certificate-errors-spki-list")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--disable-popup-blocking")
options.add_argument("--start-maximized")
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
)

CHROME_PATH = config["driver_path"]
if config["server"]:
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    CHROME_PATH = config["driver_path_server"]


class Crawler:
    driver = webdriver.Chrome(executable_path=CHROME_PATH, options=options)
    wait = WebDriverWait(driver, config["driver_wait_time"])
    sleep_time = config["sleep_time"]
    logging = get_logger(config)

    def close(self):
        if self.driver is not None:
            try:
                self.driver.quit()
            except:
                pass

    def set_parse_url(self):
        return None

    def set_keyword(self, keyword):
        self.keyword = keyword

    def remove_duplicates(self, data_list):
        return list(set(data_list)) if data_list else data_list

    def filter_if_not_include_keyword(self, sentences):
        result = []
        verb, particle = get_verb_particle_from_keyword(self.keyword)

        for sentence in sentences:
            if verb in sentence or particle in sentence:
                result.append(sentence)

        return self.remove_duplicates(result)

    def parse_by_selectors(self, target=None, css_selectors=None):
        result = []
        try:
            time.sleep(uniform(self.sleep_time, self.sleep_time + 1))
            for css_selector in css_selectors:
                result.extend(self.driver.find_elements(By.CSS_SELECTOR, css_selector))
        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(
                f"parse {target} except {str(tb.tb_lineno)}, {e.__str__()}"
            )
        return result
    
    
    def get_elements_by_selector(self, src, target=None, css_selector=None):
        result = []
        try:
            result = src.find_elements(By.CSS_SELECTOR, css_selector)
        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(
                f"parse {target} except {str(tb.tb_lineno)}, {e.__str__()}"
            )
        return result
    
    
    def get_an_element_by_selector(self, src, target=None, css_selector=None):
        result = None
        try:
            result = src.find_element(By.CSS_SELECTOR, css_selector)
        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.debug(
                f"parse {target} except {str(tb.tb_lineno)}, {e.__str__()}"
            )
        return result

    def get_text_contents_from_elemets(self, elements):
        result = []
        try:
            for ele in elements:
                result.append(ele.get_attribute("textContent").strip())

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(
                f"parse text contents except {str(tb.tb_lineno)}, {e.__str__()}"
            )
        return result
    
    
    def get_text_content_from_elemet(self, element):
        result = ""
        try:
            result = element.get_attribute("textContent").strip()

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(
                f"parse text content except {str(tb.tb_lineno)}, {e.__str__()}"
            )
        return result

    def get_text_contents_from_src_except(self, src, exclude):
        result = []
        try:
            text_elements = src.find_elements(By.XPATH, "./*")
            for text_ele in text_elements:
                if text_ele.get_attribute("class") != exclude:
                    result.extend(text_ele.get_attribute("textContent").strip())

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(
                f"parse text contents except {str(tb.tb_lineno)}, {e.__str__()}"
            )
        return result

    def log_parsing_result(self, definition_count, example_count):
        self.logging.info(
            f"parsed definition {str(definition_count)}, example {str(example_count)}"
        )

    def trim_spaces(self, sentences):
        result = []
        for sentence in sentences:
            if sentence.startswith(": "):
                sentence = sentence[2:]
            sentence = sentence.strip()
            result.append(sentence)
        return result

    def return_if_has_css_selector_classname(self, src, class_name):
        result = False
        try:
            result = src.find_elements(By.CSS_SELECTOR, class_name)
            print(result)
            return result
        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(
                f"check if it has css selector class {class_name} except {str(tb.tb_lineno)}, {e.__str__()}"
            )
        return result