import sqlite3

class DataBase:
	def __init__(self):
		self.conn = sqlite3.connect('database.sqlite')
		self.make_tables()

	def make_tables(self):
		cur = self.conn.cursor()
		cur.executescript("""
		CREATE TABLE IF NOT EXISTS valid_links(
			link TEXT
		);
		CREATE TABLE IF NOT EXISTS spam_links(
			link TEXT
		);
		CREATE TABLE IF NOT EXISTS unverified(
			link TEXT,
			given_id TEXT
		);
		CREATE TABLE IF NOT EXISTS member_status(
			id INTEGER,
			warning INTEGER
		);
		""")
		cur.close()
		self.conn.commit()

	#-----------------------------------------------
	def is_valid(self, link):      # complete
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM valid_links WHERE link = ?',(link, ))
		info = cur.fetchall()
		cur.close()
		return info != []

	def set_valid(self, link):  # return false mean its already in the list

		if(self.is_valid(link)):
			return False

		cur = self.conn.cursor()
		cur.execute('INSERT INTO valid_links VALUES(? )', (link, ))
		cur.close()
		self.conn.commit()

		return True

	def del_valid(self, link):

		if(self.is_valid(link)):
			cur = self.conn.cursor()
			cur.execute('DELETE FROM valid_links WHERE link=?', (link,) )
			cur.close()
			self.conn.commit()
			return True

		return False

	def show_valid(self):
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM valid_links')
		info = cur.fetchall()
		return info


	#-----------------------------------------------
	def is_spam(self, link):      # complete
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM spam_links WHERE link = ?',(link, ))
		info = cur.fetchall()
		cur.close()
		return info != []

	def set_spam(self, link):  # return false mean its already in the list

		if(self.is_spam(link)):
			return False

		cur = self.conn.cursor()
		cur.execute('INSERT INTO spam_links VALUES(? )', (link, ))
		cur.close()
		self.conn.commit()

		return True

	def del_spam(self, link):

		if(self.is_spam(link)):
			cur = self.conn.cursor()
			cur.execute('DELETE FROM spam_links WHERE link=?', (link,) )
			cur.close()
			self.conn.commit()
			return True

		return False

	def show_spam(self):
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM spam_links')
		info = cur.fetchall()
		return info


	#------------------------------------------------
	def is_unverified(self, link):      # complete
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM unverified WHERE link = ?',(link, ))
		info = cur.fetchall()
		cur.close()
		return info != []

	def set_unverified(self, link, id):   # complete
		id = str(id)
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM unverified WHERE link = ?',(link, ))
		info = cur.fetchall()
		if info==[]:
			cur.execute('INSERT INTO unverified VALUES( ?, ?)',(link, id, ))
		elif id not in info[0][1].split(','):
			cur.execute('UPDATE unverified set given_id=? WHERE link=?', ( info[0][1]+','+id,link,))
		cur.close()
		self.conn.commit()


	def del_unverified(self, link):
		
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM unverified WHERE link=?', (link, ))
		info = cur.fetchall()
		if info==[]:
			return False

		cur.execute('DELETE FROM unverified WHERE link=?', (link, ))
		self.conn.commit()

		return info[0][1].split(',')

	def get_unverified_link_sender(self, link):
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM unverified WHERE link=?', (link, ))
		info = cur.fetchall()

		if info == []:
			return False
		return info[0][1].split(',')



	def show_unverified(self):
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM unverified')
		info = cur.fetchall()
		return info




	#----------------------------------------------------
	def update_warning(self, id):
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM member_status WHERE id=? ',(id, ))
		info = cur.fetchall()
		warning = 1

		if info==[]:
			cur.execute('INSERT INTO member_status VALUES( ?, ?)',(id,  warning, ))
		else:
			warning = info[0][1] + 1
			cur.execute('''UPDATE member_status SET warning = ? WHERE id= ? ''', ( warning, id,) )

		cur.close()
		self.conn.commit()
		return warning

	def check_warning(self, id):
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM member_status WHERE id=?',(id, ))
		info = cur.fetchall()
		cur.close()
		if info==[]:return 0
		return info[0][1]


	def del_warning(self, id):
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM member_status WHERE id=?',(id, ))
		info = cur.fetchall()
		if info==[]:
			cur.close()
			return False

		cur.execute('DELETE FROM member_status WHERE id = ?', (id, ))
		cur.close()
		self.conn.commit()
		return True


	def show_member(self):
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM member_status')
		info = cur.fetchall()
		return info

