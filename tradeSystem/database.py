#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sqlite3
import hashlib

DB_NAME = 'tradeSystem.db'
CONN = None
cur = None

ERROR_MESSAGE = {
	'Froze amount is not a int': ['股票交易数量必须为整数'],
	'Frozed amount must be positive': ['股票交易数量必须大于零'],
	'Id does not exist': ['ID 不存在'],
	'Id exist': ['账户已存在'],
	'Incorrect password': ['密码有误'],
	'Invalid amount': ['交易数量必须为整数'],
	'Invalid id': ['账户格式不合法'],
	'Invalid stock id': ['股票代码格式不合法'],
	'Invalid stock user id': ['证券账户格式不合法'],
	'Moved amount is not a int': ['股票交易数量必须为整数'],
	'Moved amount must be positive': ['股票交易数量必须大于零'],
	'Stock does not exist': ['股票不存在'],
	'Stock user is already frozen': ['该证券账户已被挂失'],
	'Stock user is not frozen': ['该证券账户未挂失'],

	'Field %(field)s could not be empty': ['%(field)s不能为空'],
	'%(field)s is invalid': ['%(field)s不合法'],
	'%(field)s alreadly exist': ['%(field)s已存在'],

	'This user still own some stocks': ['该用户仍持有证券资产']
}
ERROR_FIELD = {
	'StockUser.id': ['stock user id', '证券账户'],
	'StockUser.available': ['available', '账户可用性'],
	'StockUser.password': ['password', '密码'],
	'StockUser.create_time': ['create time', '账户创建时间'],
	'StockUser.name': ['name', '姓名'],
	'StockUser.sex': ['sex', '性别'],
	'StockUser.id_number': ['id number', '身份证号码'],
	'StockUser.mobilephone': ['mobilephone', '手机号'],
	'StockUser.telephone': ['telephone', '座机号'],
	'StockUser.home_address': ['home address', '家庭地址'],
	'StockUser.degree': ['degree', '学历'],
	'StockUser.job': ['jog', '职业'],
	'StockUser.work_address': ['work address', '工作地址'],
	'StockUserFund.id': ['stock user id', '证券账户'],
	'StockUserFund.fund_id': ['fund id', '资金账户'],
	'Stock.id': ['stock user id', '证券账户'],
	'Stock.stock_id': ['fund id', '股票代码'],
	'Stock.own': ['own', '持有股票数量'],
	'Stock.frozen': ['frozen', '冻结股票数量'],
	'StockUserManager.id': ['id', '证券管理账户'],
	'StockUserManager.password': ['password', '密码'],
	'StockUserManager.name': ['name', '姓名'],
	'StockQueryManager.id': ['id', '交易管理账户'],
	'StockQueryManager.password': ['password', '密码'],
	'StockQueryManager.type': ['type', '权限类型'],
	'StockQueryManager.name': ['name', '姓名']
}
ERROR_LANG = 1 # [0: eng, 1: chs]

def __checkErrmsg(msg):
	if not isinstance(msg, str):
		return msg

	dt = {}
	if msg.find('NOT NULL constraint failed:') == 0:
		dt['field'] = msg[msg.find(':') + 2 :]
		msg = 'Field %(field)s could not be empty'
	if msg.find('CHECK constraint failed:') == 0:
		dt['field'] = msg[msg.find(':') + 2 :]
		msg = '%(field)s is invalid'
	if msg.find('UNIQUE constraint failed:') == 0:
		dt['field'] = msg[msg.find(':') + 2 :]
		msg = '%(field)s alreadly exist'
	if msg.find('FOREIGN KEY constraint failed') == 0:
		msg = 'This user still own some stocks'

	if 0 < ERROR_LANG < 2 and msg in ERROR_MESSAGE:
		msg = ERROR_MESSAGE[msg][ERROR_LANG - 1]

	if 'field' in dt:
		dt['field'] = dt['field'].replace('$', '.')
		if dt['field'] in ERROR_FIELD:
			dt['field'] = ERROR_FIELD[dt['field']][ERROR_LANG]
	return msg % dt

def __checkReturnValue(func):
	def __func(*args, **kwargs):
		ret = func(*args, **kwargs)
		ret['error'] = __checkErrmsg(ret['error'])
		return ret
	return __func

def to_md5(name):
    id = hashlib.md5()
    id.update(name.encode("utf-8"))
    id = id.hexdigest()
    return id

def __checkid(id, length=10):
	"""Check whether id is consisted of digits

	Args:
		id: id of the stock user
		length: expected length. Set it to None when there is no requirement of length
	
	Return:
		bool: True for valid
	"""
	return id.isdigit() and ((not length) or len(id) == length)

