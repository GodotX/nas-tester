#!/usr/bin/env python

import time, socket, sys
dest = ('<broadcast>', 9700)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto("Hello", dest)
print "Looking for replys; press CTRL-C to stop."

s.settimeout(10.0)

try:
	(buf, address) = s.recvfrom(2048)
except socket.error, e:
	print "It %s. Retrying in 5 seconds..." % e
	time.sleep(5)
	s.settimeout(20.0)
	s.sendto("Hello", dest)
	try:
	    (buf, address) = s.recvfrom(2048)
	except socket.error, e:
		print "It %s. I quit." % e
		sys.exit(1)

print "Found server at %s:%s" % (address[0], address[1])
s.close

print "Opening TCP connection with server:"

dest = (address[0], 9701)
print "  \-Creating TCP socket... \t",

try: 
	TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, e:
	print "ERROR\n *** Problem sir: %s ***" % e
	sys.exit(1)

print "done."

print "  \-Connecting to server... \t",

try:
	TCPsock.connect(dest)
except socket.error, e:
	print "ERROR\n *** Problem sir: %s ***" % e[1]
	sys.exit(1)

print "done."
