import json, time
import pandas as pd

from flask import escape, Blueprint, request, session, current_app as app
from sqlalchemy import text
from sqlalchemy import text, desc

from main.extensions import *
from main.model import *

search_api = Blueprint('search', __name__, url_prefix='/search')

@search_api.route('/restaurantList', methods=['GET'])
def get_schoolList():
    # this is server-side query.
    # trim 고,등,학,교 off
    search_text = escape(request.args.get('restaurant'))
    if not search_text or search_text == "":
        return response_with_code("<fail>:2:invalid search text")
    restaurantList = RestaurantInfo.query.filter(RestaurantInfo.restaurantName.like('%'+search_text+'%')).order_by(desc(RestaurantInfo.feedNum))
    df = pd.read_sql(restaurantList.statement, restaurantList.session.bind)
    return response_with_code("<success>", json.loads(df.to_json(orient='records', force_ascii=False)))

@search_api.route('/hashTag', methods=['GET'])
def get_hashTag():
    search_text = escape(request.args.get('hashtag'))
    if not search_text or search_text == "":
        return response_with_code("<fail>:2:invalid search text")
    sim_hashtag = []
    try:
        sim_hashtag = [{"hashtag":hashtag, "sim":str(round(sim, 2))} for hashtag, sim in word2vec.wv.most_similar(search_text, topn=20)]
        sim_hashtag.insert(0, {"hashtag":search_text, "sim":"1.0"})
    except:
        return response_with_code("<fail>:2:invalid search text")
    return response_with_code("<success>", sim_hashtag)
