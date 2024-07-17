import scrapy


class WangguohaoSpider(scrapy.Spider):
    name = "wangguohao"
    allowed_domains = ["qianlima.com"]
    start_urls = ["http://zb.yfb.qianlima.com/yfbsemsite/mesinfo/zbpglist"]

    lb = []
    data = {
        'pageNo': '1',
        'provinceName': '河南'
    }
    def parse(self, response):
        yield scrapy.FormRequest(
            url=response.url,
            callback=self.parse_wgh_onepage,
            dont_filter=True,
            formdata=self.data
        )
    def parse_wgh_onepage(self, response):
        招标s = response.xpath("//table[@id='contentTable']/tbody/tr")
        for 招标 in 招标s:
            日期 = 招标.xpath("td[1]/text()").get("没有日期").strip()
            地区 = 招标.xpath("td[2]/text()").get("没有地区").strip()
            项目类型 = 招标.xpath("td[3]/text()").get("没有项目类型").strip()
            采购标题 = 招标.xpath("td[4]/a/text()").get("没有采购标题").strip()
            if 采购标题 in self.lb:
                print("数据已采集")
            else:
                self.lb.append(采购标题)
                itme = {
                    '日期': 日期,
                    '地区': 地区,
                    '项目类型': 项目类型,
                    '采购标题': 采购标题,
                }
                yield itme
        pd = response.xpath("//*[contains(text(),'下一页')]/@onclick")
        if pd:
            page = int(self.data['pageNo'])
            page += 1
            self.data['pageNo'] = str(page)
            yield scrapy.FormRequest(url=response.url,
                                     callback=self.parse_wgh_onepage,
                                     dont_filter=True,
                                     formdata=self.data
                                     )

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl wangguohao".split())