def __checkint(num, low=None, high=None):
	try:
		num = int(num)
	except:
		return False
	else:
		return (low is None or low <= num) and (high is None or num <= high)

# rows of table StockUser
__attrListStockUser = (
	'id',
	'available',
	'password',
	'create_time',
	'name',
	'sex',
	'id_number',
	'mobilephone',
	'telephone',
	'home_address',
	'degree',
	'job',
	'work_address'
)

def __dictToListStockUser(src):
	"""Convert a dict of rows of StockUser to list

	Args:
		src: a dict represent a row of StockUser
	
	Return:
		list: a list represent the row of StockUser
	"""
	global __attrListStockUser
	ret = []
	for attr in __attrListStockUser:
		ret.append('NULL' if attr not in src else '"%s"' %(src[attr]))
	return ret

def __listToDictStockUser(src):
	"""Convert a list of rows of StockUser to dict

	Args:
		src: a list represent a row of StockUser
	
	Return:
		list: a dict represent the row of StockUser
	"""
	global __attrListStockUser
	ret = {}
	i = 0
	for attr in __attrListStockUser:
		ret[attr] = src[i]
		i += 1
	return ret

def __insertStockUser(id, info):
	"""Insert a row into StockUser

	Args:
		id: id of the stock user
		info: info of the stock user
	
	Return:
		None: success
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'
	info['id'] = id
	info['available'] = 1
	if 'create_time' in info:
		del info['create_time']

	s = __dictToListStockUser(info)
	s[3] = 'CURRENT_TIMESTAMP'
	try:
		cur.execute("INSERT INTO Stockuser VALUES (%s)" %(','.join(s)))
	except Exception as e:
		return str(e)
	else:
		return None

def __updateStockUser(id, info):
	"""Update a row into StockUser

	Args:
		id: id of the stock user
		info: info of the stock user which need to be updated
	
	Return:
		None: success
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'
	if 'id' in info:
		del info['id']
	if 'create_time' in info:
		del info['create_time']

	s = __dictToListStockUser(info)
	sx = ""
	i = 0
	for attr in __attrListStockUser:
		if attr in info:
			sx += attr + ' = ' + s[i] + ', '
		i += 1
	if len(sx) > 0:
		sx = sx[: -2]

	try:
		cur.execute("UPDATE Stockuser SET %s WHERE id == \"%s\"" %(sx, id))
	except Exception as e:
		return str(e)
	else:
		return None

def __queryStockUser(id):
	"""Query a row into StockUser by id

	Args:
		id: id of the stock user
	
	Return:
		dict: the selected row
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'

	cur.execute("SELECT * FROM StockUser where id == \"%s\"" %(id))
	res = cur.fetchone()
	if not res:
		return 'Id does not exist'

	res = __listToDictStockUser(list(res))
	return res

def __deleteStockUser(id):
	"""Delete a row from StockUser

	Args:
		id: id of the stock user
	
	Return:
		None: success
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'

	try:
		cur.execute("DELETE FROM StockUser where id == \"%s\"" %(id))
	except Exception as e:
		return str(e)
	else:
		return None

def __insertFundAccount(id, fund_id):
	"""Insert a row into FundAccount

	Args:
		id: id of the stock user
		fund_id: id of the fund account
	
	Return:
		None: success
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'

	try:
		cur.execute("INSERT INTO StockUserFund VALUES (\"%s\", \"%s\")" %(id, fund_id))
	except Exception as e:
		return str(e)
	else:
		return None

def __queryFundAccount(id):
	"""Query rows of FundAccount by id

	Args:
		id: id of the stock user
	
	Return:
		list: select fund accounts from FundAccount
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'

	cur.execute("SELECT * FROM StockUserFund where id == \"%s\"" %(id))
	res = cur.fetchall()
	res = [{'id': x[0], 'fund_id': x[1]} for x in res]
	return res

