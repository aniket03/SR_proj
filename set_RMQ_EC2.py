# Should run on local machine
# And ssh into your AWS accounts then start rabbitmq-server

import paramiko
import soldier

hostnames = [
	''		# Your instance's public name
]
# since gonna be same for each host

path_ssh_key="/home/aniket/Downloads/rabbitmqkey.pem"
path_ssl_keys='/home/aniket/rmq-keys/keys-server'
path_config_file = '/home/aniket/SR_proj/rabbitmq.config'
pub_key = paramiko.RSAKey.from_private_key_file(path_key)

#Function returns output on remote shell
def ssh_session(host, command):
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

for host in hostnames:
	commands =[
		'sudo -i apt-get install rabbitmq-server -y',
		'sudo rabbitmq-plugins enable rabbitmq_management',
		'sudo -i rabbitmq-server -detached',
		'sudo -i rabbitmqctl stop_app',
		'sudo -i rabbitmqctl reset',
		'sudo -i rabbitmqctl start_app',
		'sudo -i rabbitmqctl cluster_status',
	]
	single_command = "\n".join(commands)
	shell_lines = ssh_session(host, single_command)
	for s in shell_lines:
		print s

	# To transfer SSL files to AWS instance
	soldier.run("scp -i "+path_key+" -r "+path_ssl_keys+" ubuntu@"+host+":~/").output
	# To transfer rabbitmq.config 
	soldier.run("scp -i "+path_key+" -r "+path_config_file+" ubuntu@"+host+":~/").output
	print "Soldier Done!!"
	commands = [
		"sudo -i mv /home/ubuntu/rabbitmq.config /etc/rabbitmq",
		"sudo -i mv /etc/rabbitmq/rabbitmq-env.conf /etc/rabbitmq/rabbitmq-env.conf.old",
		"sudo -i /etc/init.d/rabbitmq-server stop",
		"sudo -i /etc/init.d/rabbitmq-server start",
		# Above 2 commands to restart RMQ server
	]
	single_command = "\n".join(commands)
	shell_lines = ssh_session(host,single_command)
	for s in shell_lines:
		print s

	# To make new rabbitmq user and provide permissions and to delete guest 
	# This need be done for master of cluster only
	RMQ_user_name="aniket"
	RMQ_password=""
	commands =[
		'sudo -i rabbitmqctl add_user '+RMQ_user_name+' '+RMQ_password,
		'sudo -i rabbitmqctl set_user_tags '+RMQ_user_name+ ' administrator',
		'sudo -i rabbitmqctl set_permissions -p / '+RMQ_user_name+' ".*" ".*" ".*"',
		'sudo -i rabbitmqctl delete_user guest',
	]
	single_command = "\n".join(commands)
	shell_lines = ssh_session(host,single_command)
	for s in shell_lines:
		print s



