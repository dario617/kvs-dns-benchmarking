#!/usr/bin/env bash

function recover_results{
	for host in $targets; do
    # Tar remote folder
		ssh $user@$host "cd ${wd}; tar -czf ${1}.tar.gz results"
    # Clean
    ssh $user@$host "cd ${wd}; rm results/*"
    # Copy to requester machine
    scp $user@$host:/$wd/$1.tar.gz ./
	done
}

targets=$1
wd=$2
testname=$3
user=$4

recover_results $testname