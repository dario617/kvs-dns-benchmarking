#!/usr/bin/env bash

# Author: Dario Andhael
# Issues at dpalma@dcc.uchile.cl
echo -e "
    \033[1;31m__ ___    _______    ____  _   _______
   / //_/ |  / / ___/   / __ \/ | / / ___/
  / ,<  | | / /\__ \   / / / /  |/ /\__ \ 
 / /| | | |/ /___/ /  / /_/ / /|  /___/ / 
/_/ |_| |___//____/  /_____/_/ |_//____/  
                                          
    ____                  __                         __  
   / __ )___  ____  _____/ /_  ____ ___  ____ ______/ /__
  / __  / _ \/ __ \/ ___/ __ \/ __ \`__ \/ __ \`/ ___/ //_/
 / /_/ /  __/ / / / /__/ / / / / / / / / /_/ / /  / ,<   
/_____/\___/_/ /_/\___/_/ /_/_/ /_/ /_/\__,_/_/  /_/|_|  

\033[0mRemember to set ansible variables before running the tests
Go to ansible/inventory and ansible/playbooks/group_vars
and set the corresponding variables.

NB: Additional ssh and password setup is required as explained on 
the README

Setup should run only once.
"
cd ansible
# Setup password for multiple playbooks
read -p 'Do you want to store your password in a variable? (y/n) ' doPass
if [ $doPass == "y" ]; then
    read -sp 'Please type your password: ' daPasswd
    echo ""
else
    echo "\__ you will be prompted for each test for your password"
fi
# Setup
read -p 'Do you wish to setup the systems? (y/n) ' doSetup
if [ $doSetup == "y" ]; then
    echo "Starting setup"
    if [ -z $daPasswd ]; then
        ansible-playbook -K playbooks/setup.yml
    else
        ansible-playbook playbooks/setup.yml --extra-vars "ansible_become_pass=${daPasswd}"
    fi
else
    echo "Skipping setup"
fi
# Create a set of UDP packets and queries
read -p 'Create queries, UDP requests and configurations? (y/n) ' doPCAP
if [ $doPCAP == "y" ]; then
    echo "Do queries and config setup"
    if [ -z $daPasswd ]; then
        ansible-playbook -K playbooks/pre_run.yml
    else
        ansible-playbook playbooks/pre_run.yml --extra-vars "ansible_become_pass=${daPasswd}"
    fi
else
    echo "Skipping PCAP setup"
fi
# Tests
read -p 'Run all tests and measure? (y/n) ' doAll
if [ $doAll == "y" ]; then
    echo "Running all tests"
    while IFS= read -r line; do
        export $line
        echo "############# Doing ${SERVER} with ${ZONES} values #############"
        if [ -z $daPasswd ]; then
            ansible-playbook -K playbooks/run_and_measure.yml
        else
            ansible-playbook playbooks/run_and_measure.yml --extra-vars "ansible_become_pass=${daPasswd}"
        fi
        returned=$?
        [[ $returned -eq "99" ]] && echo "[CANCELED] Aborting all test" && break
    done < "../tests.conf"
else
    echo "Continue..."
fi

# Move results to another folder over here
mkdir -p ../results
mv playbooks/results/* ../results
echo "If everything went well results were saved at results"
echo "Bye bye"