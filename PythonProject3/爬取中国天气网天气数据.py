import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_weather_7days(city_code):
    # 获取页面显示七天天气数据时的网址,构造URL
    url = f'http://www.weather.com.cn/weather/{city_code}.shtml'

    # 反反爬,伪装成浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print(f"正在请求: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'

        # 检查请求是否成功（状态码200表示成功）
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return None

        # 解析网页源代码
        soup = BeautifulSoup(response.text, 'lxml')

        # 中国天气网的7天数据存放在 id="7d" 的div标签里里，类名为 "t clearfix" 的ul中
        weather_div = soup.find('div', id='7d')
        weather_ul = weather_div.find('ul', class_='t clearfix')
        # 每一天的天气数据在<li>标签中,检索所有该标签
        days = weather_ul.find_all('li')

        # 将提取到的数据放入空列表里
        weather_data = []

        # 从每一天中提取各项详细数据
        for day in days:
            # 提取日期（在<h1>标签里）
            date_tag = day.find('h1')
            date = date_tag.text.strip() if date_tag else '未知日期'

            # 提取天气状况（在<p class="wea">里）
            weather_tag = day.find('p', class_='wea')
            weather = weather_tag.text.strip() if weather_tag else '未知天气'

            # 提取温度（在<p class="tem">里）
            temp_tag = day.find('p', class_='tem')
            if temp_tag:
                # 获取纯文本
                temp_text = temp_tag.get_text(strip=True)
                # 去除摄氏度符号
                temp_text = temp_text.replace('℃', '')
                # 按 '/' 拆分成最高温和最低温
                if '/' in temp_text:
                    high_temp, low_temp = temp_text.split('/')
                else:
                    # 如果没有'/'，说明只有单个温度
                    high_temp = temp_text
                    low_temp = temp_text
            else:
                high_temp = '无数据'
                low_temp = '无数据'

            # 将所有数据放入字典中
            weather_data.append({
                '日期': date,
                '天气状况': weather,
                '最高温(℃)': high_temp,
                '最低温(℃)': low_temp
            })

        print(f"成功爬取到 {len(weather_data)} 天的数据")
        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")
        return None
    except Exception as e:
        print(f"解析过程发生错误: {e}")
        return None


# 7. 保存数据到CSV文件
def save_to_csv(data, filename='weather_forecast.csv'):
    df = pd.DataFrame(data)

    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"数据已成功保存到: {filename}")


if __name__ == "__main__":

    CITY_CODE = {
        '北京': '101010100',
        '上海': '101020100',
        '广州': '101280101',
        '深圳': '101280601',
        '杭州': '101210101',
        '成都': '101270101',
        '武汉': '101200101',
        '南京': '101190101',
        '重庆': '101040100',
        '长沙': '101250101'
    }
    user_input = input("请输入您所要查询的城市:")
    if user_input in CITY_CODE:
        city_code = CITY_CODE[user_input]
    # 调用函数
    result = get_weather_7days(city_code)

    # 如果爬取成功，就保存数据
    if result:
        save_to_csv(result)
    # 降低爬取速率,防止被封
    time.sleep(1)