#!/usr/bin/env python

import socket, traceback
import curses, random, time

scr = curses.initscr()

host = ''
port = 51432

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

try:
	scr.nodelay(1)
	scr.leaveok(0)
	max_y, max_x = scr.getmaxyx()

	cur_y = 0
	cur_x = 0
	scr.addstr(cur_y, cur_x, 'Press Ctrl-C to quit')
	cur_y = cur_y + 1
	while 1:
		c = scr.getch()
		if c == ord('q'): break
		message, address = s.recvfrom(8192)
		scr.addstr(cur_y, cur_x, "Got data from %s " % (address,))
		s.sendto("I am here", address)
		cur_y = cur_y + 1
		scr.move(0,0)
		scr.refresh()
finally:
	curses.endwin()
