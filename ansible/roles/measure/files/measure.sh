#!/usr/bin/env bash

replay_duration="10"
netmap_delay=0

function do_replay() {
	# Prepare tcpreplay flags
	speed="-t"
	[ "${1}" -gt 0 ] && speed="-p $(( ${1} ))"
	netmap="--netmap --nm-delay ${netmap_delay:-5}"
	[ "${netmap_delay}" -eq 0 ] && netmap=""
	duration="${replay_duration}"
	rflags="-K -q -T gtod -l 10000000 ${netmap} --duration=${duration} ${speed}"

	# Stats before for each target
	for host in $targets; do
		ssh $user@$host "cd ${wd}; ./gather_stats.sh before${host}.log"
	done

	# Replay the trace file
	tcpprep --auto=client --cachefile=tmp.cache --pcap=$2
	sudo tcpreplay -i $interface ${rflags} tmp.cache
	
	# Stats after and compute
	for host in $targets; do
		ssh $user@$host "cd ${wd}; ./gather_stats.sh after${host}.log"
		ssh $user@$host "cd ${wd}; ./compute_rate.sh ${pps}"
	done

}

pps=$1
pcap_file=$2
user=$3
targets=$4 # Like "192.168.0.1 192.168.0.2 192.168.0.3"
wd=$5
interface=$6

do_replay $pps $pcap_file