import socket

s0 = socket.socket()
s1 = socket.socket()
host = socket.gethostname()
port0 = 6672
port1 = 6674
try:
  s0.connect((host,port0))
except:
  pass

try:
  s1.connect((host,port1))
except:
  pass
s0.close()
s1.close()
