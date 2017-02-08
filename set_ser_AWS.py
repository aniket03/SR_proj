##Should run on local machine
## And ssh into your AWS accounts then start rabbitmq-server

import paramiko

hostnames = [
	'ec2-54-173-2-90.compute-1.amazonaws.com'		##Your instance's public name
	
]
## since gonna be same for each host
k = paramiko.RSAKey.from_private_key_file("/home/aniket/Downloads/rabbitmqkey.pem")

##To set up RMQ-server up and running on each node
for host in hostnames:
	print "Setting RabbitMQ on host", host
	## To establish ssh session with the reqd server
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=host, username='ubuntu', pkey=k)
	transport = ssh.get_transport()
	session = transport.open_session()
	session.set_combine_stderr(True)
	session.get_pty()

	## To execute the commands
	commands =[
		'sudo -i apt-get install rabbitmq-server -y',
		'sudo rabbitmq-plugins enable rabbitmq_management',
		'sudo -i rabbitmq-server -detached',
		'sudo -i rabbitmqctl stop_app',
		'sudo -i rabbitmqctl reset',
		'sudo -i rabbitmqctl start_app',
		'sudo -i rabbitmqctl cluster_status',
	]

	## To make a single command
	single_command = ""
	for i in range(len(commands)):
		if i < len(commands)-1:
			single_command=single_command + (commands[i]+"\n")
		else:
			single_command=single_command + (commands[i])

	print single_command
	session.exec_command(single_command)
	stdin = session.makefile('wb', -1)
	stdout = session.makefile('rb', -1)
	shell_lines = stdout.readlines()
	for s in shell_lines:
		print s
	ssh.close()

'''
Chain of Events
1. pip install paramiko --upgrade
Error: ImportError: No module named packaging.version
Resolved: sudo pip install packaging
2. Again tried 1
Error: ImportError: No module named appdirs
Resolved: sudo pip install appdirs
3. Again tried 1
This time it worked

4. Now sudo apt-get install rabbitmq-server not working
Error: E: Could not get lock /var/lib/dpkg/lock - open (11: Resource temporarily unavailable)

5. Try This
stdin, stdout, stderr = client.exec_command(command,  get_pty=True)
'''
