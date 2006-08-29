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


class bcastlistener(threading.Thread):
	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		s.bind((host, bcastport))
		while 1:
		
			message, address = s.recvfrom(8192)
			print "Got message from %s" % (address,)
			#scr.addstr(cur_y, cur_x, "Got data from %s " % (address,))
			s.sendto("I am here", address)
			#cur_y = cur_y + 1
			#scr.move(0,0)
			#scr.refresh()
bcastlistener().start()
while 1:
	print "doing something else"
	time.sleep(random.randint(10, 100) / 1000.0)




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
