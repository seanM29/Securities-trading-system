#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3

DB_NAME = '../../tradeSystem.db'
CONN = sqlite3.connect(DB_NAME, isolation_level=None)
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
	print ','.join(s)
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
	if 'available' in info:
		del info['available']
	if 'create_time' in info:
		del info['create_time']

	s = __dictToListStockUser(info)
	sx = ""
	i = 0
	for attr in __attrListStockUser:
		if s[i]:
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
		print e
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
	if not __checkid(fun_id):
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

###
#	add stock account
#	return:	{'status', 'error'}
def addStockUser(id, info):
	ret = {'status': False, 'error': None}

	res = __insertStockUser(id, info)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	ret['status'] = True
	return ret

###
#	update stock account
def updStockUser(id, info):
	ret = {'status': False, 'error': None}

	res = __updateStockUser(id, info)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	ret['status'] = True
	return ret

###
#	get stock user info by id
#	return:	{'status', 'error', 'result'}
def getStockUser(id):
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

###
#	login check
#	return:	{'status', 'error'}
def loginStockUser(id, password):
	ret = getStockUser(id)
	if not ret['status']:
		return ret

	same = res['result']['password'] != password
	del res['result']
	if not same:
		ret['status'] = False
		ret['error'] = 'Incorrect password'
		return ret

	return ret

###
#	delete stock account
#	return:	{'status', 'error'}
def delStockUser(id):
	ret = {'status': False, 'error': None}

	res = __deleteStockUser(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	ret['status'] = True
	return ret

###
#	froze stock account
#	return:	{'status', 'error'}
def frozeStockUser(id):
	ret = {'status': False, 'error': None}

	res = __queryStockUser(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	if not res['available']:
		ret['error'] = 'Stock user is already frozen'
		return ret

	__updateStockUser(id, {'available': 0})
	ret['status'] = True
	return ret

###
#	unfroze stock account
#	return:	{'status', 'error'}
def unfrozeStockUser(id):
	ret = {'status': False, 'error': None}

	res = __queryStockUser(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	if not res['available']:
		ret['error'] = 'Stock user is not frozen'
		return ret

	__updateStockUser(id, {'available': 1})
	ret['status'] = True
	return ret

###
#	add fund account
#	return:	{'status', 'error'}
def addFundAccount(id, fund_id):
	ret = {'status': False, 'error': None}

	res = __insertFundAccount(id, fund_id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	ret['status'] = True
	return ret

###
#	get fund accounts
#	return:	{'status', 'error', 'result'}
def getFundAccount(id, fund_id):
	ret = {'status': False, 'error': None, 'result': None}

	res = __queryFundAccount(id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	ret['status'] = True
	ret['result'] = res
	return ret

###
#	delete fund account
#	return:	{'status', 'error'}
def delFundAccount(id, fund_id):
	ret = {'status': False, 'error': None}

	res = __deleteFundAccount(id, fund_id)
	if isinstance(res, str):
		ret['error'] = res
		return ret

	ret['status'] = True
	return ret

###
#	login check
#	return:	{'status', 'error'}
def loginStockUserManager(id, password):
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

###
#	login check
#	return:	{'status', 'error'}
def loginStockQueryManager(id, password):
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
			id_number char(18),
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

			own integer NOT NULL,
			frozen integer NOT NULL,

			PRIMARY KEY (id, stock_id)
		);''')
	cur.execute('''
		CREATE TABLE StockUserManager(
			id char(10),
			password char(32) NOT NULL,

			name nvarchar(64),

			PRIMARY KEY (id)
		);''')
	cur.execute('''
		CREATE TABLE StockQueryManager(
			id char(10),
			password char(32) NOT NULL,

			type nvarchar(256),
			name nvarchar(64),

			PRIMARY KEY (id)
		);''')


def testUser():
	user = {}

def test1():
	t = {
		'id': '0123456789',
		'password': '01cd2d699991ea786acf871aa39646dd',
		'sex': 1
	}
	print addStockUser(t['id'], t)


def test2():
	print addFundAccount('0123456789', 223489)
	print addFundAccount('0123456789', 2234839)

if __name__ == "__main__":
#	init()
	test1()
	test2()

	cur.execute("SELECT * FROM StockUser")
	print cur.fetchone()
	cur.execute("SELECT * FROM StockUserFund")
	print cur.fetchall()

	print getStockUser('0123456789')
	print sqlite3.sqlite_version

	delStockUser('0123456789')
	cur.execute("SELECT * FROM StockUser")
	print cur.fetchall()
	cur.execute("SELECT * FROM StockUserFund")
	print cur.fetchall()