def __deleteFundAccount(id, fund_id):
	"""Delete a row from FundAccount

	Args:
		id: id of the stock user
		info: id of the fund account
	
	Return:
		None: success
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'

	try:
		cur.execute("DELETE FROM StockUserFund where id == \"%s\" and fund_id == \"%s\"" %(id, fund_id))
	except Exception as e:
		return str(e)
	else:
		return None

def __updateStock(id, stock_id, own, frozen):
	"""Insert a row into Stocks

	Args:
		id: id of the stock user
		stock_id: id of the fund account
		amount: number of gained stocks
		frozen: number of frozen stocks
	
	Return:
		None: success
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'
	if not __checkint(stock_id, 0, 999999):
		return 'Invalid stock id'
	stock_id = int(stock_id)
	if not __checkint(own, None, None):
		return 'Invalid amount'
	own = int(own)
	if not __checkint(frozen, None, None):
		return 'Invalid amount'
	frozen = int(frozen)

	stock = __queryStock(id, stock_id)
	try:
		if isinstance(stock, str):	# not exist
			cur.execute("INSERT INTO Stock VALUES (\"%s\", %d, %d, %d)" %(id, stock_id, own, frozen))
		else:
			if own + stock['own'] == 0:
				cur.execute("DELETE FROM Stock WHERE id == \"%s\" and stock_id == %d" %(id, stock_id))
			else:
				cur.execute("UPDATE Stock SET own = own + %d, frozen = frozen + %d WHERE id == \"%s\" and stock_id == %d" %(own, frozen, id, stock_id))
	except Exception as e:
		return str(e)
	else:
		return None

def __queryStock(id, stock_id):
	"""Query row of Stocks by id and stock id

	Args:
		id: id of the stock user
		stock_id: id of the stock

	Return:
		dict: select stock from Stock
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'
	if not __checkint(stock_id, 0, 999999):
		return 'Invalid stock id'
	stock_id = int(stock_id)

	cur.execute("SELECT * FROM Stock WHERE id == \"%s\" and stock_id == %d" % (id, stock_id))
	res = cur.fetchone()
	if not res:
		return 'Stock does not exist'
	res = {'id': res[0], 'stock_id': res[1], 'own': res[2], 'frozen': res[3]}
	return res

def __queryStocks(id):
	"""Query rows of Stocks by id

	Args:
		id: id of the stock user

	Return:
		list: select stocks from Stock
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'

	cur.execute("SELECT * FROM Stock WHERE id == \"%s\"" % (id))
	res = cur.fetchall()
	res = [{'id': x[0], 'stock_id': x[1], 'own': x[2], 'frozen': x[3]} for x in res]
	return res

def __queryStockUserManager(id):
	"""Query a row of StockUserManager

	Args:
		id: id of the stock user manager
	
	Return:
		dict: manager info
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid id'

	cur.execute("SELECT * FROM StockUserManager where id == \"%s\"" %(id))
	res = cur.fetchone()
	if not res:
		return 'Id does not exist'

	res = {'id': res[0], 'password': res[1], 'name': res[2]}
	return res

def __queryStockQueryManager(id):
	"""Query a row of StockQueryManager

	Args:
		id: id of the stock query manager
	
	Return:
		dict: manager info
		string: error message
	"""
	id = str(id)
	if not __checkid(id):
		return 'Invalid id'

	cur.execute("SELECT * FROM StockQueryManager where id == \"%s\"" %(id))
	res = cur.fetchone()
	if not res:
		return 'Id does not exist'

	res = {'id': res[0], 'password': res[1], 'type': res[2], 'name': res[3]}
	return res

################################################################################

@__checkReturnValue
def addStockUser(id, info):
	"""Add a stock user

	Args:
		id: id of the new stock user
		info: other infomations about the user
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = {'status': False, 'error': None}

	res = __insertStockUser(id, info)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	CONN.commit()
	ret['status'] = True
	return ret

@__checkReturnValue
def updStockUser(id, info):
	"""Update the infomation of a stock user

	Args:
		id: id of the stock user
		info: infomation need to be updated
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = {'status': False, 'error': None}

	if 'available' in info:
		del info['available']
	res = __updateStockUser(id, info)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	CONN.commit()
	ret['status'] = True
	return ret

@__checkReturnValue
def getStockUser(id):
	"""Get the infomation of a stock user

	Args:
		id: id of the stock user
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
		'result': user info
	"""
	ret = {'status': False, 'error': None, 'result': None}

	res = __queryStockUser(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	fund = __queryFundAccount(id)
	if isinstance(fund, str):
		ret['error'] = fund
		return ret

	res['fund'] = fund
	ret['status'] = True
	ret['result'] = res
	return ret

@__checkReturnValue
def loginStockUser(id, password):
	"""Login into the system

	Args:
		id: id of the stock user
		password: user password
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = getStockUser(id)
	if not ret['status']:
		return ret

	same = ret['result']['password'] == password
	del ret['result']
	if not same:
		ret['status'] = False
		ret['error'] = 'Incorrect password'
		return ret

	return ret

