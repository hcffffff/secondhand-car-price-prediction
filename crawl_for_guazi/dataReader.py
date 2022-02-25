import json
import pandas as pd
import os


def getDict(title, dict):
    '''
    获取一个子列表，并返回该列表
    '''
    for child in dict:
        if child['title'] == title:
            return child
    return None


def readSingleCarFile(path):
    '''
    读位于allData目录下的单个车辆信息json文件
    '''
    with open(path) as f:
        car_dict = json.load(f)
        return {
            'id': car_dict['dataRough']['baseInfo']['carOtherInfo']['clueId'], # clueId
            'car_name': car_dict['dataRough']['carCommodityInfo']['basicInfo']['titleDesc'], # 车辆详细型号
            'car_brand': car_dict['dataRough']['baseInfo']['carOtherInfo']['minorName'], # 车辆品牌
            'car_tag': car_dict['dataRough']['baseInfo']['carOtherInfo']['tagName'], # 具体型号

            'price': car_dict['dataRough']['carCommodityInfo']['carPriceInfo']['styleData']['price']['value'], # 二手车价格 单位：元
            'new_price': car_dict['dataRough']['carCommodityInfo']['carPriceInfo']['styleData']['newPrice']['value'], # 新车价格 单位：元

            'complexOutlook': car_dict['dataRough']['carCommodityInfo']['carRecordInfo']['reportResultAnalysis']['complex'] if 'reportResultAnalysis' in car_dict['dataRough']['carCommodityInfo']['carRecordInfo'] else None, # 整体成色，如果不存在该词条返回None
            'firstCert': car_dict['dataRough']['carCommodityInfo']['carRecordInfo']['salienceItem'][0]['value'], # 首次上牌年月
            'odograph': car_dict['dataRough']['carCommodityInfo']['carRecordInfo']['salienceItem'][1]['value'], # 表显里程

            'allPower': car_dict['dataRough']['carCommodityInfo']['carRecordInfo']['summary'][2]['value'], # 总功率 单位kW
            'carBelong': car_dict['dataRough']['carCommodityInfo']['carRecordInfo']['summary'][3]['value'], # 车牌归属地
            'range': car_dict['dataRough']['carCommodityInfo']['carRecordInfo']['summary'][4]['value'], # 续航里程

            'isDome': 1 if car_dict['dataDetail']['list'][0]['children'][1]['content'] == '国产' else 0, # 是否为国产
            'wheelBase': getDict('车身结构', car_dict['dataDetail']['list'])['children'][0]['content'] if getDict('车身结构', car_dict['dataDetail']['list']) else None, # 轴距（mm）
            'drivingMode': getDict('底盘转向', car_dict['dataDetail']['list'])['children'][0]['content'] if getDict('底盘转向', car_dict['dataDetail']['list']) else None, # 驱动方式
        }


if __name__ == "__main__":
    path = 'crawl_for_guazi/allData'
    allCarFiles = os.listdir(path)
    df = pd.DataFrame([])
    for singleFileName in allCarFiles:
        if '.json' not in singleFileName:
            continue
        singleCardict = readSingleCarFile(path + f'/{singleFileName}')
        tempdf = pd.DataFrame(singleCardict, index=[0])
        df = df.append(tempdf)
    df = df.reset_index(drop = True)
    # print(df.head())
    # print(df.shape)
    df.to_csv('crawl_for_guazi/data.csv', index = False)
