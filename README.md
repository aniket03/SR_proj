THis is a sample Django project which uses rabbitMQ as a queueing service along with Celery

First make a virtual environment
And then:
pip install -r requirements.txt

Then first exit the virtual environment:

In file set_ser.py change hostname of each rabbitMQ node to ur computer's username
[like mine was ANIKET]

Then run:
1st. Install Soldier
	sudo pip install soldier
And then:
sudo python set_ser.py     

Above command will set up a cluster of rabbitMQ nodes.

To enable queue mirroring in the the cluster nodes:
use this in terminal:

sudo rabbitmqctl -n rb1 set_policy ha-all "" '{"ha-mode":"all","ha-sync-mode":"automatic"}'

Afterwards install HAproxy on the system using:
sudo apt-get install haproxy

make a copy of original haproxy.cfg using
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.orignal
For just in case things don't work as they should

Then copy the haproxy.cfg file in this repo to /etc/haproxy/

Then open the port which shall be used by load balancer to accept requests:
$ firewall-cmd --permanent --add-port=5500/tcp
$ firewall-cmd --reload


Thats it and launch two terminals with virtual env in both:

TO launch celery-worker:
$ celery -A SR_proj worker -l info

To launch tasks:
$ python manage.py shell
>>>  from helloapp.tasks  import *
>>>  x=add.delay(44,55)
>>>  x.get()	##To fetch results

TO TEST HA 
From 3rd terminal
launch 
$ sudo rabbitmqctl -n rb1 stop_app






