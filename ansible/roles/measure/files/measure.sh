#!/usr/bin/env bash

source env_vars.sh

replay_duration="10"
netmap_delay=0
average_packet_size=200
buffer_size=40 # In MBs
measure_period=10
wait_time=40

function do_replay() {
	# Prepare tcpreplay flags
	speed="-t" # --Topspeed
	[ "${1}" -gt 0 ] && speed="-p ${1}" # pps rate defined by sequence
	netmap="--netmap --nm-delay $netmap_delay:-5}"
	[ "${netmap_delay}" -eq 0 ] && netmap=""
	duration="${replay_duration}"
	rflags="-K -q -T gtod -l 10000000 ${netmap} --duration=${duration} ${speed}"

	hostsVar=()
	# Stats before for each target
	for host in $targets; do
		ssh $user@$host "cd ${wd}; ./tools/gather_stats.sh before${host}.log"
		# Add host to array
		hostsVar+=($host)
	done

	# Create custom output for wireshark
	tmp=$(mktemp)
	measure_incoming="-z io,stat,${measure_period},ip.dst==${myIp},ip.src==${hostsVar[0]},ip.src==${hostsVar[1]},ip.src==${hostsVar[2]}"
	measure_sent="-z io,stat,${measure_period},ip.src==${myIp},ip.dst==${hostsVar[0]},ip.dst==${hostsVar[1]},ip.dst==${hostsVar[2]}"

	# Start a wireshark capture session
	sudo tshark -f "udp port ${myPort}" -i $interface -s $average_packet_size -B $buffer_size -q -a duration:$wait_time $measure_incoming $measure_sent > $tmp &
	echo $! > tshark.pid

	# Replay the trace file
	sudo tcpreplay -i $interface $rflags $2
	
	# Give some time for packages to transit
	sleep 5

	# Stats after and compute
	for host in $targets; do
		ssh $user@$host "cd ${wd}; ./tools/gather_stats.sh after${host}.log mem-${host}-${pps}.log cpu-${host}-${pps}.log"
		ssh $user@$host "cd ${wd}; ./tools/compute_rate.sh ${pps}"
	done

	# Wait for wireshark to finish
	tail -f --pid=$(cat tshark.pid) /dev/null

	# Read results and append to file
	echo "===== ${pps}pps, ${replay_duration}s replay duration =====" >> $out_file
	cat $tmp >> $out_file
	echo "===== end test ====" >> $out_file
	echo "" >> $out_file

	return 0
}

pps=$1
pcap_file=$2
out_file=$3

do_replay $pps $pcap_file