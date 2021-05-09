# -*- coding: utf-8 -*-
import os
import scrapy 
from crawl_biquge.items import TestItem

# 项目文件所在位置
# /d/study/code/python/crawler/crawl_biquge/crawl_biquge

class NovelSpider(scrapy.Spider):
	# 爬虫名称
    name = 'novel'
    # 爬虫的可信域名
    allowed_domains = ['xbiquge.la']
    # 最开始的url
    start_urls = ['http://www.xbiquge.la/xiaoshuodaquan/']

    # 设置指定的管道
    custom_settings = {
        'ITEM_PIPELINES': {'crawl_biquge.pipelines.TestPipeline': 300, }
    }

    # 解析html获取所需的数据
    def parse(self, response):

        # 获取所有小说名字 以及详情页连接
        # 
        # //div[@id="main"]/div[@class="novellist"]/ul/li
        # //div[@id="main"]/div[@class="novellist"][1]/ul/li[1]
        novellist = response.xpath('//div[@id="main"]/div[@class="novellist"]/ul/li');
        for novel in novellist:

            # 获取小说详情页链接
            novelurl = novel.xpath('./a/@href').extract()[0]

            # 进入 小说详情页
            yield scrapy.Request(novelurl, callback=self.novelInfo)
    
    # 抓取小说详情页数据
    def novelInfo(self, response):

        # 抓取小说基本信息
        novel_name = response.xpath('//div[@id="info"]/h1/text()').extract()[0]
        novel_auther = response.xpath('//div[@id="info"]/p[1]/text()').extract()[0]
        novel_profile = response.xpath('//div[@id="intro"]/p[2]/text()').extract()[0]
        novel_cover = response.xpath('//div[@id="fmimg"]/img/@src').extract()[0]
        novel_type = response.xpath('//div[@id="wrapper"]/div[@class="box_con"]/div[@class="con_top"]/a[2]/text()').extract()[0]

        # 用于小说章节排序
        sort = 0

        # 抓取小说章节 及 章节内容 
        # 这时的 章节是有序的 
        chatpers = response.xpath('//div[@id="list"]/dl/dd')
        for chatper in chatpers:
            sort = sort + 1
            item = TestItem()
            item['sort'] = sort
            item['novel_name'] = novel_name
            item['novel_auther'] = novel_auther
            item['novel_profile'] = novel_profile
            item['novel_cover'] = novel_cover
            item['novel_type'] = novel_type
            
            chapter_title = chatper.xpath('./a/text()').extract()[0]
            item['chapter_title'] = chapter_title

            chapter_content_url = 'http://www.xbiquge.la' + chatper.xpath('./a/@href').extract()[0]

            yield scrapy.Request(chapter_content_url, meta={'item': item}, callback=self.getChatper)

    # 获取小说章节内容
    def getChatper(self, response):
        item = response.meta['item']
        item['chapter_content'] = response.xpath('//div[@id="content"]/text()').extract()[0]

        yield item