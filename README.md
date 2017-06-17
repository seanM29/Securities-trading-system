# Trading-system
* Do not change the original information
* 	pw = to_md5("123456")

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
* Trading-system: Our core project, You should push your modification here.
  * For front-end, you can add code in ./css, ./js, ./font, ./img, and add some html files
  * For back-end, your code should be added in ./src

<p></p>
<p></p>


* Template: Our referring Template, You should not change it.
  <p>If there's something you need, just copy it out</p>
