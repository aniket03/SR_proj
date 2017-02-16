#Steps to setup RabbitMQ servers cluster using EC2

###Note:  Before running the python scripts mentioned here make sure you have paramiko 2.1.1 installed. To install the same try:  sudo pip install paramiko --upgrade

1. Create a new security key which shall be same for all the AWS instances. Let this be named "rabbitmqkey". Any description can be added.
Also change permission of the key file eg : chmod 400 rabbitmqkey.pem

2. Create a new security group on AWS, with following under inbound ports:
```
##All TCP            TCP          0 - 65535     0.0.0.0/0
SSH                TCP             22         0.0.0.0/0
Custom TCP Rule    TCP            4369        0.0.0.0/0
Custom TCP Rule    TCP            5671        0.0.0.0/0
Custom TCP Rule    TCP            15672       0.0.0.0/0
Custom TCP Rule    TCP            25672       0.0.0.0/0
Custom TCP Rule    TCP            35197       0.0.0.0/0
Custom TCP Rule    TCP            55672       0.0.0.0/0
```

3. Create anew AWS EC2 instance
	1. I used Ubuntu 16.04 server with t2.micro instance type
	2. Open set_RMQ_EC2.py and replace public DNS or instance's name with your instance's name in the "hostnames" list.
	2. In path_key give the path to the security key used to create your instance.
	3. Run set_RMQ_EC2.py to build rabbitMQ server up and running on this instance.

4. Create an image of your AWS EC2 instance.

5. After the image is constructed, create a new instance using that image. Make sure this instance also belongs to the same security group.

6. After the instance gets created, this should be our slave machine. Replace in after_img.py the master and slave hostnames with the public DNS [instance names of your master and slave instances]. Also make the required changes at required places. 

7. Replace the private key with the one present at your computer.

8. Run the script after_img.py. This shall create the cluster of master and slave between these two instances and also set the mirroring policy between the queues.

9. To check whether the rabbitmq queues are working on their dedicated servers.	
	In your web browser type:
	rabbit@<pub-ip-addr-of-your-EC2>:5672
	
10. Launch an elastic load balncer (ELB) with the same security group as was used to create the EC2 instances.
For listening to SSl:
Set LB Protocol to '''TCP/5671'''
And Instance protocol to '''TCP/5671'''

For listening management plugin:
Set LB Protocol to '''TCP/15672'''
And Instance protocol to '''TCP/15672'''

Then in 2nd step choose our security group 
Also configure Health Check ping to '''TCP/5671'''
Then add all EC2 instances to the LB
Review and Launch

11. Update the '''BROKER_URL''' in settings.py file to point to ELB instance. Use A-record address shown on ELB's description page for the same.

