import json, time
from pprint import pprint as pp
from datetime import datetime
import unicodedata
from flask import jsonify, make_response, escape, Blueprint, request, session, current_app as app
from sqlalchemy import text, desc
from main.extensions import *
from main.model import *

list_api = Blueprint('list', __name__, url_prefix='/list')

@list_api.route('/restaurantList', methods=['GET'])
def get_restaurant_list():
    types = request.args.get('type')
    gu = str(request.args.get('gu'))
    restaurant = {"franchise":[], "non_franchise":[]}
    franchise = RestaurantInfo.query.filter(RestaurantInfo.subRegion==gu, RestaurantInfo.type==types, RestaurantInfo.isFranchise==True, RestaurantInfo.mediaURL!=None).order_by(desc(RestaurantInfo.feedNum)).limit(30).all()
    non_franchise = RestaurantInfo.query.filter(RestaurantInfo.subRegion==gu, RestaurantInfo.type==types, RestaurantInfo.isFranchise==False, RestaurantInfo.mediaURL!=None).order_by(desc(RestaurantInfo.feedNum)).limit(30).all()
    for row in franchise:
        dict_row = convert_to_dict(row)
        restaurant['franchise'].append(dict_row)
    for row in non_franchise:
        dict_row = convert_to_dict(row)
        restaurant['non_franchise'].append(dict_row)
    print("프렌차이즈 개수 : ", len(restaurant['franchise']))
    print("비 프렌차이즈 개수 : ", len(restaurant['non_franchise']))
    print(restaurant['non_franchise'][0])
    return response_with_code("<success>", restaurant)

@list_api.route('/feedList', methods=['GET'])
def get_feed_list():
    types = int(request.args.get('type'))
    query = request.args.get('tag')
    result = []
    hashtag = ""
    re_result = []
    if types == 1:
        result = FeedInfo.query.filter(FeedInfo.restaurantName.like('%'+query+'%')).limit(5)
        result = pd.read_sql(result.statement, result.session.bind)
        result = result.to_dict(orient='records')
        re_result = FeedInfo.query.filter(FeedInfo.hashtag.like('%'+"양식"+'%')).limit(20)
        re_result = pd.read_sql(re_result.statement, re_result.session.bind)
        re_result = re_result.to_dict(orient='records')
    else:
        hashtag = query[:].strip("#")
        if not isHangul(hashtag):
            hashtag = unicodedata.normalize('NFC', hashtag)
        result = FeedInfo.query.filter(FeedInfo.hashtag.like('%'+query+'%')).limit(5)
        result = pd.read_sql(result.statement, result.session.bind)
        result = result.to_dict(orient='records')
        sim_hashtags = [hashtag for hashtag, sim in word2vec.wv.most_similar(hashtag, topn=20)]
        temp_result = []
        url_set = set()
        for sim_hashtag in sim_hashtags:
            temp_result = FeedInfo.query.filter(FeedInfo.hashtag.like('%'+sim_hashtag+'%')).limit(1)
            temp_result = pd.read_sql(temp_result.statement, temp_result.session.bind)
            temp_result = temp_result.to_dict(orient='records')
            temp_result = list(filter(lambda x : x['mediaURL'] not in url_set, temp_result))
            url_set.update(set([feed['mediaURL'] for feed in temp_result]))
            re_result.extend(temp_result)
    # print(result)
    # print(restaurant)
    return response_with_code("<success>", {"feeds":result,"relatedFeeds":re_result})

@list_api.route('/RelatedfeedList', methods=['GET'])
def get_related_feed_list():
    types = int(request.args.get('type'))
    query = request.args.get('tag')
    result = []
    if types == 1:
        query = query.split(' ')[0][1:]
        hashtag, sim = word2vec.wv.most_similar(query, topn=1)
        result = FeedInfo.query.filter(FeedInfo.hashtag.like('%'+hashtag+'%')).limit(20)
        result = pd.read_sql(result.statement, result.session.bind)
        result = result.to_dict(orient='records')
    else:
        query = query.split(' ')[0][1:]
        hashtag, sim = word2vec.wv.most_similar(query, topn=1)
        result = FeedInfo.query.filter(FeedInfo.hashtag.like('%'+hashtag+'%')).limit(20)
        result = pd.read_sql(result.statement, result.session.bind)
        result = result.to_dict(orient='records')
    # print(result)
    # print(restaurant)
    return response_with_code("<success>", result)


def isHangul(text):
    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text))
    return hanCount > 0
