import requests
import random

KEYS = ['DBEAF4669920AFF08A065931753E4EC7']
API_URL = 'https://api.ip2location.io'

def get_location(ip_address):
    key = random.choice(KEYS)  # 从列表中随机选择一个key
    try:
        response = requests.get(f'{API_URL}?key={key}&ip={ip_address}&format=json')
        response.raise_for_status()  # 如果请求失败，则引发异常
        data = response.json()
        region_name = data.get("region_name").replace("'", "")
        location_data = {
            "country": data.get("country_code"),
            "regionName": region_name
        }
        return location_data
    except requests.exceptions.RequestException as e:
        print(f"发生错误：{e}")
        return None

