'''
根据车辆的clueId和city字段号获取详细信息，并返回一个字典
'''
import requests
import json
import execjs
import os

headers = {
    "authority": "mapi.guazi.com",
    "accept": "application/json, text/plain, */*",
    "verify-token": "90aa6e100ff698b2ae6f076a89dd4817",
    "client-time": "1642868960",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1",
    "token": "",
    "origin": "https://m.guazi.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://m.guazi.com/",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "uuid=12be6bb1-1b41-4bda-f274-d18b315e9065; user_city_id=12; cityDomain=bj; sessionid=f54546b2-bd1c-471c-a4d4-53f3a4e58543; tktrackid=404395297875746816; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22%25e7%2593%259c%25e5%25ad%2590%25e4%25ba%258c%25e6%2589%258b%25e8%25bd%25a6%25e7%259b%25b4%25e5%258d%2596%25e7%25bd%2591%22%7D; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22%25e7%2593%259c%25e5%25ad%2590%25e4%25ba%258c%25e6%2589%258b%25e8%25bd%25a6%25e7%259b%25b4%25e5%258d%2596%25e7%25bd%2591%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22guid%22%3A%2212be6bb1-1b41-4bda-f274-d18b315e9065%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%222%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22sessionid%22%3A%22cf0d98fd-b82b-47b1-8b6c-1f95f4186181%22%7D; puuid=9253fd9b-b612-4110-c255-389dddd04349; browsingHistoryCount=1",
} # 保险起见，运行时建议修改最新的时间戳即client-time字段（md5.js中也要修改）和verify-token字段，可以自行在网页中的标头中获取

def get_verify_token(stringify_params):
    """
    获取 verify_token
    """
    with open("crawl_for_guazi/md5.js", mode="r", encoding="utf-8") as fp:
        js_code = fp.read()
        etx = execjs.compile(js_code)
        verify_token = etx.call("Verify_Token", stringify_params)
        return verify_token
    # stringifyParams


def getCarInfo(clueId):
    '''
    获取车辆基础数据
    '''
    stringify_params = f"ca_n=default&ca_s=seo_baidu&clueId={clueId}&deviceId=12be6bb1-1b41-4bda-f274-d18b315e9065&guazi_city=12&lat=0&lng=0&osv=ios&platfromSource=wap&sourceFrom=wap&versionId=0.0.0.0"
    headers["verify-token"] = get_verify_token(stringify_params)
    base_url = f"https://mapi.guazi.com/car-source/carDetail/ecDetail?clueId={clueId}&guazi_city=12&ca_s=seo_baidu&ca_n=default&osv=ios&lng=0&lat=0&deviceId=12be6bb1-1b41-4bda-f274-d18b315e9065&versionId=0.0.0.0&sourceFrom=wap&platfromSource=wap"
    response = requests.get(url=base_url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        data = result["data"]
        # highlightConfigItem = data['carCommodityInfo']['carRecordInfo']['highlightConfigItem']
        # return data, {
        #     '型号': data['baseInfo']['carOtherInfo']['tagName'],
        #     '二手价格': data["carCommodityInfo"]["carPriceInfo"]["styleData"]["price"]["value"],
        #     '新车价格': data["carCommodityInfo"]["carPriceInfo"]["styleData"]["newPrice"]["value"],
        #     '首次上牌日期': data['carCommodityInfo']['carRecordInfo']['salienceItem'][0]['value'],
        #     '表显里程': data['carCommodityInfo']['carRecordInfo']['salienceItem'][1]['value'],
        #     '综合成色': data['carCommodityInfo']['carRecordInfo']['reportResultAnalysis']['complex'],
        #     '过户次数': data['carCommodityInfo']['carRecordInfo']['summary'][0]['value'],
        #     '归属地': data['carCommodityInfo']['carRecordInfo']['summary'][2]['value'],
        #     '续航里程': data['carCommodityInfo']['carRecordInfo']['summary'][3]['value'],
        #     '电池容量': data['carCommodityInfo']['carRecordInfo']['summary'][5]['value'],
        #     '出厂日期': data['carCommodityInfo']['carRecordInfo']['summary'][9]['value'],
        #     '有无并线辅助': isHighlight(highlightConfigItem, '并线辅助'),
        #     '有无自动驻车': isHighlight(highlightConfigItem, '自动驻车'),
        #     '有无四驱系统': isHighlight(highlightConfigItem, '四驱系统'),
        #     '有无座椅加热': isHighlight(highlightConfigItem, '座椅加热')
        # }
        return data
    else:
        print(clueId + " has problems!")
        return '', {
            '型号': '','二手价格': '','新车价格': '','首次上牌日期': '','表显里程': '','过户次数': '','续航里程': '','电池容量': ''
        }


def getDetailInfo(clueId):
    '''
    获取车辆更详细数据
    '''
    stringify_params = f"clueId={clueId}&deviceid=12be6bb1-1b41-4bda-f274-d18b315e9065&guazi_city=12&osv=ios&platfromSource=wap&versionId=0.0.0.0"
    headers["verify-token"] = get_verify_token(stringify_params)
    base_url = f'https://mapi.guazi.com/car-source/carRecord/configurations?versionId=0.0.0.0&osv=ios&clueId={clueId}&deviceid=12be6bb1-1b41-4bda-f274-d18b315e9065&guazi_city=12&platfromSource=wap'
    response = requests.get(url=base_url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        data = result['data']
        return data
    else:
        print('error!')


def isHighlight(data, highlight):
    '''
    data为data['carCommodityInfo']['carRecordInfo']['highlightConfigItem'] 一个列表
    返回1，如果这辆车有该项highlight；
    否则返回0
    '''
    for hasHighlight in data:
        # print(hasHighlight['title'])
        if hasHighlight['title'] == highlight:
            return 1
    return 0


def getAllDataAndSaveToFile(clueId):
    '''
    为方便调用的封装函数，目的是将数据存储在位于'./crawl_for_guazi/allData'的json文件中
    '''
    dataInfo = getCarInfo(clueId)
    dataDetail = getDetailInfo(clueId)
    tempDict = {'dataRough': dataInfo, 'dataDetail': dataDetail}
    f = open(f"./crawl_for_guazi/allData/{clueId}.json", 'w')
    json.dump(tempDict, f, ensure_ascii=False)


# test:
if __name__ == "__main__":
    clueId = "115928025"
    getAllDataAndSaveToFile(clueId)
