#!/usr/bin/env bash

source env_vars.sh

function dig_zones {
  # Dig for 1% of last zones
	# Probabilistic, but digging 1M+ times is too slow and affects the results
	zonelist="$1"
	zonecount=$(cat ${zonelist}|wc -l)
	portion=$(( ${zonecount} / 100 + 1 ))
  
  # Reset file
  touch $2
  echo "" > $2

  while read zone;
  do
    for target in $targets
    do
      dig @$target -p $myPort +notcp $zone SOA | grep "Query time" | awk '{print $4, $5}' >> $2
    done
  done < <(tail -n ${portion} ${zonelist})
}

# As dig_zones file out
dig_zones $1 $2