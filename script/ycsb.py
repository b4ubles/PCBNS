#!/usr/bin/python

import threading
import time
import os
import sys

def record( threadName, delay):
   while t1.isAlive():
      time.sleep(delay)
      os.system(rec)

def start_ycsb():
	time.sleep(1)
	os.system(ycsb_cmd[ycsb] + thread + outfile)

ycsb_cmd = [\
 "~/ycsb-0.7.0/bin/ycsb load mongodb -P ~/ycsb-0.7.0/workloads/S1",\
 "~/ycsb-0.7.0/bin/ycsb run mongodb -P ~/ycsb-0.7.0/workloads/S2",\
 "~/ycsb-0.7.0/bin/ycsb run mongodb -P ~/ycsb-0.7.0/workloads/S3",\
 "~/ycsb-0.7.0/bin/ycsb run mongodb -P ~/ycsb-0.7.0/workloads/S4",\
 "~/ycsb-0.7.0/bin/ycsb run mongodb -P ~/ycsb-0.7.0/workloads/S5"]

thread = " -threads "
count = " -p recordcount = "
outfile = "" #" > "

if __name__ == "__main__":

	rec = "top -n 1 -b | grep mongo >> "

	rec += sys.argv[1]
	ycsb = int(sys.argv[2])
	thread += sys.argv[3]
	count += sys.argv[4]
	#outfile += sys.argv[5]

	t0=threading.Thread(target=record,args=(1,0.1))
	t1=threading.Thread(target=start_ycsb)

	t1.start()
	t0.start()

