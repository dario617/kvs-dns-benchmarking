#!/usr/bin/env bash

source env_vars.sh

# The tcpreplay runs under 10 seconds so we try to 
# kill a random server at half time 5s with a delta (1s)
#
# A controlled failure should benefit the key-value-stores

server=$1
# Random select victim
custom_id=$(( $RANDOM % 3 ))
cnt=0
victim=""
for t in $targets; do
  [[ $cnt == $custom_id ]] && victim=$t && break
  cnt=$(bc <<< $cnt+1)
done

sleep 6
ssh $user@$victim "cd ${wd}; ./tools/killserver.sh $server $cnt"