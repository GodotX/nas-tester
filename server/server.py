#!/usr/bin/env python

import socket, traceback
import curses, random, time
from pysqlite2 import dbapi2 as sqlite
import commands, os
import threading

#connect to the db
con = sqlite.connect('nas.db')
cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS hosts (o_id INTEGER PRIMARY KEY, ip VARCHAR(30), check_in CURRENT_TIMESTAMP)')
con.commit()

#init curses
#scr = curses.initscr()

host = ''
bcastport = 9700
cport = 9701
maxClients = 20

class bcastlistener(threading.Thread):
	global db
	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		s.bind((host, bcastport))
		while 1:
		
			message, address = s.recvfrom(8192)
			print "Got message from %s" % (address,)
			messageLock.acquire()
			#scr.addstr(cur_y, cur_x, "Got data from %s " % (address,))
			s.sendto("I am here", address)
			messageLock.release()
			#cur_y = cur_y + 1
			#scr.move(0,0)
			#scr.refresh()

class dbWriter(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(1)
	def run(self):
		print "help"
		
class work(threading.Thread):
	def __init__(self,clientsock):
		threading.Thread.__init__(self)
		self.myclientcon = clientsock
		self.setDaemon(1)
		self.start()
	def run(self):
		print self.myclientcon
		
		
messageLock = threading.Lock()
bcast_t = bcastlistener()
bcast_t.setDaemon(1)
bcast_t.start()
db_t = dbWriter().start()

lstn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lstn.bind((host, cport))
lstn.listen(maxClients)
for i in range(maxClients):
	(clientcon,ap) = lstn.accept()
	work(clientcon)




#try:
#	scr.nodelay(1)
#	scr.leaveok(0)
#	max_y, max_x = scr.getmaxyx()
#
#	cur_y = 0
#	cur_x = 0
#	scr.addstr(cur_y, cur_x, 'Press Ctrl-C to quit')
#	cur_y = cur_y + 1
	
#finally:
#	curses.endwin()
