import requests
import re

# 1. 提前创建csv文件
f = open("top250.csv", mode="w", encoding="utf-8")
# 写入csv表头
f.write("电影名称,导演,上映年份,评分,评价人数\n")

# 请求头（你的UA没问题，保留）
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

# 2. 豆瓣TOP250的翻页规律：每页25条，url的start参数 = 页数*25
# 0:第1页 25:第2页 50:第3页 ... 225:第10页
for page in range(10):
    start_num = page * 25
    url = f"https://movie.douban.com/top250?start={start_num}&filter="
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    content = resp.text

    # 正则
    obj = re.compile(
        r'<div class="item">.*?<span class="title">(?P<name>.*?)</span>.*?'
        r'导演: (?P<dao>.*?)&nbsp;&nbsp;(?P<type>.*?)<br>'
        r'(?P<year>.*?)&nbsp;/&nbsp.*?'
        r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
        r'<span>(?P<num>.*?)人评价</span>',
        re.S
    )

    # 匹配当前页数据并写入csv
    result = obj.finditer(content)
    for item in result:
        name = item.group("name").strip()
        dao = item.group("dao").strip()
        year = item.group("year").strip()
        score = item.group("score").strip()
        num = item.group("num").strip()
        # 写入csv，逗号分隔
        f.write(f"{name},{dao},{year},{score},{num}\n")
        # 控制台打印进度
        print(f"爬取成功：{name} | {dao} | {year} | {score}分 | {num}人评价")

# 3. 关闭文件和请求
f.close()
resp.close()
print("="*50)
print("豆瓣电影TOP250 全部250条数据 爬取完毕，已保存到 top250.csv 文件！")
