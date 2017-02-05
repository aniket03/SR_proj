import soldier

soldier.run("sudo RABBITMQ_NODE_PORT=5673 RABBITMQ_NODENAME=rb1 rabbitmq-server -detached")
soldier.run("sudo RABBITMQ_NODE_PORT=5674 RABBITMQ_NODENAME=rb2 rabbitmq-server -detached")
soldier.run("sudo rabbitmqctl -n rb2 stop_app")
soldier.run("sudo rabbitmqctl -n rb2 join_cluster rb1@ANIKET")
soldier.run("sudo rabbitmqctl -n rb2 start_app")

##soldier.run(rabbitmqctl -n rb1 set_policy ha-all "" '{"ha-mode":"all","ha-sync-mode":"automatic"}')
##Above line must be checked