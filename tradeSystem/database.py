#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import hashlib
def to_md5(name):
    id = hashlib.md5()
    id.update(name.encode("utf-8"))
    id = id.hexdigest()
    return id
DB_NAME = 'tradeSystem.db'
CONN = sqlite3.connect(DB_NAME, isolation_level=None, check_same_thread=False)
cur = CONN.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

###
#	about stock users
def __checkid(id, length=10):
	return id.isdigit() and ((not length) or len(id) == length)

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
	global __attrListStockUser
	ret = []
	for attr in __attrListStockUser:
		ret.append('NULL' if attr not in src else '"%s"' %(src[attr]))
	return ret

def __listToDictStockUser(src):
	global __attrListStockUser
	ret = {}
	i = 0
	for attr in __attrListStockUser:
		ret[attr] = src[i]
		i += 1
	return ret

def __insertStockUser(id, info):
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'
	info['id'] = id
	info['available'] = 1
	if 'create_time' in info:
		del info['create_time']

	s = __dictToListStockUser(info)
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
	id = str(id)
	if not __checkid(id):
		return 'Invalid stock user id'

	try:
		cur.execute("DELETE FROM StockUser where id == \"%s\"" %(id))
	except Exception as e:
		return str(e)
	else:
		return None

###
#	insert fund account
def __insertFundAccount(id, fund_id):
	id = str(id)
	fund_id = str(fund_id)
	if not __checkid(id):
		return "Invalid stock user id"
	if not __checkid(fund_id, length=None):
		return "Invalid fund id"

	try:
		cur.execute("INSERT INTO StockUserFund VALUES (\"%s\", \"%s\")" %(id, fund_id))
	except Exception as e:
		return str(e)
	else:
		return None

def __queryFundAccount(id):
	id = str(id)
	if not __checkid(id):
		return "invalid stock user id"

	cur.execute("SELECT * FROM StockUserFund where id == \"%s\"" %(id))
	res = cur.fetchall()
	res = [{'id': x[0], 'fund_id': x[1]} for x in res]
	return res

###
#	delete fund account
def __deleteFundAccount(id, fund_id):
	id = str(id)
	fund_id = str(fund_id)
	if not __checkid(id):
		return "Invalid stock user id"
	if not __checkid(fund_id):
		return "Invalid fund id"

	try:
		cur.execute("DELETE FROM StockUserFund where id == \"%s\" and fund_id == \"%s\"" %(id, fund_id))
	except Exception as e:
		return str(e)
	else:
		return None

###
#	get info of StockUserManager by id
#	including verify of id
def __queryStockUserManager(id):
	id = str(id)
	if not __checkid(id):
		return 'Invalid id'

	cur.execute("SELECT * FROM StockUserManager where id == \"%s\"" %(id))
	res = cur.fetchone()
	if not res:
		return 'Id does not exist'

	res = {'id': res[0], 'password': res[1], 'name': res[2]}
	return res

###
#	get info of StockQueryManager
def __queryStockQueryManager(id):
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

	ret['status'] = True
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
				DEFAULT CURRENT_TIMESTAMP,

			name nvarchar(64),
			sex integer
				CHECK (sex BETWEEN 0 AND 1),
			id_number char(18)
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
	cur.execute('''
		CREATE TABLE Stock(
			id char(10)
				REFERENCES StockUser (id)
					ON DELETE RESTRICT
					ON UPDATE CASCADE,
			stock_id integer
				CHECK (stock_id BETWEEN 0 AND 999999),

			own integer
				NOT NULL,
			frozen integer
				NOT NULL,

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
	pas=to_md5("123456")
	cur.execute("insert into StockUserManager values('3140103312','%s','')"%pas)
	cur.execute("insert into StockQueryManager values('3140103312','%s','','')" % pas)

def test1():
	t = {
		'id': '0123456789',
		'password': '01cd2d699991ea786acf871aa39646dd',
		'sex': 1,
		'degree': 3
	}
	print addStockUser(t['id'], t)

def test2():
	print addFundAccount('0123456789', 223489)
	print addFundAccount('0123456789', 2234839)
	print getStockUser('0123456789')
	print getFundAccount('0123456789')

def test3():
	print frozeStockUser('0123456789')
	print unfrozeStockUser('0123456789')
	print updStockUser('0123456789', {'degree': 3})

def testend():
	cur.execute("SELECT * FROM StockUser")
	print cur.fetchone()
	cur.execute("SELECT * FROM StockUserFund")
	print cur.fetchall()

	print sqlite3.sqlite_version

	delStockUser('0123456789')
	cur.execute("SELECT * FROM StockUser")
	print cur.fetchall()
	cur.execute("SELECT * FROM StockUserFund")
	print cur.fetchall()

if __name__ == "__main__":
	init()
	# test1()
	# test2()
	# test3()
	# testend()
