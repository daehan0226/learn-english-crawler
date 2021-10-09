
import time
from libs.Crawler import Crawler
from libs.helper import get_keywords, get_sites, upload_parsed_data

from crawlers.CrawlerCambridge import CrawlerCambridge
from crawlers.CrawlerMerriam import CrawlerMerriam
from crawlers.CrawlerOxford import CrawlerOxford
from crawlers.CrawlerMacmillan import crawlerMacmillan

def run_crawler(keyword):
    crawler = Crawler()
    logging = crawler.logging
    keywords = [keyword] if keyword else get_keywords()
    dictionary_sites = get_sites()
    for keyword in keywords:
        sites = []
        definitions = []
        examples = []
        for site, site_data in dictionary_sites.items():
            try:
                if site == "cambridge":
                    continue
                    cralwer = CrawlerCambridge()

                elif site == "merriam":
                    continue
                    cralwer = CrawlerMerriam()

                elif site == "oxford":
                    continue
                    cralwer = CrawlerOxford()
                
                elif site == "macmillan":
                    cralwer = crawlerMacmillan()

                logging.info(f"parsing for '{keyword}' started from {site}")
                start_time = time.time()
                cralwer.set_keyword(keyword)
                cralwer.set_parse_url(site_data)
                cralwer.parse()
                end_time = time.time()
                logging.debug(
                    f"site : {site} parsing finished, parsing time : {end_time - start_time}"
                )
                sites.append(site)
                definitions.extend(cralwer.definitions)
                examples.extend(cralwer.examples)
            except:
                pass
        print(keyword, sites, definitions, examples)
        # upload_parsed_data(keyword, sites, definitions, examples)
    cralwer.close()

if __name__ == "__main__":
    keyword = "give up"
    run_crawler(keyword)