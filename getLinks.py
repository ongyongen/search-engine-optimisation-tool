import requests

import pandas as pd

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

class getLinks:
    def __init__(self, url, filter_criteria, **args):
        self.url = url
        self.filter_criteria = filter_criteria
        self.bfe_webpage_url_links_at_homepage = []
        self.all_url_links = []
        self.all_bfe_webpage_url_links = []
        self.all_external_webpage_url_links = {}
        self.df_all_bfe_webpage_url_links = None
        self.df_all_external_webpage_url_links = None
        
    def get_main_url(self):
        return self.url

    def get_bfe_webpage_url_links_at_homepage(self):
        return self.bfe_webpage_url_links_at_homepage
    
    def get_all_url_links(self):
        return self.all_url_links
    
    def get_all_unique_bfe_webpage_url_links(self):
        return self.all_bfe_webpage_url_links
    
    def get_all_unique_external_webpage_url_links(self):
        all_external_webpage_url_links = list(self.all_external_webpage_url_links.values())
        return list(set([url_link for url_link_lst in all_external_webpage_url_links for url_link in url_link_lst]))
    
    def get_df_all_bfe_webpage_url_links(self):
        return self.df_all_bfe_webpage_url_links
    
    def get_df_all_external_webpage_url_links(self):
        return self.df_all_external_webpage_url_links
    
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
            valid_url_links = self.extract_and_filter_valid_url_links(page_link) 
            self.all_url_links += list(filter(lambda x: x not in self.all_url_links, valid_url_links + [page_link]))
            if page_link not in self.all_external_webpage_url_links:
                self.all_external_webpage_url_links[page_link] = valid_url_links
            else:
                self.all_external_webpage_url_links[page_link] += list(filter(lambda x: x not in self.all_external_webpage_url_links[page_link], valid_url_links))
        
        self.all_bfe_webpage_url_links = self.filter_bfe_webpage_url_links(self.all_url_links,filter_criteria)    
        
        d_all_external_webpage_url_links_keys = list(self.all_external_webpage_url_links.keys())
        d_all_external_webpage_url_links_values = list(map(lambda x: self.filter_external_webpage_url_links(x,filter_criteria), list(self.all_external_webpage_url_links.values())))    
        self.all_external_webpage_url_links = {k:v for k,v in zip(d_all_external_webpage_url_links_keys,d_all_external_webpage_url_links_values)}
    
    def prepare_df_for_all_bfe_webpage_url_links(self):
        df_webpage = pd.DataFrame(columns=['bfe_webpage_url_links'])
        df_webpage['bfe_webpage_url_links'] = self.all_bfe_webpage_url_links
        self.df_all_bfe_webpage_url_links = df_webpage
        
    def prepare_df_for_all_external_webpage_url_links(self):
        df_ext = pd.DataFrame(columns=['parent_webpage','external_url_link'])
        d = check.all_external_webpage_url_links
        d_parent_external_lst = list(map(lambda x,y: [[x] * len(y), y], list(d.keys()), list(d.values())))
        parent = [parent for parent_lst in list(map(lambda x: x[0], d_parent_external_lst)) for parent in parent_lst]
        ext = [ext for ext_lst in list(map(lambda x: x[1], d_parent_external_lst)) for ext in ext_lst]
        df_ext['parent_webpage'] = parent
        df_ext['external_url_link'] = ext
        self.df_all_external_webpage_url_links = df_ext
        
            
url = "https://www.bridgesforenterprise.com/"
filter_criteria = "www.bridgesforenterprise.com"

check = getLinks(url,filter_criteria)
check.extract_bfe_webpage_url_links_from_homepage()
check.extract_all_url_links()

check.prepare_df_for_all_bfe_webpage_url_links()
check.prepare_df_for_all_external_webpage_url_links()

bfe = check.get_df_all_bfe_webpage_url_links()
ext = check.get_df_all_external_webpage_url_links()
