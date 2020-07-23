#!/usr/bin/env bash

source env_vars.sh

function dig_zones {
  # Wait for 20% of last zones
	# Probabilistic, but digging 1M+ times is too slow and affects the results
	zonelist="$1"
	zonecount=$(cat ${zonelist}|wc -l)
	portion=$(( ${zonecount} / 100 + 20 ))
  
  # Reset file
  touch $3
  echo "" > $3

  for i in {$2..1}
  do
    while read zone;
    do
      for target in $targets
      do
        dig @$target -p $myPort +notcp $zone SOA | grep "Query time" | awk '{print $4, $5}' >> $3
      done
    done < <(tail -n ${portion} ${zonelist})
  done
}

# As dig_zones file repeat out
dig_zones $1 $2 $3