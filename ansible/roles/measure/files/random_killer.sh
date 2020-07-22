#!/usr/bin/env bash

#source env_vars.sh

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

  sleep 6
}

function kill_cassandra {
  echo "cassandra"

  sleep 6
}

function kill_etcd {
  echo "etcd"

  sleep 6
}

server=$1
# Random select victim
custom_id=$(( $RANDOM % 3 ))
cnt=0
victim=""
for t in $targets; do
  [[ $cnt == $custom_id ]] && victim=$t
  cnt=$cnt+1
done

[[ $server == "bind9" ]] && kill_bind $victim
[[ $server == "knot2" ]] && kill_knot $victim
[[ $server == "nsd4" ]] && kill_nsd $victim
[[ $server == "redis" ]] && kill_redis $victim
[[ $server == "cassandra" ]] && kill_cassandra $victim
[[ $server == "etcd" ]] && kill_etcd $victim