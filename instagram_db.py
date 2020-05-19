# -*- coding: UTF-8 -*-

import pymysql

def select_instagram_star():
	# 打开数据库连接
	db = pymysql.connect("localhost","root","root","instagram",charset='utf8',port=3306)

	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# SQL 查询语句
	sql = "SELECT id,name,url,memberid,username,type_name FROM instagram_star ORDER BY id ASC LIMIT 150"
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

def select_ins_id(ins_id):
	# 打开数据库连接
	db = pymysql.connect("localhost","root","root","instagram",charset='utf8',port=3306)

	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# SQL 查询语句
	sql = "SELECT id FROM instagram_log WHERE ins_id = "+ins_id
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

def set_instagram_log(sid, sname, surl, smemberid, susername, stype_name, ins_id, thumb_img_src, thumb_img_width, thumb_img_height, thumb_img_url, img_src, img_width, img_height, img_url, shortcode, text, create_time):
	# 打开数据库连接
	db = pymysql.connect("localhost","root","root","instagram",charset='utf8',port=3306)

	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# SQL 更新语句
	sql = "INSERT INTO instagram_log SET sid = %s, sname = %s, surl = %s, smemberid = %s, susername = %s, stype_name = %s, ins_id = %s, thumb_img_src = %s, thumb_img_width = %s, thumb_img_height = %s, thumb_img_url = %s, img_src = %s, img_width = %s, img_height = %s, img_url = %s, shortcode = %s, text = %s, create_time = %s"
	try:
	   # 执行SQL语句
	   cursor.execute(sql,(sid, sname, surl, smemberid, susername, stype_name, ins_id, thumb_img_src, thumb_img_width, thumb_img_height, thumb_img_url, img_src, img_width, img_height, img_url, shortcode, text, create_time))
	   # 提交到数据库执行
	   db.commit()
	except:
	   # 发生错误时回滚
	   db.rollback()

	# 关闭数据库连接
	db.close()
















