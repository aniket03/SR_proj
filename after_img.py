import paramiko

hostnames = [
	'ec2-54-173-2-90.compute-1.amazonaws.com',		##Master(original)
	'ec2-54-234-142-144.compute-1.amazonaws.com'	##slave(image)

]

master = 'ec2-54-173-2-90.compute-1.amazonaws.com'
slaves = [
	'ec2-54-234-142-144.compute-1.amazonaws.com'
]	##Since there can be multiple slaves

pr_ip = {}	## Dict to store private ip of each host
## since gonna be same for each host
k = paramiko.RSAKey.from_private_key_file("/home/aniket/Downloads/rabbitmqkey.pem")

##To obtain private ips of each 
for host in hostnames:
	print "Getting private ip of host", host
	## To establish ssh session with the reqd server
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=host, username='ubuntu', pkey=k)
	transport = ssh.get_transport()
	session = transport.open_session()
	session.set_combine_stderr(True)
	session.get_pty()

	## To execute the command to get host name
	session.exec_command("hostname")
	stdin = session.makefile('wb', -1)
	stdout = session.makefile('rb', -1)
	shell_lines = stdout.readlines()
	pr_ip[host] = shell_lines[0][:len(shell_lines[0])-2]
	##so as to remove last 2 chars
	ssh.close()

## To cluster the nodes using join_cluster 
## will be launched by slave
for slave in slaves:
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=slave, username='ubuntu', pkey=k)
	transport = ssh.get_transport()
	session = transport.open_session()
	session.set_combine_stderr(True)
	session.get_pty()

	## To execute the command of join_cluster
	commands =[
		'sudo -i rabbitmqctl stop_app',
		"sudo -i rabbitmqctl join_cluster rabbit@"+pr_ip[master] ,
		'sudo -i rabbitmqctl start_app',
		'sudo -i rabbitmqctl cluster_status',
	]
	single_command = ""
	for i in range(len(commands)):
		if i < len(commands)-1:
			single_command=single_command + (commands[i]+"\n")
		else:
			single_command=single_command + (commands[i])

	session.exec_command(single_command)
	stdin = session.makefile('wb', -1)
	stdout = session.makefile('rb', -1)
	shell_lines = stdout.readlines()
	for s in shell_lines:
		print s
	##so as to remove last 2 chars
	ssh.close()


##From master node to set HA policy
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=master, username='ubuntu', pkey=k)
transport = ssh.get_transport()
session = transport.open_session()
session.set_combine_stderr(True)
session.get_pty()

## To execute the command to get host name
session.exec_command("sudo rabbitmqctl set_policy ha-all \"\" \'{\"ha-mode\":\"all\",\"ha-sync-mode\":\"automatic\"}\'")
stdin = session.makefile('wb', -1)
stdout = session.makefile('rb', -1)
shell_lines = stdout.readlines()
for s in shell_lines:
	print s
ssh.close()

