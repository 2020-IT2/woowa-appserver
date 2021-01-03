 #-*- coding: utf-8 -*-
import requests
import json
import time
import re
import os
from tqdm import tqdm
from baseCrawler import crawler

class contestCrawler(crawler):
    def __init__(self):
        self.pattern = re.compile('\\<.*?\\>')
        self.category = {'분야':'area', '응모대상':'target', '주최/주관':'sponsor', '접수기간' : 'dates', '총 상금':'prize', '1등 상금':'firstPrize', '홈페이지':'homePage'}
        super().__init__('https://www.wevity.com/')

    def get_page_list(self, page, mode):
        request_url = '?c=find&s=1&mode='+mode+'&gub=2&cidx=30&gp='+page
        contest_div = self.get_soup(request_url).find('div', {'class':'ms-list'}).find_all('div', {'class':'tit'})
        contest_urls = []
        for div in contest_div:
            if div.a:
                contest_urls.append(div.a['href'])
        return contest_urls

    def get_list(self):
        url_list = []
        for pageNo in range(6):
            url_list.extend(self.get_page_list(str(pageNo+1), 'soon'))
        for pageNo in range(6):
            url_list.extend(self.get_page_list(str(pageNo+1), 'ing'))
        return url_list

    def get_json(self):
        list_contest = self.get_list()

        json_data = []
        for url in tqdm(list_contest):
            soup = self.get_soup(url)
            content_info = {key : "" for key in self.category.values()}
            content_info['title'] = soup.find('div', {'class':'tit-area'}).h6.text
            content_info['imageUrl'] = self.BASE_URL + soup.find('div', {'class':'thumb'}).img['src']
            content = soup.find('div', {'id':'viewContents'}).text.strip(u'\r\t\n').replace(u'\t\n', u'\n')
            raw_content = re.sub("\\<\\/?img.*?\\/?\\>", "", str(soup.find('div', {'id':'viewContents'})))
            # print(raw_content)
            # content = soup.find('div', {'id':'viewContents'}).text
            content_info['content'] = raw_content
            infos = soup.find('ul', {'class', 'cd-info-list'}).find_all('li')
            for info in infos:
                raw = [r.strip('\r\n ') for r in info.text.strip('\n').split('\t')]
                type = raw[0]
                content = list(filter(lambda x : len(x) > 0, raw[1:]))
                # why it is first index? duration has two things
                if content:
                    content = content[0]
                else:
                    content = ''
                # hompage does not split up automatically
                if '홈페이지' in type:
                    type = raw[0].split('\n')[0]
                    if len(raw[0].split('\n')) > 1:
                        content = raw[0].split('\n')[1]
                    else:
                        content = ''
                # only needed info
                if type in self.category:
                    category = self.category[type]
                    if category == 'dates':
                        start_date, end_date = content.split('~')
                        content_info['start'] = start_date.strip()
                        content_info['end'] = end_date.strip()
                    else:
                        content_info[category] = content.strip()
            # print(content_info)
            json_data.insert(0, content_info)
        return json_data

if __name__ == '__main__':
    api = contestCrawler()
    api.get_json()
