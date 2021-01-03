import json

class baseDB:
    def __init__(self):
        self.regionInfo = {"서울특별시":1102, "부산광역시":1151, "대구광역시":1153, "인천광역시":1132, "광주광역시":1162,
        "대전광역시":1142, "울산광역시":1152, "세종특별자치시":1144, "경기도":1131, "강원도":1133, "충청북도":1143,
        "충청남도":1141, "전라북도":1163, "전라남도":1161, "경상북도":1154, "경상남도":1155, "제주특별자치도":1164}

        self.nickName_to_realName = {"서울":"서울특별시", "부산":"부산광역시", "대구":"대구광역시", "인천":"인천광역시", "광주":"광주광역시",
        "대전":"대전광역시", "울산":"울산광역시", "세종":"세종특별자치시", "경기":"경기도", "강원":"강원도", "충북":"충청북도",
        "충남":"충청남도", "전북":"전라북도", "전남":"전라남도", "경북":"경상북도", "경남":"경상남도", "제주":"제주특별자치도"}

        self.hash_item = ['region', 'subRegion', 'name', 'gender']
        self.gender = {'남여공학':0, '남자':1, '여자':2}

    def save_json(self, file_name, json_data):
        with open(file_name+'.json', "w", encoding = 'utf8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    def read_json(self, file_name):
        json_data = {}
        with open(file_name, encoding = 'utf8') as json_file:
            json_data = json.load(json_file)
        return json_data
