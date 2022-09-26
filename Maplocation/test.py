# 导入BaiduSpider
import string

from Maplocation import MaplocationSpider

cookie = "Hm_lvt_08d69bacaa4e3cf394f0b5647eb2b258=1663399760; Hm_lpvt_08d69bacaa4e3cf394f0b5647eb2b258=1663401613"
spider = MaplocationSpider(cookie=cookie)

# 加载数据
file = open('E:\Desktop\实验1.txt', encoding='utf-8')
dataMat = []
temp = []
for line in file.readlines():
    curLine = line.split(" ")
    temp.append(curLine)
    if len(temp) == 1000:  # 一次性爬取的数据个数
        dataMat.append(temp)
        temp = []
print('dataMat:', dataMat)

# 搜索网页
# querys = [["上海", "北京"], ["天津", "马旭"]]
spider.mutiprocess(querys=dataMat)
