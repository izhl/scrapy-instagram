#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymysql
import decimal

def select_user_list():
	# 打开数据库连接
	db = pymysql.connect("localhost","root","root","instagram",charset='utf8',port=3306)

	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# SQL 查询语句
	sql = "SELECT user_id, fticoin, freeze_fticoin FROM ch_account"
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

def get_recharge(user_id):
	# 打开数据库连接
	db = pymysql.connect("localhost","root","root","instagram",charset='utf8',port=3306)

	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# SQL 查询语句
	sql = "SELECT sum(recharge_ifs) as recharge FROM ch_fti_block_recharge_log WHERE user_id=%s AND is_confirmed=1"
	try:
	   # 执行SQL语句
	   cursor.execute(sql,(user_id))
	   # 获取所有记录列表
	   results = cursor.fetchall()

	   return results
	except:
	   print('Error: unable to fecth data')

	# 关闭数据库连接
	db.close()

def get_withdraw(user_id):
	# 打开数据库连接
	db = pymysql.connect("localhost","root","root","instagram",charset='utf8',port=3306)

	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# SQL 查询语句
	sql = "SELECT SUM(fancoin) as fancoin, SUM(commission) AS commission FROM ch_withdraw WHERE ch_withdraw_type=2 AND currency_type=2 AND user_id=%s"
	try:
	   # 执行SQL语句
	   cursor.execute(sql,(user_id))
	   # 获取所有记录列表
	   results = cursor.fetchall()

	   return results
	except:
	   print('Error: unable to fecth data')

	# 关闭数据库连接
	db.close()

def add_yichang(user_id,user_fticoin,user_freeze_fticoin,user_withdraw_fancoin,user_withdraw_commission,user_recharge,yichang):
	# 打开数据库连接
	db = pymysql.connect("localhost","root","root","instagram",charset='utf8',port=3306)

	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# SQL 更新语句
	sql = "INSERT INTO yichang SET user_id = %s, user_fticoin = %s, user_freeze_fticoin = %s, user_withdraw_fancoin = %s, user_withdraw_commission = %s, user_recharge = %s, yichang = %s"
	try:
	   # 执行SQL语句
	   cursor.execute(sql,(user_id,user_fticoin,user_freeze_fticoin,user_withdraw_fancoin,user_withdraw_commission,user_recharge,yichang))
	   # 提交到数据库执行
	   db.commit()
	except:
	   # 发生错误时回滚
	   db.rollback()

	# 关闭数据库连接
	db.close()

def check():
	user_list = select_user_list()
	for user in user_list:
		user_id = user[0]
		user_fticoin = user[1]
		user_freeze_fticoin = user[2]

		recharge = get_recharge(user_id)
		if recharge[0][0]:
			user_recharge = recharge[0][0]
		else:
			user_recharge = decimal.Decimal.from_float(0.0000)

		user_withdraw = get_withdraw(user_id)
		if user_withdraw[0][0]:
			user_withdraw_fancoin = user_withdraw[0][0]
		else:	
			user_withdraw_fancoin = decimal.Decimal.from_float(0.0000)

		if user_withdraw[0][1]:
			user_withdraw_commission = user_withdraw[0][1]
		else:
			user_withdraw_commission = decimal.Decimal.from_float(0.0000)

		yichang = abs(user_fticoin+user_freeze_fticoin+user_withdraw_fancoin+user_withdraw_commission-user_recharge)

		if yichang==0.0000:
			continue
		else:
			print(user_id,user_fticoin,user_freeze_fticoin,user_withdraw_fancoin,user_withdraw_commission,user_recharge,yichang)

		add_yichang(user_id,user_fticoin,user_freeze_fticoin,user_withdraw_fancoin,user_withdraw_commission,user_recharge,yichang)

check()





