from bs4 import BeautifulSoup
import requests
import re

class Page:
    def __init__(self, url):
        self.url = url
        self.html = requests.get(url).content
        self.soup = BeautifulSoup(self.html, 'html.parser')

    @staticmethod
    def format_sentence(string):
        string = re.sub('\s(?=[,\.\)])', '', string)
        return re.sub('(?<=\()\s', '', string)
