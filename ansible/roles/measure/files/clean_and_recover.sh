#!/usr/bin/env bash

source env_vars.sh

function recover_results{
	for host in $targets; do
    # Tar remote folder
		ssh $user@$host "cd ${wd}; tar -czf ${1}.tar.gz results"
    # Clean
    ssh $user@$host "cd ${wd}; rm results/*"
    # Copy to requester machine
    scp $user@$host:/$wd/$1.tar.gz /home/$user/$wd/results/$1.$host.tar.gz
	done
}

recover_results $1