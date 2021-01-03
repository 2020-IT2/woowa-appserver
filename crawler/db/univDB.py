import os, sys, json, time
import hashlib
from tqdm import tqdm

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grand_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, grand_parent_dir)

from main.model import *
from baseDB import baseDB
from univ_info import convert_to_json

class univDB(baseDB):
    def __init__(self):
        super().__init__()
        self.eduPage = {"아주대학교" : "http://www.iajou.ac.kr/ipsi/board/notice/list.do",
            "수원대학교" : "https://ipsi.suwon.ac.kr/index.html?menuno=2084",
            "경희대학교" : "https://iphak.khu.ac.kr/cop/bbs/selectBoardList.do",
            "성균관대학교" : "https://admission.skku.edu/connect/dataroom.htm?ctg_cd=susi",
            "경기대학교" : "http://enter.kyonggi.ac.kr/cms/FR_CON/index.do?MENU_ID=210",
            "수원여자대학교" : "https://entr.swwu.ac.kr/cop/bbs/BBSMSTR_000000000051/selectBoardList.do?mn=ko"
        }

    def register_UnivInfo(self):
        univ_info = convert_to_json('crawler/data/대학교 목록.xlsx')
        for univ in tqdm(univ_info):
            unit = UnivInfo(univName=univ['name'], subRegion=univ['sub_region'], homePage=univ['homePage'])
            eduPage = self.eduPage.pop(univ['name'], "")
            unit.eduHomePage = eduPage
            unit.logoPossible = 1 if eduPage != '' else 0
            db.session.add(unit)
        db.session.commit()

    def run(self):
        self.register_UnivInfo()
