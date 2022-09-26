import hashlib
import time
from typing import Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from multiprocessing import Process
from threading import Thread
from Maplocation import utli


class MaplocationSpider():

    def __init__(self, cookie: str = None) -> None:
        """初始化
        - 设置Cookie：
            Cookie可以被用于增强爬虫的真实性，尽可能减少封禁IP的概率。
            cookie = "Hm_lvt_08d69bacaa4e3cf394f0b5647eb2b258=1663399760; Hm_lpvt_08d69bacaa4e3cf394f0b5647eb2b258=1663399760"

            如果你想获取你的Cookie，请打开你的网站，并
            按F12打开开发者工具，然后在开发者工具最上方的选项栏中选择“网络”（Network）这一选项，点击
            出现的列表中最上方的以`maplocation.sjfkai.com`开头的选项，在出现的详情中找到`Request Headers`
            一项，然后在它的下方找到`Cookie`，并复制Cookie这一选项内（不包括`Cookie: `）后面的所有内容，
            并将它粘贴在你需要的位置。

            请勿传入非法的Cookie。

        Args:
            cookie (Union[str, None], optional): 浏览器抓包得到的cookie. Defaults to None.
        """
        super().__init__()
        # 爬虫名称（不是请求的，只是用来标识）
        self.spider_name = "MaplocationSpider"
        # 解析Cookie
        if cookie:
            if "__yjs_duid" not in cookie:
                cookie += "; __yjs_duid=1_" + str(hashlib.md5().hexdigest()) + "; "
            else:
                _ = cookie.split("__yjs_duid=")
                __ = _[1].split(";", 1)[-1]
                ___ = hashlib.md5()
                cookie = _[0] + "__yjs_duid=1_" + str(___.hexdigest()) + "; " + __
        # 设置请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Sec-Fetch-Mode": "navigate",
            "Cookie": cookie,
            "Connection": "Keep-Alive",
        }

        self.EMPTY = {"results": [], "pages": 0, "total": 0}
        # self.indicator = ["order", "aderss", "longitude", "latitude", "is_real", "credibility", "address_type", "Coordinate_System", "error"]
        self.indicator = ["序号", "地址", "经度", "纬度", "是否精确", "可信度", "地址类型", "坐标系", "错误"]

    def search_web(self, querys: []):
        """coockie = "Hm_lvt_08d69bacaa4e3cf394f0b5647eb2b258=1663399760; Hm_lpvt_08d69bacaa4e3cf394f0b5647eb2b258=1663401613"
        Returns:
            WebResult: 爬取的返回值和搜索结果
        """

        url = f"https://maplocation.sjfkai.com/"
        # 启动chrome浏览器，填入chromedriver浏览器的位置
        # 没有的化需要下载与安装的chrome对应版本
        # 下载地址：http://chromedriver.storage.googleapis.com/index.html
        # 若使用火狐浏览器，则使用 wd = webdriver.Firefox()
        # 还可以使用IE、EDGE等等
        options = webdriver.ChromeOptions()
        out_path = r'D:\QMDownload\data_store'  # 是你想指定的下载路径
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
        options.add_experimental_option('prefs', prefs)
        wd = webdriver.Chrome(
            executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver_win32\chromedriver.exe',
            chrome_options=options)
        wd.implicitly_wait(10)
        wd.get(url)

        # 定位编辑框
        element = wd.find_element(By.ID, "locations")
        element.clear()
        for query in querys:
            # text = quote(query)
            for data in query:
                # element.send_keys(data + "\n")
                element.send_keys(data)
        # 定位“转换”按钮
        press = wd.find_element(By.CLASS_NAME, "ant-btn.ant-btn-primary")
        # webdriver.ActionChains(wd).move_to_element(element).click(element).perform()
        press.click()

        # 定位“下载”按钮，给足充分的时间转换
        time.sleep(700)
        download = wd.find_element(By.CLASS_NAME, "ant-btn.table-btn")
        download.click()
        time.sleep(3)
        print()

    def download_by_html(self, wd):
        time.sleep(5)
        handles = wd.window_handles  # 获取当前浏览器的所有窗口句柄
        wd.switch_to.window(handles[-1])  # 切换到最新打开的窗口

        # 定位表格
        # butom1 = wd.find_element(By.CLASS_NAME, "ant-table-tbody")
        ans_rows = wd.find_elements(By.CLASS_NAME, "ant-table-row.ant-table-row-level-0")
        print(len(ans_rows))

        # 保存结果
        ans_result = []
        ans_result.append(self.indicator)
        for result in ans_rows:
            data = []
            # assert result.find_element(By.CLASS_NAME, "Internal Service Error:无相关结果"), "请输入正确的地址"
            data_row = result.find_elements(By.TAG_NAME, "td")
            for res in data_row:
                if res.text != "删除":
                    data.append(res.text)
                    if res.text:
                        print(res.text)
            ans_result.append(data)

        # 存储成csv文件
        utli.tabluate(ans_result, "ans")

    def mutiprocess(self, querys: [[[]]]):
        process = []
        start = time.time()
        for i in range(len(querys)):
			# p = Process(target=self.search_web, args=(querys[i],))
            p = Thread(target=self.search_web, args=(querys[i],))  # args一般为三元组，如只有一个参数，必须加','
            p.start()  # 生成多个进程并启动
            process.append(p)

        for p in process:
            p.join()
        end = time.time()
        print("总用时: ", end - start)
