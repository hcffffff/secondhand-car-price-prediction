from pandas.io import html
import requests
import os, re
import json
import pandas as pd
from spider import getAllDataAndSaveToFile, getNewData


url = "https://mapi.guazi.com/car-source/carList/pcList?minor=&sourceType=&ec_buy_car_list_ab=&location_city=&district_id=&tag=-1&license_date=&auto_type=&driving_type=&gearbox=&road_haul=&air_displacement=&emission=&car_color=&guobie=&bright_spot_config=&seat=&fuel_type=3&order=&priceRange=0,-1&tag_types=&diff_city=&intention_options=&initialPriceRange=&monthlyPriceRange=&transfer_num=&car_year=&carid_qigangshu=&carid_jinqixingshi=&cheliangjibie=&page={pg}&pageSize=20&city_filter=12&city=12&guazi_city=12&qpres=499374582726520832&versionId=0.0.0.0&osv=IOS&platfromSource=wap"

head = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}


def deal_page(url, head):
    """
    对筛选数据页的初步处理，获取电动车的总数量以及页面数量
    """
    url1 = f"https://mapi.guazi.com/car-source/carList/pcList?minor=&sourceType=&ec_buy_car_list_ab=&location_city=&district_id=&tag=-1&license_date=&auto_type=&driving_type=&gearbox=&road_haul=&air_displacement=&emission=&car_color=&guobie=&bright_spot_config=&seat=&fuel_type=3&order=&priceRange=0,-1&tag_types=&diff_city=&intention_options=&initialPriceRange=&monthlyPriceRange=&transfer_num=&car_year=&carid_qigangshu=&carid_jinqixingshi=&cheliangjibie=&page=1&pageSize=20&city_filter=12&city=12&guazi_city=12&qpres=499374582726520832&versionId=0.0.0.0&osv=IOS&platfromSource=wap"
    page = requests.get(url1, headers=head, timeout=3)
    # f = open("./crawl_for_guazi/test.json", 'w')
    # f.write(page.text)
    page_text_dict = json.loads(page.text)
    page, total_page, total = (
        page_text_dict["data"]["page"],
        page_text_dict["data"]["totalPage"],
        page_text_dict["data"]["total"],
    )
    while page <= total_page:
        get_single_page_info(url, page, head)
        page += 1
    print(f"Finish! Total is {total}.", end="\n")


def get_single_page_info(url, pg, head):
    """
    获取每一页的车辆数据信息（每一页大概是20辆车）
    """
    url = url.format(pg=pg)
    page = requests.get(url, headers=head, timeout=3)
    page_text = json.loads(page.text)
    df = pd.DataFrame()
    for single_car in page_text["data"]["postList"]:
        # print(single_car["title"] + "clueid = " + str(single_car["clue_id"]), end="\n")
        temp_df = pd.DataFrame(
            [[single_car["title"], single_car["clue_id"]]], columns=["title", "clueID"]
        )
        df = pd.concat([df, temp_df])
        getAllDataAndSaveToFile(single_car["clue_id"])
    # print(df.head(5))


def get_new_page(url, head, idList):
    '''
    用于获取测试集
    '''
    url1 = f"https://mapi.guazi.com/car-source/carList/pcList?minor=&sourceType=&ec_buy_car_list_ab=&location_city=&district_id=&tag=-1&license_date=&auto_type=&driving_type=&gearbox=&road_haul=&air_displacement=&emission=&car_color=&guobie=&bright_spot_config=&seat=&fuel_type=3&order=&priceRange=0,-1&tag_types=&diff_city=&intention_options=&initialPriceRange=&monthlyPriceRange=&transfer_num=&car_year=&carid_qigangshu=&carid_jinqixingshi=&cheliangjibie=&page=1&pageSize=20&city_filter=12&city=12&guazi_city=12&qpres=499374582726520832&versionId=0.0.0.0&osv=IOS&platfromSource=wap"
    page = requests.get(url1, headers=head, timeout=3)
    page_text_dict = json.loads(page.text)
    page, total_page, pageTotal = (
        page_text_dict["data"]["page"],
        page_text_dict["data"]["totalPage"],
        page_text_dict["data"]["total"],
    )
    print(pageTotal)
    total = 0
    while page <= total_page:
        total = total + get_new_single_page_info(url, page, head, idList)
        page += 1
        if page > 1: # 用于测试，只获取1页（20辆车）的数据
            break
    print(f"Finish! Total is {total}/{pageTotal}.", end="\n")


def get_new_single_page_info(url, pg, head, idList):
    '''
    用于获取测试集（新数据）
    '''
    url = url.format(pg=pg)
    page = requests.get(url, headers=head, timeout=3)
    page_text = json.loads(page.text)
    df = pd.DataFrame()
    count = 0
    for single_car in page_text["data"]["postList"]:
        # print(single_car["title"] + "clueid = " + str(single_car["clue_id"]), end="\n")
        temp_df = pd.DataFrame(
            [[single_car["title"], single_car["clue_id"]]], columns=["title", "clueID"]
        )
        df = pd.concat([df, temp_df])
        count += getNewData(single_car["clue_id"], idList)
    return count


if __name__ == "__main__":
    # deal_page(url, head)
    path = 'crawl_for_guazi/allData'
    allCarFiles = os.listdir(path)
    idList = []
    for singleFileName in allCarFiles:
        if '.json' not in singleFileName:
            continue
        idList.append(int(singleFileName.split('.')[0]))
    # print(idList)
    get_new_page(url, head, idList)
