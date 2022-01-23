from pandas.io import html
import requests
import os, re
import json
import pandas as pd
from spider import getAllDataAndSaveToFile


car_brands = ["tesila", "weila", "lixiang", "xiaopeng"]
car_brands_chn = ["特斯拉", "蔚来", "理想", "小鹏"]
cities = [12, 16, 45, 13, 17, 15, 204, 194, 93]
cities_chn = ["beijing", "guangzhou", "chengdu", "shanghai", "shenzhen", "chongqing", "changsha", "wuhan", "haerbin"]
url = 'https://mapi.guazi.com/car-source/carList/pcList?minor={car_brand}&sourceType=&ec_buy_car_list_ab=&location_city=&district_id=&tag=-1&license_date=&auto_type=&driving_type=&gearbox=&road_haul=&air_displacement=&emission=&car_color=&guobie=&bright_spot_config=&seat=&fuel_type=&order=&priceRange=0,-1&tag_types=&diff_city=&intention_options=&initialPriceRange=&monthlyPriceRange=&transfer_num=&car_year=&carid_qigangshu=&carid_jinqixingshi=&cheliangjibie=&key_word={car_brand_chn}&page={pg}&pageSize=100&city_filter={ct}&city={ct}&guazi_city={ct}&qpres=484192054210134016&versionId=0.0.0.0&osv=IOS&platfromSource=wap'

head = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
 

def deal_page(url, car_brand, car_brand_chn, ct, ct_chn, head):
    '''
    对筛选数据页的初步处理，获取
    '''
    url1 = url.format(car_brand = str(car_brands[0]), car_brand_chn = str(car_brands_chn[0]), pg = 1, ct = 12)
    # print(url1)
    page = requests.get(url1,headers=head,timeout=3)
    # f = open("./crawl_for_guazi/test.json", 'w')
    # f.write(page.text)
    page_text_dict = json.loads(page.text)
    page, total_page = page_text_dict["data"]["page"], page_text_dict["data"]["totalPage"]
    while page <= total_page:
        get_single_page_info(url, car_brand, car_brand_chn, page, ct, ct_chn, head)
        page += 1
    print(f'{car_brand_chn} in {ct_chn} finish!', end='\n')


def get_single_page_info(url, car_brand, car_brand_chn, pg, ct, ct_chn, head):
    '''
    获取每一页的车辆数据信息（每一页大概是20辆车）
    '''
    url = url.format(car_brand = str(car_brand), car_brand_chn = str(car_brand_chn), pg = pg, ct = ct)
    page = requests.get(url,headers=head,timeout=3)
    page_text = json.loads(page.text)
    df = pd.DataFrame()
    for single_car in page_text["data"]["postList"]:
        # print(single_car["title"] + "clueid = " + str(single_car["clue_id"]), end="\n")
        temp_df = pd.DataFrame([[single_car["title"], single_car["clue_id"]]], columns=['title', 'clueID'])
        df = pd.concat([df, temp_df])
        getAllDataAndSaveToFile(car_brand, single_car["clue_id"], ct, ct_chn)
    # print(df.head(5))
    print('\n')


def save_info(df, file):
    return

def page_cover(url, car_brand, car_brand_chn, pg, ct, head):
    return

if __name__ == "__main__":
    for cb_, cb_chn_ in zip(car_brands, car_brands_chn):
        for ct_, ct_chn_ in zip(cities, cities_chn):
            deal_page(url, cb_, cb_chn_, ct_, ct_chn_, head)