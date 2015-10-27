# Docker swarm warmup
My first look into Docker Swarm and what it can do. Lets get started.

## Install
Wow ok so docker is great at eating its own food. Swarm install is actuall just pulling and running a Docker image that Docker provides on the Docker Hub.

First thing I ran into: the swarm master uses the public Docker environment as its registry endpoint. I had to use our proxy to get a token even made. This will need to change to a private etcd setup.

### Setup single node [etcd](https://github.com/coreos/etcd)


## Swarm Cluster with etcd
Setting up the 

    # on each of your nodes, start the swarm agent
    #  <node_ip> doesn't have to be public (eg. 192.168.0.X),
    #  as long as the swarm manager can access it.
    $ swarm join --addr=<node_ip:2375> etcd://<etcd_ip>/<path>

    # start the manager on any machine or your laptop
    $ swarm manage -H tcp://<swarm_ip:swarm_port> etcd://<etcd_ip>/<path>

    # use the regular docker cli
    $ docker -H tcp://<swarm_ip:swarm_port> info
    $ docker -H tcp://<swarm_ip:swarm_port> run ...
    $ docker -H tcp://<swarm_ip:swarm_port> ps
    $ docker -H tcp://<swarm_ip:swarm_port> logs ...
    ...

    # list nodes in your cluster
    $ swarm list etcd://<etcd_ip>/<path>
    <node_ip:2375>