#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymysql

def select_instagram():
	# 打开数据库连接
	db = pymysql.connect("localhost","root","root","instagram",charset='utf8',port=3306)

	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# SQL 查询语句
	sql = "SELECT articleid, title FROM t_article WHERE flag=13 AND source_author=''"
	try:
	   # 执行SQL语句
	   cursor.execute(sql)
	   # 获取所有记录列表
	   results = cursor.fetchall()

	   return results
	except:
	   print('Error: unable to fecth data')

	# 关闭数据库连接
	db.close()

def set_source_author(ids,val):
	# 打开数据库连接
	db = pymysql.connect("localhost","root","root","instagram",charset='utf8',port=3306)

	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# SQL 更新语句
	sql = "UPDATE t_article SET source_author = %s WHERE articleid = %s"
	try:
	   # 执行SQL语句
	   cursor.execute(sql,(val,ids))
	   # 提交到数据库执行
	   db.commit()
	except:
	   # 发生错误时回滚
	   db.rollback()

	# 关闭数据库连接
	db.close()

def set():
	ins_list = select_instagram()
	for ins in ins_list:
		source_author = ins[1].rpartition('——')
		print(ins[0],source_author[0])
		set_source_author(ins[0],source_author[0])

set()