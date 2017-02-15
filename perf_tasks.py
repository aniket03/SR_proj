from helloapp.tasks import *
from random import randint
for i in range(100):
	x=randint(1,100)
	y=randint(1,100)
	if i%2==0:
		add.delay(x,y)
	else:
		mul.delay(x,y)