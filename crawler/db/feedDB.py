# -*- coding: utf-8 -*-
import os, sys, json, time
import hashlib
from tqdm import tqdm

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grand_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, grand_parent_dir)

from main.model import *
from baseDB import baseDB

class FeedDB(baseDB):
    def __init__(self):
        super().__init__()

    def change_to_digit(self, like):
        if '.' in like:
            mul = 0
            if '천' in like:
                mul = 1000
            elif '만' in like:
                mul = 10000
            elif '백' in like:
                mul = 100
            like = float(like.strip('천만백')) * mul
        else:
            like = int(like.replace(',', ''))
        return like

    def register_feed(self):
        json_data = self.read_json('crawler/data/total_posts.json')
        for feed in tqdm(json_data.values()):
            like, reply = (feed['like_reply'][0], feed['like_reply'][1]) if len(feed['like_reply']) == 2 else (feed['like_reply'][0], 0)
            if isinstance(like, str):
                like = self.change_to_digit(like)
            if isinstance(reply, str):
                reply = self.change_to_digit(reply)
            if len(feed['origin_caption']) > 100:
                feed['origin_caption'] = feed['origin_caption'][:100]
            row = FeedInfo(mediaURL=feed['img_url'],
            caption=feed['origin_caption'],hashtag=" ".join(feed['hashtags']),
            like=like,reply=reply)
            db.session.add(row)
            db.session.commit()
    def register_restaurant_feed(self):
        gu_list = ['중구', '중랑구']
        food_category = ['닭_오리요리', '별식_퓨전요리', '분식', '양식', '일식_수산물', '제과제빵떡케익', '중식', '패스트푸드', '한식']
        for gu in gu_list:
            for food in food_category:
                json_data = self.read_json(f'crawler/data/restaurant_feed/{gu}_{food}_posts.json')
                json_data = [feed for feeds in json_data for feed in feeds]
                for feed in tqdm(json_data):
                    like, reply = (feed['like_reply'][0], feed['like_reply'][1]) if len(feed['like_reply']) == 2 else (feed['like_reply'][0], 0)
                    if isinstance(like, str):
                        like = self.change_to_digit(like)
                    if isinstance(reply, str):
                        reply = self.change_to_digit(reply)
                    if len(feed['origin_caption']) > 100:
                        feed['origin_caption'] = feed['origin_caption'][:100]
                    row = FeedInfo(mediaURL=feed['img_url'],
                    restaurantName=feed['restaurant'],
                    caption=feed['origin_caption'],hashtag=" ".join(feed['hashtags']),
                    like=like,reply=reply)

                    for r in RestaurantInfo.query.filter_by(restaurantName=feed['restaurant']).all():
                        r.mediaURL = feed['img_url']

                    db.session.add(row)
                    db.session.commit()

    def run(self):
        db.session.query(FeedInfo).delete()
        self.register_feed()
        self.register_restaurant_feed()
