#!/usr/bin/env bash

source env_vars.sh

function recover_results {
	for host in $targets; do
    # Tar remote folder
		ssh $user@$host "cd ${wd}; tar -czf ${1}.tar.gz results; rm results/*"
    # Recover memory snapshots
    ssh $user@$host "cd ${wd}; mv mem-${host}-* results/; tar -czf ${1}-mem.tar.gz results; rm results/*"
    # Recover cpu snapshots
    ssh $user@$host "cd ${wd}; mv cpu-${host}-* results/; tar -czf ${1}-cpu.tar.gz results; rm results/*"
    # Recover load average snapshots
    ssh $user@$host "cd ${wd}; mv load-${host}-* results/; tar -czf ${1}-load.tar.gz results; rm results/*"
    # Copy to requester machine
    scp $user@$host:~/$wd/$1.tar.gz /home/$user/$wd/results/$1.$host.tar.gz
    scp $user@$host:~/$wd/$1-mem.tar.gz /home/$user/$wd/results/$1-mem.$host.tar.gz
    scp $user@$host:~/$wd/$1-cpu.tar.gz /home/$user/$wd/results/$1-cpu.$host.tar.gz
    scp $user@$host:~/$wd/$1-load.tar.gz /home/$user/$wd/results/$1-load.$host.tar.gz
    # Remove remote files
    sleep 5
    ssh $user@$host "cd ${wd}; rm *.tar.gz"
	done
}

recover_results $1