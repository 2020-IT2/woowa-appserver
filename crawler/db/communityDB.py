import os, sys, json, time, datetime
import hashlib
from tqdm import tqdm

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grand_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, grand_parent_dir)

from main.model import *
from baseDB import baseDB

class communityDB(baseDB):
    def __init__(self):
        super().__init__()
        # Todo : community ListUp
        self.all_communityList = ['학원/인강', '질문', '자유']
        self.region_communityList = ['질문', '모집', '자유']
        self.school_communityList = ['질문', '자유']

    def register_all_communityList(self):
        db.session.query(CommunityAll).delete()
        for id in range(len(self.all_communityList)):
            community_name = self.all_communityList[id]
            community = CommunityAll(communityID=id+1, communityName=community_name)
            db.session.add(community)
        db.session.commit()

    def register_univ_community(self):
        for univ in UnivInfo.query.all():
            id = univ.univID * 10
            if CommunityAll.query.filter_by(communityID=id).first():
                continue
            community = CommunityAll(communityID=id+1, communityName=univ.univName+"커뮤니티")
            db.session.add(community)
            community = CommunityAll(communityID=id, communityName=univ.univName+"뉴스")
            db.session.add(community)
        db.session.commit()

    def load_regionList(self):
        regionInfo = RegionInfo.query.all()
        if not regionInfo:
            return []
        regionInfo = [r.regionID for r in regionInfo]
        return regionInfo

    def register_region_communityList(self):
        region_id_list = self.load_regionList()

        for region_idx in tqdm(range(len(region_id_list))):
            region_id = region_id_list[region_idx]
            for com_idx in range(len(self.region_communityList)):
                community_name = self.region_communityList[com_idx]
                community_id = com_idx + region_idx * 100 + region_id * 100
                if CommunityRegion.query.filter_by(communityID=community_id).first():
                    continue

                community = CommunityRegion(
                communityID=community_id, regionID= region_id, communityName=community_name)
                db.session.add(community)
        db.session.commit()

    def load_schoolList(self):
        schoolInfo = SchoolInfo.query.all()
        if not schoolInfo:
            return []
        schoolInfo = [r.schoolID for r in schoolInfo]
        return schoolInfo

    def register_school_communityList(self):
        school_id_list = self.load_schoolList()

        for school_idx in tqdm(range(len(school_id_list))):
            school_id = school_id_list[school_idx]
            for com_idx in range(len(self.school_communityList)):
                community_name = self.school_communityList[com_idx]
                community_id = com_idx*100 + school_idx * 10000
                if CommunitySchool.query.filter_by(communityID=community_id).first():
                    continue

                community = CommunitySchool(
                communityID=community_id, schoolID= school_id, communityName=community_name)
                db.session.add(community)
        db.session.commit()

    def get_cur_date(self):
        time_format = "%04d/%02d/%02d %02d:%02d:%02d"
        now = time.localtime()
        written_time = time_format % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        return written_time

    def init_community(self):
        try:
            num_rows_deleted = db.session.query(ArticleAll).delete()
            num_rows_deleted = db.session.query(ArticleSchool).delete()
            num_rows_deleted = db.session.query(ArticleRegion).delete()
            db.session.commit()
        except:
            db.session.rollback()

        for community in CommunityAll.query.all():
            article = ArticleAll(communityID=community.communityID, userID=1479750676, nickName="삐약이",
            title="환영합니다", content="게시판에 오신것을 환영합니다. 첫글을 남겨 주세요.",
            viewNumber=0, reply=0, heart=5, writtenTime=self.get_cur_date())
            db.session.add(article)

        for community in CommunityRegion.query.all():
            article = ArticleRegion(communityID=community.communityID, regionID=community.regionID, userID=1479750676, nickName="삐약이",
            title="환영합니다", content="게시판에 오신것을 환영합니다. 첫글을 남겨 주세요.",
            viewNumber=0, reply=0, heart=5, writtenTime=self.get_cur_date())
            db.session.add(article)

        for community in CommunitySchool.query.all():
            article = ArticleSchool(communityID=community.communityID, schoolID=community.schoolID, userID=1479750676, nickName="삐약이",
            title="환영합니다", content="게시판에 오신것을 환영합니다. 첫글을 남겨 주세요.",
            viewNumber=0, reply=0, heart=5, writtenTime=self.get_cur_date())
            db.session.add(article)
        db.session.commit()


    def run(self):
        self.register_all_communityList()
        self.register_region_communityList()
        self.register_school_communityList()
        self.register_univ_community()
        self.init_community()
