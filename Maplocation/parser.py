import Maplocation.utli
from base._spider import BaseSpider
from base.parser.subparser import WebSubParser
from bs4 import BeautifulSoup


class Parser(BaseSpider):
    def __init__(self) -> None:
        """百度搜索解析器"""
        super().__init__()
        self.webSubParser = WebSubParser()

    def parse_web(self, content: str, indicator: list) -> dict:
        """解析搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度网页搜索HTML源码.
            exclude (list): 要屏蔽的控件.

        Returns:
            dict: 解析后的结果
        """
        soup = BeautifulSoup(content, "html.parser")
        if not soup.find("div", id="root"):
            return {"results": [], "pages": 0, "total": 0}

        # 定义预结果（运算以及相关搜索）
        pre_results = []
        # 预处理
        ans = soup.find("div", class_="ant-table-tbody")
        ans_detail = self.webSubParser.parse_answer(ans)

        # 加载搜索结果总数
        # 已经移动到根字典中
        # if num != 0:
        #     pre_results.append(dict(type="total", result=num))
        # 加载结果
        pre_results.append(indicator)
        pre_results.append(dict(type="ans", results=ans_detail))
        Maplocation.utli.tabluate(pre_results, 'ans')

        return {
            "results": pre_results,
        }
