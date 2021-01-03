from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session
from functools import *

from flask_security import Security,  \
    UserMixin, RoleMixin, login_required, current_user
from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from flask import Flask, session, url_for, redirect, request
from flask_mail import Mail
from uuid import uuid4
from datetime import datetime, timedelta
import _pickle
import time
import string
import json
import random
import requests

import io
from base64 import encodebytes
from PIL import Image
# from flask import jsonify

security = Security()
flask_bcrypt = Bcrypt()
login_manager = LoginManager()
sess = Session()
mail = Mail()


current_milli_time = lambda: int(round(time.time() * 1000)) % 100000

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

def response_with_code(status, body=None):
    return json.dumps({'status':status, 'body':body})

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def get_random_numeric_value(length):
    digits = string.digits
    result_str = ''.join((random.choice(digits) for i in range(length)))
    return int(result_str)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = session.get('user_id')
        if session_token is None:
            return response_with_code("<fail>:2:login required")
        return f(*args, **kwargs)
    return decorated_function

def user_have_write_right(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = session.get('authorized')
        print(session_token)
        if session_token is None:
            return response_with_code("<fail>:4:인증 해주세요")
        if session_token == 0:
            return response_with_code("<fail>:4:인증 해주세요")
        return f(*args, **kwargs)
    return decorated_function

def is_highSchool(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = session.get('age')
        if session_token is None:
            return response_with_code("<fail>:2:고등학생이 아닙니다.")
        if session_token > 19:
            return response_with_code("<fail>:2:고등학생이 아닙니다.")
        return f(*args, **kwargs)
    return decorated_function

def get_cur_date():
    time_format = "%04d/%02d/%02d %02d:%02d:%02d"
    now = time.localtime()
    written_time = time_format % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return written_time

def allowed_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        json_data = request.json
        id = int(json_data['communityID']) if json_data else int(request.args.get('communityID'))
        ids = session.get('allowed_ids')
        communityType = request.args.get('communityType')
        if not communityType:
            communityType = json_data['communityType']
        else:
            communityType = int(communityType)

        if communityType == 0:
            return f(*args, **kwargs)
        if id not in ids:
            return response_with_code("<fail>:2:access denied")
        return f(*args, **kwargs)
    return decorated_function

def convert_to_dict(query_result):
    dict_result = dict(query_result.__dict__)
    dict_result.pop('_sa_instance_state', None)
    written_time = dict_result.pop('writtenTime', None)
    if written_time:
        dict_result['writtenTime'] = str(written_time)
    return dict_result

def send_push_alarm(to, title, body):
    headers = {
        'Content-Type' : 'application/json',
        'Authorization': 'key=AAAAfktu114:APA91bFKJ0O4YF28d_IgbGJRmf6iyjSMdYEheVu_zLfvlNKi-vHBSeKuSlqEP-8JnWGG1e0s17-Ask5wKoFMOZLA11jXaS8hJLuGPA-pSQt5d_ylmHJfv8YlKzQ8dsjq7kOAIpv2bpCz'
    }
    body = {
        'to':to,
        'priority':'high',
        'data':{
            'title':title,
            'message':body
        },
        'notification':{
            'title':title,
            'body':body
        }
    }
    r= requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=json.dumps(body))
    print(r)


import json
import pandas as pd
import re

def saveGensim():
    from gensim.models.word2vec import Word2Vec
    from pathlib import Path
    def read_json(file_name):
        json_data = {}
        with open(file_name, encoding = 'utf8') as json_file:
            json_data = json.load(json_file)
        return json_data
    # users_comment_only = read_json("drive/Shareddrives/집교2/머신러닝/new_users_for_crawling.json")
    users = read_json("main/ML/data/total_users.json")
    posts = read_json("main/ML/data/total_posts.json")
    list(posts.values())
    hashtags = []
    all_hashtags=[]
    for user in posts.values():
      text = user['hashtags']
      h=[]
      for hashtag in text:
        hashtag = hashtag[1:]
        h.append(hashtag)
      if h == []:
        continue
      hashtags.append(h)
      all_hashtags.extend(h)
    # all_hashtags
    model = Word2Vec(hashtags, sg=1, window=5, min_count=3, iter=100)
    model.init_sims(replace=True)
    model.save('main/ML/model/hashtag.model')

def loadGensim():
    from gensim.models.word2vec import Word2Vec
    from pathlib import Path
    model = Path("main/ML/model/hashtag.model")
    if not model.is_file():
        saveGensim()
    return Word2Vec.load(str(model))

word2vec = loadGensim()
