import time

start=time.time()
for i in range (10000000):
   a=1+1999999
print(time.time()-start>3) 