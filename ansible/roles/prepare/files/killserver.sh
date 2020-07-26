#!/usr/bin/env bash

# Asume pwd to be wd

function kill_bind {
  echo "bind"
  kill -9 $(cat ./bind9/named.pid)
}

function kill_knot {
  echo "knot"
  ./knot2/src/knotc -c knot2.conf stop
}

function kill_nsd {
  echo "nsd"
  kill -9 $(cat ./nsd4/nsd.pid)
}

function kill_redis {
  echo "redis"
  # Select port from index
  redis_port=7001
  [[ $2 == 0 ]] && redis_port=7001
  [[ $2 == 1 ]] && redis_port=7003
  [[ $2 == 2 ]] && redis_port=7005
  cd /redis-5.0.8/conf/
  ./redis-cli -p ${redis_port} debug segfault
}

function kill_cassandra {
  echo "cassandra"
  kill $(cat cassandra_pid)
}

function kill_etcd {
  echo "etcd"
  sudo systemctl stop etcd.service
}

server=$1
cnt=$2

[[ $server == "bind9" ]] && kill_bind
[[ $server == "knot2" ]] && kill_knot
[[ $server == "nsd4" ]] && kill_nsd
[[ $server == "redis" ]] && kill_redis $cnt
[[ $server == "cassandra" ]] && kill_cassandra
[[ $server == "etcd" ]] && kill_etcd