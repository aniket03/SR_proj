import paramiko

master = ''
slaves = [
	''
]

hostnames = [master]+slaves  #to form hostnames list

path_key= "/home/aniket/Downloads/rabbitmqkey.pem"  #AWS security key

private_ip = {}	# Dict to store private ip of each host since gonna be same for each host
pub_key = paramiko.RSAKey.from_private_key_file(path_key)

#Function returns output on remote shell
def ssh_session(host,command):
	# To establish ssh session with the reqd server
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=host, username='ubuntu', pkey=pub_key)
	transport = ssh_client.get_transport()
	session = transport.open_session()
	session.set_combine_stderr(True)
	session.get_pty()

	session.exec_command(command)
	stdin = session.makefile('wb', -1)
	stdout = session.makefile('rb', -1)
	shell_lines = stdout.readlines()
	ssh_client.close()
	return shell_lines

#To obtain private ips of each 
for host in hostnames:
	print "Getting private ip of host", host
	shell_lines = ssh_session(host,'hostname')
	private_ip[host] = shell_lines[0][:len(shell_lines[0])-2]  #so as to remove last 2 chars


# To cluster the nodes using join_cluster 
# will be launched by slave
for slave in slaves:
	# To execute the command of join_cluster
	commands =[
		'sudo -i rabbitmqctl stop_app',
		"sudo -i rabbitmqctl join_cluster rabbit@"+private_ip[master] ,
		'sudo -i rabbitmqctl start_app',
		'sudo -i rabbitmqctl cluster_status',
	]
	single_command = "\n".join(commands)
	shell_lines = ssh_session(slave,single_command)
	for s in shell_lines:
		print s

#From master node to set HA policy 
command = " sudo rabbitmqctl set_policy ha-all \"\" \'{\"ha-mode\":\"all\",\"ha-sync-mode\":\"automatic\"}\'"
shell_lines = ssh_session(master,command)
for s in shell_lines:
	print s
