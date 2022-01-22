import requests
import json
import execjs

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
}

# 保险起见，运行时建议修改最新的时间戳即client-time字段（md5.js中也要修改）和verify-token字段，可以自行在网页中的标头中获取

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


def get_carInfo(clueId, guazi_city):
    stringify_params = f"ca_n=default&ca_s=seo_baidu&clueId={clueId}&deviceId=12be6bb1-1b41-4bda-f274-d18b315e9065&guazi_city={guazi_city}&lat=0&lng=0&osv=ios&platfromSource=wap&sourceFrom=wap&versionId=0.0.0.0"
    headers["verify-token"] = get_verify_token(stringify_params)
    base_url = f"https://mapi.guazi.com/car-source/carDetail/ecDetail?clueId={clueId}&guazi_city={guazi_city}&ca_s=seo_baidu&ca_n=default&osv=ios&lng=0&lat=0&deviceId=12be6bb1-1b41-4bda-f274-d18b315e9065&versionId=0.0.0.0&sourceFrom=wap&platfromSource=wap"
    response = requests.get(url=base_url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        data = result["data"]
        return data


# test:
if __name__ == "__main__":
    clueId = "115459575"
    guazi_city = "12"
    data = get_carInfo(clueId, guazi_city)
    print(data["carCommodityInfo"]["carPriceInfo"]["styleData"]["price"]["value"]) # 二手价格
    print(data["carCommodityInfo"]["carPriceInfo"]["styleData"]["newPrice"]["value"]) # 新车价格
    # f = open("./crawl_for_guazi/test_carData.json", 'w')
    # json.dump(data, f)
