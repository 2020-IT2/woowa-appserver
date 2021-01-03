 #-*- coding: utf-8 -*-
import requests
import json
import time
import re
import os
from tqdm import tqdm
from baseCrawler import crawler

class cafeteriaCrawler(crawler):
    def __init__(self):
        self.pattern = re.compile('\\(.?\\){1}|(([0-9]*?)\\.)*')
        super().__init__('https://www.foodsafetykorea.go.kr/')

    def get_list(self):
        url = 'portal/sensuousmenu/selectSchoolMeals_school.do'
        data = {}
        school_list = self.parse_school_info(self.post_url(url, json.dumps(data))['list'])
        return school_list

    def parse_school_info(self, schools):
        region_school = {}
        for school in schools:
            if school['ara'] not in region_school:
                region_school[school['ara']] = []

            if '고등학교' in school['schl_nm']:
                region_school[school['ara']].append({'id':school['schl_cd'], 'name':school['schl_nm']})
        return region_school

    def parse_menu(self, menu_data):
        menus = []
        for raw_menu in menu_data['list']:
            if "dd_date" not in raw_menu:
                continue
            if "lunch" not in raw_menu:
                raw_menu['lunch'] = ''

            menus.append({
                'date' : raw_menu['dd_date'].strip(),
                'week' : raw_menu['week_dvs'].strip(),
                'week_day' : raw_menu['week_day'].strip(),
                'lunch' : self.parse_lunch(raw_menu['lunch']),
            })

        return menus

    def parse_lunch(self, lunch):
        return ",".join([self.pattern.sub('', x).strip('*') for x in lunch.split('\n')])

    def process_json(self):
        json_data = self.read_json('data/cafeteria_menu_per_school.json')
        for region, schools in json_data.items():
            for days in schools.values():
                for day in days:
                    day['lunch'] = self.parse_lunch(day['lunch'])
        self.save_json('processed_cafeteria_menu_per_school', json_data)

    def get_json(self):
        url = 'portal/sensuousmenu/selectSchoolMonthMealsDetail.do'
        school_list = self.get_list()

        now = time.localtime()
        curYear = now.tm_year
        curMonth = now.tm_mon
        curDay = now.tm_mday
        nextYear = curYear
        nextMonth = curMonth + 1

        if curMonth == 12:
            nextYear = curYear + 1
            nextMonth = 1

        cur_data = self.get_data_per_month(url, school_list, curYear, curMonth)
        next_data = self.get_data_per_month(url, school_list, nextYear, nextMonth) if curDay >= 15 else []
        final_data = {'curMonth':cur_data, 'nextMonth':next_data}
        self.save_json(str(now.tm_year)+'-'+str(now.tm_mon)+'-'+str(now.tm_mday)+'-'+'cafeteria_menu_per_school', final_data)
        self.save_json('school_list', school_list)

    def get_data_per_month(self, url, school_list, year, month):
        post_data = {
            'schl_cd' : "",
            'type_cd' : 'M',
            'year' : year,
            'month' : month,
        }
        cafe_menu_per_school = {}
        for region, schools in tqdm(school_list.items()):
            region_school = {}
            for school in tqdm(schools):
                time.sleep(0.01)
                post_data['schl_cd']=school['id']
                menus = self.parse_menu(self.post_url(url, post_data))
                region_school[school['name']] = menus

            cafe_menu_per_school[region] = region_school
        return cafe_menu_per_school



if __name__ == '__main__':
    api = cafeteriaCrawler()
    api.get_json()
