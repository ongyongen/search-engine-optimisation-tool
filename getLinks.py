import re
import requests

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

class getLinks:
    def __init__(self, url, filter_criteria, **args):
        self.url = url
        self.filter_criteria = filter_criteria
        self.bfe_webpage_url_links_at_homepage = []
        self.all_url_links = []
        self.all_bfe_webpage_url_links = []
        self.all_external_webpage_url_links = []
        
    def get_main_url(self):
        return self.url

    def get_bfe_webpage_url_links_at_homepage(self):
        return self.bfe_webpage_url_links_at_homepage
    
    def get_all_url_links(self):
        return self.all_url_links
    
    def get_all_bfe_webpage_url_links(self):
        return self.all_bfe_wepage_url_links
    
    def get_all_external_webpage_url_links(self):
        return self.all_external_webpage_url_links
    
    def extract_and_filter_valid_url_links(self, url):
        req = Request(url)
        page = urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        all_url_links = []
        for url_link in soup.findAll('a'):
            all_url_links.append(url_link.get('href'))
        valid_url_links = list(set(filter(lambda x: 'http' in x or 'www.' in x if x != None else None, all_url_links)))
        return valid_url_links
    
    def filter_bfe_webpage_url_links(self, url_links, filter_criteria):
        return list(filter(lambda x: filter_criteria in x, url_links))
    
    def filter_external_webpage_url_links(self, url_links, filter_criteria):
        return list(filter(lambda x: filter_criteria not in x, url_links))
        
    def extract_bfe_webpage_url_links_from_homepage(self):
        valid_url_links = self.extract_and_filter_valid_url_links(self.url)
        self.bfe_webpage_url_links_at_homepage = self.filter_bfe_webpage_url_links(valid_url_links,filter_criteria)
        
    def extract_all_url_links(self):
        for page_link in self.bfe_webpage_url_links_at_homepage:
            valid_url_links = self.extract_and_filter_valid_url_links(page_link) + [page_link]
            self.all_url_links += list(filter(lambda x: x not in self.all_url_links, valid_url_links))
            
    def extract_all_bfe_and_external_webpage_links(self):
        self.all_bfe_wepage_url_links = self.filter_bfe_webpage_url_links(self.all_url_links,filter_criteria)
        self.all_external_webpage_url_links = self.filter_external_webpage_url_links(self.all_url_links,filter_criteria)
            
        
url = "https://www.bridgesforenterprise.com/"
filter_criteria = "www.bridgesforenterprise.com"

check = getLinks(url,filter_criteria)
check.extract_bfe_webpage_url_links_from_homepage()
check.extract_all_url_links()
check.extract_all_bfe_and_external_webpage_links()
