#!/usr/bin/env bash

# Adapted from KnotBenchmark
function wait_for_zones {
  # Wait for 1% of last zones
	# Probabilistic, but digging 1M+ times is too slow and affects the results
	zonelist="$1"
	zonecount=$(cat ${zonelist}|wc -l)
	portion=$(( ${zonecount} / 100 + 1 ))
	while read zone;
	do
		ret=1
		while [ $ret -ne 0 ]; do
			${DIG} @${DIG_ADDR} -p ${PORT} +notcp +retry=0 +time=1 ${zone} SOA|grep -q NOERROR
			ret=$?
			if [ $ret -ne 0 ]; then
				sleep 1
			fi
		done
	done < <(tail -n ${portion} ${zonelist})
}

wait_for_zones $1