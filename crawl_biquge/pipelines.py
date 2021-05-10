# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pymysql
import logging

class CrawlBiqugePipeline(object):

	# db:数据连接  cursor:游标
	db = ''
	cursor = ''

	# 爬虫开始时执行
	def open_spider(self, spider):
		try:
			# 创建连接
			self.db = pymysql.connect(
				host = "localhost",			# 数据库地址
				port = 3306,				# 端口
				user = "root",				# 用户名称
				password = "Xiaogu971113",	# 用户密码
				database = "test",			# 数据库名称
				charset = "utf8"			# 字符集
				)
			print('数据库连接成功！')

			# 创建游标
			self.cursor = self.db.cursor()
		except:
			print('数据库连接失败！')
			os._exit(0)	#终止程序

		# 创建数据表 novel 和 chapter
		sql = """
		create table `novel` (
			`novel_id` int(11) auto_increment,
			`novel_name` varchar(255) not null,
			`novel_auther` varchar(255) default null,
			`novel_profile` text default null,
			`novel_cover` varchar(255) default null,
			`novel_type` varchar(10) default null,
			primary key (`novel_id`)
		) engine=innodb default charset=utf8
		"""
		self.cur.execute(sql);
		
		sql = """
		create table `chapter` (
			`chapter_id` int(11) auto_increment,
			`chapter_title` varchar(255) not null,
			`chatper_content` text not null,
			`novel_id` int(11) default null,
			primary key (`chapter_id`)
		) engine=innodb default charset=utf8
		"""
		self.cur.execute(sql);

	# 爬虫关闭时执行
	def close_spider(self, spider):
		# 关闭连接
		self.cur.close()
		self.db.close()
		print('关闭连接')

	def process_item(self, item, spider):

		print(item);
		
class TestPipeline(object):

	# db:数据连接 cursor:游标 datalist:缓冲池
	db = ''
	cursor = ''
	datalist = []


	# 爬虫开始时执行
	def open_spider(self, spider):
		try:
			# 创建连接
			self.db = pymysql.connect(
				host = "localhost",			# 数据库地址
				port = 3306,				# 端口
				user = "root",				# 用户名称
				password = "Xiaogu971113",	# 用户密码
				database = "test",			# 数据库名称
				charset = "utf8"			# 字符集
			)
			print('数据库连接成功！')

			# 创建游标
			self.cursor = self.db.cursor()
		except:
			print('数据库连接失败！')
			os._exit(0)	#终止程序

		# 创建数据表 
		sql = """
		create table if not exists `testData` (
			`novel_id` int(11) auto_increment,
			`novel_name` varchar(255) not null,
			`novel_auther` varchar(255) default null,
			`novel_profile` text default null,
			`novel_cover` varchar(255) default null,
			`novel_type` varchar(10) default null,
			`chapter_title` varchar(255) not null,
			`chapter_content` text not null,
			`sort` int(11),
			`get_chapter_content_time` datetime,
			primary key (`novel_id`)
		) engine=innodb default charset=utf8
		"""
		self.cursor.execute(sql)


	# 爬虫关闭时执行
	def close_spider(self, spider):
		# 爬虫关闭时 如果还有数据 将剩余的数据入库
		if len(self.datalist) > 0:
			# 数据入库
			self.bulk_insert_to_mysql(self.datalist)
			# 清空缓冲池
			del self.datalist[:]

		# 关闭数据库连接
		self.cursor.close()
		self.db.close()
		print('关闭连接')


	def process_item(self, item, spider):
		# 数据放入缓冲池
		self.datalist.append([
			item['novel_name'], 
			item['novel_auther'],
			item['novel_profile'], 
			item['novel_cover'],
			item['novel_type'], 
			item['chapter_title'],
			item['chapter_content'], 
			item['sort'],
			item['get_chapter_content_time']
		])

		# 每一百条数据 入一次数据库
		if len(self.datalist) == 100:
			# 数据入库
			self.bulk_insert_to_mysql(self.datalist)
			# 清空缓冲池
			del self.datalist[:]

		return item


	# 批量插入mysql数据库
	def bulk_insert_to_mysql(self, bulkdata):
		try:
			print("the length of the data-------%s" %len(self.datalist))
			sql = "insert into testData (novel_name, novel_auther, novel_profile, novel_cover, novel_type, chapter_title, chapter_content, sort, get_chapter_content_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			self.cursor.executemany(sql, bulkdata)
			self.db.commit()
		except:
			self.db.rollback()