import socket
from pymongo import MongoClient
from time import clock

def find(url, col, times, ran):
	x = []
	f = open(url)
	for i in f:
		x.append({"url":i})
	
	start = clock()
	for i in range(times):
		col.find(x[i])
		print "db.table.findOne({\"url\"}:\"",x[i],"\")"
	end = clock()
	time = end - start
	print "\tAverage number of seconds to run all queries: " + str(time) + " seconds"
	print "\tMinimum number of seconds to run all queries: " + str(time) + " seconds"
	print "\tMaximum number of seconds to run all queries: " + str(time) + " seconds"
	print "\tNumber of clients running queries: 1"
	print "\tAverage number of queries per client: ",str(times)

	f.close()


if __name__ == '__main__':
	conn = MongoClient('localhost')
	db = conn.html
	col = db.table
	#insert('data.json', col)
	
	s = socket.socket()

	host = socket.gethostname()
	port = 6672
	s.bind((host,port))

	s.listen(5)

	while True:
		c,addr = s.accept()
		print 'Got connection from', addr
		c.close()
		break
		
	find('url', col, 20, 200)
	s.close()

