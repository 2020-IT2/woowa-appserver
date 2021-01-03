import os, sys, json, time, random
import hashlib
from tqdm import tqdm
import traceback

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grand_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, grand_parent_dir)

from main.model import *
from baseDB import baseDB

class RestaurantDB(baseDB):
    def __init__(self):
        super().__init__()

    def register_restaurant(self):
        json_data = self.read_json('crawler/data/result.json')
        keys = ['non_franchise', 'franchise']

        bool_vals = [False, True]
        for gu_restaurants in tqdm(json_data.values()):
            for type_restaurant in gu_restaurants.values():
                for idx in range(2):
                    for restaurants in type_restaurant[keys[idx]]['top_rank']:
                        if 'restaurants' not in restaurants:
                            continue
                        restaurant = restaurants['restaurants'][0]
                        try:
                            if idx == 0:
                                row = RestaurantInfo(
                                restaurantName=restaurant['restaurantName'],
                                isFranchise=bool_vals[idx],
                                feedNum=restaurants['val'],
                                likeNum=restaurants['val']/2 + random.randint(0,100),
                                type=restaurant['type'],
                                subRegion=restaurant['subRegion'],
                                adrDong=restaurant['adrDong'],
                                adrStreet=restaurant[""],
                                lat=restaurant['lat'],
                                lon=restaurant['lon'])
                                db.session.add(row)
                                db.session.commit()
                            else:
                                row = RestaurantInfo(
                                restaurantName=restaurant['상호명'],
                                isFranchise=True,
                                feedNum=restaurants['val'],
                                likeNum=restaurants['val']/2 + random.randint(0,100),
                                type=restaurant['상권업종중분류명'],
                                subRegion=restaurant['시군구명'],
                                adrDong=restaurant['지번주소'],
                                adrStreet=restaurant["도로명주소"],
                                lat=restaurant['경도'],
                                lon=restaurant['위도'])
                                db.session.add(row)
                                db.session.commit()
                        except:
                            print(restaurant)
                            traceback.print_exc()
                            return

    def register_non_franchise(self):
        json_data = self.read_json('crawler/data/non_frenchise_data.json')
        for gu_restaurants in tqdm(json_data.values()):
            for restaurants in gu_restaurants.values():
                for restaurant in restaurants.values():
                    row = RestaurantInfo(
                    restaurantName=restaurant['restaurantName'],
                    isFranchise=False,
                    type=restaurant['type'],
                    subRegion=restaurant['subRegion'],
                    adrDong=restaurant['adrDong'],
                    adrStreet=restaurant[""],
                    lat=restaurant['lat'],
                    lon=restaurant['lon'])
                    db.session.add(row)
                    db.session.commit()

    def register_franchise(self):
        json_data = self.read_json('crawler/data/frenchise_data.json')
        for franchises in tqdm(json_data.values()):
            gus = list(franchises.keys())
            if 'total_num' in gus:
                gus.remove('total_num')
            if 'type' in gus:
                gus.remove('type')
            if 'name' in gus:
                gus.remove('name')
            for gu in gus:
                for restaurant in franchises[gu]['restaurants']:
                    # print(restaurant)
                    row = RestaurantInfo(
                    restaurantName=restaurant['상호명'],
                    isFranchise=True,
                    type=restaurant['상권업종중분류명'],
                    subRegion=restaurant['시군구명'],
                    adrDong=restaurant['지번주소'],
                    adrStreet=restaurant["도로명주소"],
                    lat=restaurant['경도'],
                    lon=restaurant['위도'])
                    db.session.add(row)
                    db.session.commit()

    def run(self):
        db.session.query(RestaurantInfo).delete()
        self.register_restaurant()
        # self.register_non_franchise()
        # self.register_franchise()
