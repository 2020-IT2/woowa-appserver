import os, sys, json, time, datetime
import hashlib
from tqdm import tqdm

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grand_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, grand_parent_dir)

from main.model import *
from baseDB import baseDB
from contestCrawler import contestCrawler

class contestDB(baseDB):
    def __init__(self):
        super().__init__()
        now = time.localtime()
        time_format = "%04d/%02d/%02d"
        self.version = time_format % (now.tm_year, now.tm_mon, now.tm_mday)
        self.month = now.tm_mon
        self.year = now.tm_year
        self.day = now.tm_mday

    def get_api(self):
        api = contestCrawler()
        return api.get_json()

    def register_contest(self):
        contest_infos = self.get_api()
        try:
            num_rows_deleted = db.session.query(ContestInfo).delete()
            db.session.commit()
        except:
            db.session.rollback()
        for contest in tqdm(contest_infos):
            new_contest = ContestInfo(title=contest['title'],imageUrl=contest['imageUrl'],content=contest['content'],area=contest['area'],sponsor=contest['sponsor'],
            start=contest['start'], end=contest['end'], prize=contest['prize'],firstPrize=contest['firstPrize'],homePage=contest['homePage'],storedDate=self.version)
            db.session.add(new_contest)
            db.session.commit()


    def run(self):
        self.register_contest()
        # self.test_cafeinfo()
