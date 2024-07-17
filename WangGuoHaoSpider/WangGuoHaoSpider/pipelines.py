# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class WangguohaospiderPipeline:
    def process_item(self, item, spider):
        return item

import pymysql


class WangGuoHaoPipeline:
    WGH的连接 = pymysql.Connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        port=3306,
    )
    WGH的游标 = WGH的连接.cursor()
    def __init__(self):
        self.WGH的游标.execute("CREATE DATABASE IF NOT EXISTS `wangguohao_db`")
        创建表的语句 = """
                    CREATE TABLE IF NOT EXISTS `wangguohao` (
                            `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                            `date` VARCHAR(20),
                            `title` VARCHAR(200),
                            `area` VARCHAR(50),
                            `cate` VARCHAR(20)
                    )
                """
        self.WGH的游标.execute("USE `wangguohao_db`")
        self.WGH的游标.execute(创建表的语句)
    def process_item(self, item, spider):
        查询语句 = "SELECT * FROM wangguohao WHERE title=%s"
        self.WGH的游标.execute(查询语句, (item['采购标题'], ))
        结果 = self.WGH的游标.fetchall()
        if not 结果:
            插入语句 = "INSERT INTO wangguohao (date, title, area, cate)VALUES(%s,%s,%s,%s)"
            self.WGH的游标.execute(插入语句, (item['日期'], item['采购标题'], item['地区'], item['项目类型']))
            self.WGH的连接.commit()
        return item

    def __del__(self):
        self.WGH的游标.close()
        self.WGH的连接.close()


