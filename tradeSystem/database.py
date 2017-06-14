#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import hashlib

DB_NAME = 'tradeSystem.db'
CONN = sqlite3.connect(DB_NAME, isolation_level='EXCLUSIVE', check_same_thread=False)
cur = CONN.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

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

def __checkint(num, low, high):
	if not (isinstance(num, int) or str(num).isdigit()):
		return False
	num = int(num)
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
		e = str(e)
		if e[: 6] == 'UNIQUE':
			e = 'Id exist'
		return e
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
	fund_id = str(fund_id)
	if not __checkid(id):
		return 'Invalid stock user id'
	if not __checkid(fund_id, length=None):
		return 'Invalid fund id'

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
		return 'invalid stock user id'

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
	fund_id = str(fund_id)
	if not __checkid(id):
		return "Invalid stock user id"
	if not __checkid(fund_id, length=None):
		return "Invalid fund id"

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
		return "invalid stock user id"
	if not __checkint(stock_id, 0, 999999):
		return 'Invalid stock id'
	stock_id = int(stock_id)

	cur.execute("SELECT * FROM Stock WHERE id == \"%s\" and stock_id == %d" % (id, stock_id))
	res = cur.fetchone()
	if not res:
		return 'stock does not exist'
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
		return "invalid stock user id"

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
		return "invalid id"

	cur.execute("SELECT * FROM StockQueryManager where id == \"%s\"" %(id))
	res = cur.fetchone()
	if not res:
		return "id not exist"

	res = {'id': res[0], 'password': res[1], 'type': res[2], 'name': res[3]}
	return res

################################################################################

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
	ret = {'status': False, 'error': None}
	res = __queryStockQueryManager(id)

	if isinstance(res, str):
		ret['error'] = res
		return ret
	if res['password'] != password:
		ret['error'] = 'Incorrect password'
		return ret

	ret['status'] = True
	return ret

###
#	initialization
def init():
	"""Initialize database tables
	"""
	cur = CONN.cursor()

	cur.execute('''
		CREATE TABLE StockUser (
			id char(10),
			available integer
				NOT NULL
				CHECK (available BETWEEN 0 AND 1),
			password char(32)
				NOT NULL,

			create_time timestamp
				NOT NULL
				DEFAULT (datetime('now', 'localtime')),

			name nvarchar(64)
				NOT NULL,
			sex integer
				CHECK (sex BETWEEN 0 AND 1),
			id_number char(18)
				NOT NULL
				UNIQUE,
			mobilephone varchar(20),
			telephone varchar(20),
			home_address nvarchar(256),
			degree integer
				CHECK (degree BETWEEN 0 AND 5),
			job nvarchar(64),
			work_address nvarchar(256),

			PRIMARY KEY (id)
		);''')
	cur.execute('''
		CREATE TABLE StockUserFund(
			id char(10)
				REFERENCES StockUser (id)
					ON DELETE CASCADE
					ON UPDATE CASCADE,
			fund_id varchar(20)
				UNIQUE,

			PRIMARY KEY (id, fund_id)
		);''')
	# frozen is part of own
	cur.execute('''
		CREATE TABLE Stock(
			id char(10)
				REFERENCES StockUser (id)
					ON DELETE RESTRICT
					ON UPDATE CASCADE,
			stock_id integer
				CHECK (stock_id BETWEEN 0 AND 999999),

			own integer
				NOT NULL
				CHECK (own > 0),
			frozen integer
				NOT NULL
				CHECK (frozen >= 0),

			PRIMARY KEY (id, stock_id),
			CHECK (frozen <= own)
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
	cur.execute("INSERT INTO StockQueryManager VALUES ('3140103312', '%s', '', '')" % pw)

	addStockUser("1706140001", {
								'password': pw,
								'sex': 1,
								'degree': 1,
								'name': 'Kosaka Honoka',
								'id_number': '330101200108030000'})
	addStockUser("1706140002", {
								'password': pw,
								'sex': 1,
								'degree': 2,
								'name': 'Nitta Emi',
								'id_number': '330101198512100000'})

	addFundAccount("1706140001", 1001)
	addFundAccount("1706140002", 1002)

	cur.execute("INSERT INTO Stock VALUES (\"1706140001\", 170001, 1000, 0)")
	cur.execute("INSERT INTO Stock VALUES (\"1706140002\", 170002, 1000, 0)")

	CONN.commit()

def test1():
	t = {
		'id': '0123456789',
		'password': '01cd2d699991ea786acf871aa39646dd',
		'sex': 1,
		'degree': 3
	}
	print addStockUser(t['id'], t)
	print addStockUser('1111111111', {'password': '01cd2d699991ea786acf871aa39646dd'})

def test2():
	print addFundAccount('0123456789', 223489)
	print addFundAccount('0123456789', 2234839)
	print addFundAccount('1111111111', 2234839)
	print getStockUser('0123456789')
	print getFundAccount('0123456789')

def test3():
	print frozeStockUser('0123456789')
	print unfrozeStockUser('0123456789')
	print updStockUser('0123456789', {'degree': 3})

def test_stockExchange():
	cur.execute("SELECT * FROM StockUser")
	print cur.fetchall()
	cur.execute("SELECT * FROM StockUserFund")
	print cur.fetchall()
	cur.execute("SELECT * FROM Stock")
	print cur.fetchall()

	print frozeStock('1706140001', 170001, 500)
	cur.execute("SELECT * FROM Stock")
	print cur.fetchall()

	print mvStock('1706140001', '1706140002', 170001, 500)
	cur.execute("SELECT * FROM Stock")
	print cur.fetchall()

def testend():
	cur.execute("SELECT * FROM StockUser")
	print cur.fetchall()
	cur.execute("SELECT * FROM StockUserFund")
	print cur.fetchall()

	print sqlite3.sqlite_version

	delStockUser('0123456789')
	delStockUser('1111111111')
	cur.execute("SELECT * FROM StockUser")
	print cur.fetchall()
	cur.execute("SELECT * FROM StockUserFund")
	print cur.fetchall()

if __name__ == "__main__":
#	init()
#	test_addUser()
#	test_fundAccount()
#	test_froze()
	test_stockExchange()
#	testend()

