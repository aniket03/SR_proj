import soldier

soldier.run("sudo RABBITMQ_NODE_PORT=5673 RABBITMQ_NODENAME=rb1 rabbitmq-server -detached").output
soldier.run("sudo RABBITMQ_NODE_PORT=5674 RABBITMQ_NODENAME=rb2 rabbitmq-server -detached").output

soldier.run("sudo rabbitmqctl -n rb1 stop_app").output
soldier.run("sudo rabbitmqctl -n rb1 reset").output
soldier.run("sudo rabbitmqctl -n rb1 start_app").output

soldier.run("sudo rabbitmqctl -n rb2 stop_app").output
soldier.run("sudo rabbitmqctl -n rb2 reset").output
soldier.run("sudo rabbitmqctl -n rb2 start_app").output


soldier.run("sudo rabbitmqctl -n rb2 stop_app").output
soldier.run("sudo rabbitmqctl -n rb2 join_cluster rb1@ANIKET").output
soldier.run("sudo rabbitmqctl -n rb2 start_app").output

soldier.run(" sudo rabbitmqctl -n rb1 set_policy ha-all \"\" \'{\"ha-mode\":\"all\",\"ha-sync-mode\":\"automatic\"}\'").output


## Some notes:
##Cluster of rabbitMQ nodes set
##HA policy set
## Erlang cookie will as it is be same if we follow AWS guide to form nodes
## HAProxy if used can be configured here