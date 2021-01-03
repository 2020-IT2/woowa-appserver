import requests
import json
from bs4 import BeautifulSoup

class crawler:
    def __init__(self, base_url):
        self.BASE_URL = base_url

    def post_url(self, url, data):
        try:
            response = requests.post(self.BASE_URL + url, data = data)
            return response.json()
        except Exception as e:
            print('post_url function exception occur', e)

    def get_url(self, url):
        try:
            response = requests.get(url)
            return response
        except Exception as e:
            print('get_url function exception occur', e)

    def get_soup(self, url):
        try:
            response = self.get_url(self.BASE_URL+url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except Exception as e:
            print('get_soup function exception occur', e)

    def save_json(self, file_name, json_data):
        with open("data/"+file_name+'.json', "w", encoding = 'utf8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    def read_json(self, file_name):
        json_data = {}
        with open(file_name, encoding = 'utf8') as json_file:
            json_data = json.load(json_file)
        return json_data
