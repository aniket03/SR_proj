#Should run on local machine
# And ssh into your AWS accounts then start rabbitmq-server

import paramiko

hostnames = [
	'ec2-54-173-2-90.compute-1.amazonaws.com'		#Your instance's public name
]
# since gonna be same for each host

path_key="/home/aniket/Downloads/rabbitmqkey.pem"
pub_key = paramiko.RSAKey.from_private_key_file(path_key)

#To set up RMQ-server up and running on each node
for host in hostnames:
	print "Setting RabbitMQ on host", host
	## To establish ssh session with the reqd server
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=host, username='ubuntu', pkey=pub_key)
	transport = ssh_client.get_transport()
	session = transport.open_session()
	session.set_combine_stderr(True)
	session.get_pty()

	commands =[
		'sudo -i apt-get install rabbitmq-server -y',
		'sudo rabbitmq-plugins enable rabbitmq_management',
		'sudo -i rabbitmq-server -detached',
		'sudo -i rabbitmqctl stop_app',
		'sudo -i rabbitmqctl reset',
		'sudo -i rabbitmqctl start_app',
		'sudo -i rabbitmqctl cluster_status',
	]

	# To make a single command
	single_command = "\n".join(commands)
	print single_command
	session.exec_command(single_command)
	stdin = session.makefile('wb', -1)
	stdout = session.makefile('rb', -1)
	shell_lines = stdout.readlines()
	for s in shell_lines:
		print s
	ssh_client.close()

