#!/usr/bin/env bash

source env_vars.sh

# The tcpreplay runs under 10 seconds so we try to 
# kill a random server at half time 5s with a delta (1s)
#
# A controlled failure should benefit the key-value-stores

function kill_bind {
  echo "bind"
  sleep 6
  ssh $user@$1 "cd ${wd}; kill $(cat bind9/named.pid)"
}

function kill_knot {
  echo "knot"
  sleep 6
  ssh $user@$1 "cd ${wd}; ./knot2/src/knotc -c knot2.conf stop"
}

function kill_nsd {
  echo "nsd"
  sleep 6
  ssh $user@$1 "cd ${wd}; kill $(cat nsd4/nsd.pid)"
}

function kill_redis {
  echo "redis"
  # Select port from index
  redis_port=7001
  [[ $2 == 0 ]] && redis_port=7001
  [[ $2 == 1 ]] && redis_port=7003
  [[ $2 == 2 ]] && redis_port=7005
  sleep 6
  ssh $user@$1 "cd ${wd}/redis-5.0.8/conf/; ./redis-cli -p ${redis_port} debug segfault"
}

function kill_cassandra {
  echo "cassandra"
  sleep 6
  ssh $user@$1 "cd ${wd}; kill $(cat cassandra_pid)"
}

function kill_etcd {
  echo "etcd"
  sleep 6
  ssh $user@$1 "sudo systemctl stop etcd.service"
}

server=$1
# Random select victim
custom_id=$(( $RANDOM % 3 ))
cnt=0
victim=""
for t in $targets; do
  [[ $cnt == $custom_id ]] && victim=$t && break
  cnt=$(bc <<< $cnt+1)
done

[[ $server == "bind9" ]] && kill_bind $victim
[[ $server == "knot2" ]] && kill_knot $victim
[[ $server == "nsd4" ]] && kill_nsd $victim
[[ $server == "redis" ]] && kill_redis $victim $cnt
[[ $server == "cassandra" ]] && kill_cassandra $victim
[[ $server == "etcd" ]] && kill_etcd $victim