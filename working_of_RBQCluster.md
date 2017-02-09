Load balancers only help in detecting whether a particular RMQ is active or not, and in case it is not, it is never sent any tasks.
ELB always follows RR scheduling algorithm to rotate tasks. If a task is sent to a slave node, it won't get executed there, but would be redirected to the current master node, to be enqueued in its queue. This way, tasks only get enqueued in the master queue, and also get mirrored to the slave queues.
In case the master or any other node dies ELB never directs any traffic to that node and the RabbitMQ cluster itself shall promote the eldest slave to become the master node.

Ref link:  https://insidethecpu.com/2014/11/17/load-balancing-a-rabbitmq-cluster/