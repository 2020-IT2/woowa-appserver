import openpyxl
import json
from tqdm import tqdm

def convert_to_json(path):
    # 엑셀파일 열기
    wb = openpyxl.load_workbook(path)

    # 현재 Active Sheet 얻기
    ws = wb.active

    # 국영수 점수를 읽기
    high_school_data = []
    for r in tqdm(ws.rows):
        if r[0].row  < 6 or r[1].value not in ['대학교', '각종대학(대학)', '교육대학', '전공대학', '전문대학(4년제)']:
            continue

        high_school_data.append({
            "school_type":r[1].value,
            "region":r[2].value,
            "sub_region":r[3].value,
            "name":r[4].value,
            "eng_name":r[5].value,
            "foundation":r[8].value,
            "homePage":r[13].value
        })
    return high_school_data
#
# if __name__ == '__main__':
#     //analyze()
