import requests


def get_weather_city_code(city_name):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        url = "http://www.weather.com.cn/data/city3jdata/china.html"
        r = requests.get(url, headers=headers, timeout=10)
        r.encoding = "utf-8"
        provinces = r.json()
        for province_code, province_name in provinces.items():
            city_url = (
                "http://www.weather.com.cn/data/city3jdata/provshi/"
                f"{province_code}.html"
            )
            r2 = requests.get(city_url, headers=headers, timeout=10)
            r2.encoding = "utf-8"
            cities = r2.json()
            for city_code, city in cities.items():
                if city == city_name:
                    city_full_code = province_code + city_code
                    station_url = ("http://www.weather.com.cn/data/city3jdata/station/"
                        f"{city_full_code}.html")
                    r3 = requests.get(station_url,headers=headers,timeout=10)
                    r3.encoding = "utf-8"
                    stations = r3.json()
                    for station_code, station_name in stations.items():
                        if station_name in [city_name,city_name + "城区","市区"]:
                            return city_full_code + station_code
                    first_station = list(stations.keys())[0]
                    return city_full_code + first_station
        return None
    except Exception as e:
        print("错误:", e)
        return None

if __name__ == "__main__":
    city = input("请输入城市名称:")
    code = get_weather_city_code(city)
    if code:
        print(f"{city} 的中国天气网编码为:{code}")
    else:
        print("没有找到该城市")