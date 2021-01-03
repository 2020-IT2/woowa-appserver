import json, time
from datetime import datetime
from flask import jsonify, make_response, escape, Blueprint, request, session, current_app as app
from sqlalchemy import text, desc
from main.extensions import *
from main.model import *

recommend_api = Blueprint('recommend', __name__, url_prefix='/recommend')

@recommend_api.route('/recommend_random_food', methods=['GET'])
def get_random_food():
    idx = get_random_numeric_value(1)
    categories = ['한식', '중식', '분식', '양식', '일식', '패스트푸드', '치킨', '쌀국수', '빵', '순대']
    type = categories[idx]
    feed_info = FeedInfo.query.filter(FeedInfo.hashtag.like('%'+type+'%')).limit(7)
    df = pd.read_sql(feed_info.statement, feed_info.session.bind)
    # print(df)
    df = df.to_dict(orient='records')
    for feed in df:
        feed['hashtag'] = " ".join(feed['hashtag'][:15].split(" ")[:-1])
        # print(feed['mediaURL'])
    # print(df)
    return response_with_code("<success>", {'type':type, 'feeds':df})

@recommend_api.route('/recommend_customized_food', methods=['GET'])
def get_customized_food():
    idx = get_random_numeric_value(1)
    categories = ['한식', '중식', '분식', '양식', '일식', '패스트푸드', '치킨', '쌀국수', '빵', '순대']
    type = categories[idx]
    feed_info = FeedInfo.query.filter(FeedInfo.hashtag.like('%'+type+'%')).limit(7)
    df = pd.read_sql(feed_info.statement, feed_info.session.bind)
    # print(df)
    df = df.to_dict(orient='records')
    for feed in df:
        feed['hashtag'] = " ".join(feed['hashtag'][:15].split(" ")[:-1])
        # print(feed['mediaURL'])
    # print(df)
    return response_with_code("<success>", {'type':type, 'feeds':df})
