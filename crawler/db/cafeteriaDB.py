import os, sys, json, time, datetime
import hashlib
from tqdm import tqdm

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grand_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, grand_parent_dir)

from main.model import *
from baseDB import baseDB

class cafeDB(baseDB):
    def __init__(self):
        super().__init__()
        now = time.localtime()
        time_format = "%04d/%02d/%02d"
        self.version = time_format % (now.tm_year, now.tm_mon, now.tm_mday)
        self.month = now.tm_mon
        self.year = now.tm_year
        self.day = now.tm_mday

    def get_registered_school(self):
        registered_school = db.session.query(SchoolInfo.schoolID).filter(SchoolInfo.studentNum>0).all()
        return [row[0] for row in registered_school]

    def register_cafeInfo(self):
        # Todo: fix processe_cafeteria.json -> cafeteria.json
        registered_flag = True
        total_info = self.read_json(parent_dir + '/data/'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'-'+'cafeteria_menu_per_school.json')
        cafe_info = total_info['curMonth']
        registered_school_ids = self.get_registered_school()
        # Set registered flag
        if len(registered_school_ids) < 5:
            registered_flag = False
        for region, schools in cafe_info.items():
            regionName = region[:-3]
            regionID = self.regionInfo[regionName]
            for schoolName, menus in tqdm(schools.items()):
                school_infos = SchoolInfo.query.filter_by(schoolName=schoolName, regionID=regionID).first()
                if not school_infos:
                    continue
                if registered_flag and school_infos.schoolID not in registered_school_ids:
                    continue
                # case 1 : there is no school info in info table
                # case 2 : already exists
                # Todo : find if case 3 exist
                # case 3 : if there is same named school in same region (1개 누락)
                # Process next Month
                nextMonthmenus = total_info['nextMonth'][region][schoolName] if len(total_info['nextMonth']) > 0 else []
                existing_row = CafeteriaInfo.query.filter_by(schoolID=school_infos.schoolID).first()
                if existing_row:
                    existing_row.curCafeMenu = json.dumps(menus)
                    existing_row.nextCafeMenu = json.dumps(nextMonthmenus)
                    existing_row.version = self.version
                    db.session.commit()
                else:
                    cafe = CafeteriaInfo(schoolID=school_infos.schoolID, regionID=regionID, version=self.version)
                    cafe.curCafeMenu=json.dumps(menus, indent=4, ensure_ascii=False)
                    cafe.nextCafeMenu=json.dumps(nextMonthmenus, indent=4, ensure_ascii=False)
                    db.session.add(cafe)
                    db.session.commit()
        db.session.commit()

    def test_cafeinfo(self):
        cafe = CafeteriaInfo.query.first()
        print(json.loads(cafe.cafeMenu, encoding="utf-8"))

    def run(self):
        self.register_cafeInfo()
        # self.test_cafeinfo()
