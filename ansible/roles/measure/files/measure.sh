#!/usr/bin/env bash

function do_replay() {
	# Prepare tcpreplay flags
	speed="-t"
	[ "${1}" -gt 0 ] && speed="-p $(( ${1} / ${#players[@]} ))"
	netmap="--netmap --nm-delay ${netmap_delay:-5}"
	[ "${netmap_delay}" -eq 0 ] && netmap=""
	duration="${replay_duration:-30}"
	rflags="-K -q -T gtod -l 10000000 ${netmap} --duration=${duration} ${speed}"

	# Stats before for each target
	for target in targets:
		ssh "${user}@${target}" ./gather_stats.sh "before${target}.log"

	# Replay the trace file
	tcpreplay -i $1 ${rflags} $2
	
	# Stats after and compute
	for target in targets:
		ssh "${user}@${target}" ./gather_stats.sh "after${target}.log"
		ssh "${user}@${target}" ./compute_rate.sh ${pps}

}

pps=$1
pcap_file=$2
user=$3
targets=$4 # Like "192.168.0.1 192.168.0.2 192.168.0.3"

do_replay pps pcap_file