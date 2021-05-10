# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# class CrawlBiqugeItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

# class NovelItem(scrapy.Item):
# 	novel_name = scrapy.Field()		# 小说名字
# 	novel_auther = scrapy.Field()	# 小说作者
# 	novel_profile = scrapy.Field()	# 小说简介
# 	novel_cover = scrapy.Field()	# 小说封面
# 	novel_type = scrapy.Field()		# 小说分类

# class ChapterItem(scrapy.Item):
# 	chapter_title = scrapy.Field()		# 章节标题
# 	chapter_content = scrapy.Field()	# 章节内容
# 	novel_id = scrapy.Field()			# 小说编号

class TestItem(scrapy.Item):
	sort = scrapy.Field()	# 小说章节排序
	novel_name = scrapy.Field()		# 小说名字
	novel_auther = scrapy.Field()	# 小说作者
	novel_profile = scrapy.Field()	# 小说简介
	novel_cover = scrapy.Field()	# 小说封面
	novel_type = scrapy.Field()		# 小说分类
	chapter_title = scrapy.Field()		# 章节标题
	chapter_content = scrapy.Field()	# 章节内容
	get_chapter_content_time = scrapy.Field() #获取章节内容的时间
