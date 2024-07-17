from scrapy import signals
import zmail
import pyttsx3
class myextend:
    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.item_scraped, signal=signals.item_scraped)
        return o

    def spider_opened(self):
        print("start ---------")

    def item_scraped(self):
        print("item_scraped ---------")

    def spider_closed(self):
        print("close ----------")
        teacher = pyttsx3.init()
        # 设定朗读内容
        msg = "爬虫运行结束。邮件已发送完成"
        # 合成并播放语音
        teacher.say(msg)
        # 等待语音播放完
        teacher.runAndWait()
        mail_content = {
            'subject': 'Success!',  # 随便填写
            'content_text': '需要的数据已采集完成',  # 随便填写
        }
        server = zmail.server('zhang864071694@163.com', 'NGWGWZIHTEUQJJLU')
        server.send_mail('2182964128@qq.com', mail_content)