@__checkReturnValue
def delStockUser(id):
	"""Delete stock user

	Args:
		id: id of the stock user
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = {'status': False, 'error': None}

	res = __deleteStockUser(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	CONN.commit()
	ret['status'] = True
	return ret

@__checkReturnValue
def frozeStockUser(id):
	"""Froze a stock user

	Args:
		id: id of the stock user
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = {'status': False, 'error': None}

	res = __queryStockUser(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	if res['available'] == 0:
		ret['error'] = 'Stock user is already frozen'
		return ret

	__updateStockUser(id, {'available': 0})
	CONN.commit()
	ret['status'] = True
	return ret

@__checkReturnValue
def unfrozeStockUser(id):
	"""Unfroze a stock user

	Args:
		id: id of the stock user
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = {'status': False, 'error': None}

	res = __queryStockUser(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	if res['available'] == 1:
		ret['error'] = 'Stock user is not frozen'
		return ret

	__updateStockUser(id, {'available': 1})
	CONN.commit()
	ret['status'] = True
	return ret

@__checkReturnValue
def addFundAccount(id, fund_id):
	"""Add a fund account to a stock user

	Args:
		id: id of the stock user
		fund_id: if of a fund account
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = {'status': False, 'error': None}

	res = __insertFundAccount(id, fund_id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	CONN.commit()
	ret['status'] = True
	return ret

@__checkReturnValue
def getFundAccount(id):
	"""Get fund accounts of a stock user

	Args:
		id: id of the stock user
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
		'result': fund accounts of a stock user
	"""
	ret = {'status': False, 'error': None, 'result': None}

	res = __queryFundAccount(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	ret['status'] = True
	ret['result'] = res
	return ret

@__checkReturnValue
def delFundAccount(id, fund_id):
	"""Delete a fund account

	Args:
		id: id of the stock user
		fund_id: if of the fund account
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = {'status': False, 'error': None}

	res = __deleteFundAccount(id, fund_id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	CONN.commit()
	ret['status'] = True
	return ret

@__checkReturnValue
def frozeStock(id, stock_id, amount):
	"""Froze shares of a stock of a stock user

	Args:
		id: id of the stock user
		stock_id: id of the stock
		amount: the frozed amount

	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = {'status': False, 'error': None}

	if not __checkint(amount):
		ret['error'] = 'Froze amount is not a int'
		return ret
	amount = int(amount)

	if amount <= 0:
		ret['error'] = 'Frozed amount must be positive'
		return ret

	res = __updateStock(id, stock_id, 0, amount)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	CONN.commit()
	ret['status'] = True
	return ret

@__checkReturnValue
def mvStock(id_1, id_2, stock_id, amount):
	"""move frozed shares of a stock between two stock users

	Args:
		id_1: id of the seller
		id_2: id of the buyer
		stock_id: id of the stock
		amount: the frozed amount

	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = {'status': False, 'error': None}

	if not __checkint(amount):
		ret['error'] = 'Moved amount is not a int'
		return ret
	amount = int(amount)

	if amount <= 0:
		ret['error'] = 'Moved amount must be positive'
		return ret

	res = __updateStock(id_1, stock_id, -amount, -amount)
	if isinstance(res, str):
		ret['error'] = res
		return ret
	res = __updateStock(id_2, stock_id, amount, 0)
	if isinstance(res, str):
		CONN.rollback()
		ret['error'] = res
		return ret

	CONN.commit()
	ret['status'] = True
	return ret

@__checkReturnValue
def getStocks(id):
	"""Get stocks of a stock user

	Args:
		id: id of the stock user

	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
		'result': Stocks of a stock user
	"""
	ret = {'status': False, 'error': None, 'result': None}

	res = __queryStocks(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	ret['status'] = True
	ret['result'] = res
	return ret

@__checkReturnValue
def loginStockUserManager(id, password):
	"""Login into the system as a user manager

	Args:
		id: id of the user manager
		password: password of the manager
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = {'status': False, 'error': None}

	res = __queryStockUserManager(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret
	if res['password'] != password:
		ret['error'] = 'Incorrect password'
		return ret

	ret['status'] = True
	return ret

@__checkReturnValue
def getStockQueryManager(id):
	"""Get the infomation of a stock query manager

	Args:
		id: id of the stock query manager
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
		'result': user info
	"""
	ret = {'status': False, 'error': None, 'result': None}

	res = __queryStockQueryManager(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	ret['status'] = True
	ret['result'] = res
	return ret

@__checkReturnValue
def loginStockQueryManager(id, password):
	"""Login into the system as a query manager

	Args:
		id: id of the query manager
		password: password of the manager
	
	Return:
		A dict mapping keys include:
		'status': True or False. The result of operation.
		'error': Error message when 'status'=False
	"""
	ret = getStockQueryManager(id)
	if not ret['status']:
		return ret

	same = ret['result']['password'] == password
	del ret['result']
	if not same:
		ret['status'] = False
		ret['error'] = 'Incorrect password'
		return ret

	return ret

def __connect():
	global CONN, cur
	CONN = sqlite3.connect(DB_NAME, isolation_level='EXCLUSIVE', check_same_thread=False)
	cur = CONN.cursor()
	cur.execute("PRAGMA foreign_keys = ON;")

def init():
	"""Initialize database tables
	"""

	cur.execute('''
		CREATE TABLE StockUser (
			id char(10),
			available integer
				NOT NULL,
			password char(32)
				NOT NULL,

			create_time timestamp
				NOT NULL
				DEFAULT (datetime('now', 'localtime')),

			name nvarchar(64)
				NOT NULL,
			sex integer
				NO TNULL,
			id_number char(18)
				NOT NULL
				UNIQUE,
			mobilephone varchar(20)
				NOT NULL,
			telephone varchar(20),
			home_address nvarchar(256)
				NOT NULL,
			degree integer,
			job nvarchar(64)
				NOT NULL,
			work_address nvarchar(256)
				NOT NULL,

			CONSTRAINT StockUser$available CHECK (available BETWEEN 0 AND 1),
			CONSTRAINT StockUser$sex CHECK (sex BETWEEN 0 AND 1),
			CONSTRAINT StockUser$id_number CHECK (length(id_number) == 18),
			CONSTRAINT StockUser$degree CHECK (degree BETWEEN 0 AND 5),
			PRIMARY KEY (id)
		);''')
	cur.execute('''
		CREATE TABLE StockUserFund(
			id char(10),
			fund_id varchar(20)
				UNIQUE,

			CONSTRAINT StockUserFund$id FOREIGN KEY (id)
				REFERENCES StockUser (id)
					ON DELETE CASCADE
					ON UPDATE CASCADE,
			PRIMARY KEY (id, fund_id)
		);''')
	# frozen is part of own
	cur.execute('''
		CREATE TABLE Stock(
			id char(10),
			stock_id integer,

			own integer
				NOT NULL,
			frozen integer
				NOT NULL,

			CONSTRAINT Stock$stock_id CHECK (stock_id BETWEEN 0 AND 999999),
			CONSTRAINT Stock$own CHECK (own > 0 and own >= frozen),
			CONSTRAINT Stock$frozen CHECK (frozen >= 0),
			CONSTRAINT Stock$id FOREIGN KEY (id)
				REFERENCES StockUser (id)
					ON DELETE RESTRICT
					ON UPDATE CASCADE,
			PRIMARY KEY (id, stock_id)
		);''')
	cur.execute('''
		CREATE TABLE StockUserManager(
			id char(10),
			password char(32)
				NOT NULL,

			name nvarchar(64),

			PRIMARY KEY (id)
		);''')
	cur.execute('''
		CREATE TABLE StockQueryManager(
			id char(10),
			password char(32)
				NOT NULL,

			type nvarchar(256),
			name nvarchar(64),

			PRIMARY KEY (id)
		);''')

	pw = to_md5("123456")

	cur.execute("INSERT INTO StockUserManager VALUES ('3140103312', '%s', '')" % pw)

	cur.execute("INSERT INTO StockQueryManager VALUES ('3140102265', '%s', '房地产', 'sDong')" % pw)
	cur.execute("INSERT INTO StockQueryManager VALUES ('3140103312', '%s', '能源', 'jlLu')" % pw)
	cur.execute("INSERT INTO StockQueryManager VALUES ('3140109999', '%s', '数据挖坑', 'Ajanda')" % pw)

	addStockUser("1706140001", {
								'password': pw,
								'sex': '1',
								'degree': '1',
								'name': 'Kosaka Honoka',
								'id_number': '330101200108030000',
								'mobilephone': '12333333333',
								'home_address': 'XXX',
								'job': 'idol',
								'work_address': 'XXX'})
	addStockUser("1706140002", {
								'password': pw,
								'sex': '1',
								'degree': '2',
								'name': 'Nitta Emi',
								'id_number': '330101198512100000',
								'mobilephone': '12333333333',
								'home_address': 'XXX',
								'job': 'singer',
								'work_address': 'XXX'})

	addFundAccount('1706140001', '1001')
	addFundAccount('1706140002', '1002')

	cur.execute('INSERT INTO Stock VALUES (\"1706140001\", 170001, 1000, 0)')
	cur.execute('INSERT INTO Stock VALUES (\"1706140002\", 170002, 1000, 0)')

	CONN.commit()

if __name__ == "__main__":
	os.remove('tradeSystem.db')
	__connect()
	init()
	exit(0)

__connect()
