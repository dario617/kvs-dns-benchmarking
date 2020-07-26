#!/usr/bin/env bash

# Author: Dario Andhael
# Issues at dpalma@dcc.uchile.cl

echo -e "
           ######################
           # Reset data utility #
           ######################

Clear parsed and random data from data folders
Then continue with a pre_run playbook

If desired release data caches from databases
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
read -p 'Run? (y/n) ' doSetup
if [ $doSetup == "y" ]; then
    echo "Reset everything"
    if [ -z $daPasswd ]; then
        ansible-playbook -K playbooks/reset_dataset.yml
        ansible-playbook -K playbooks/pre_run.yml
    else
        ansible-playbook playbooks/reset_dataset.yml --extra-vars "ansible_become_pass=${daPasswd}"
        ansible-playbook playbooks/pre_run.yml --extra-vars "ansible_become_pass=${daPasswd}"
    fi
else
    echo "Aborting..."
fi

echo -e "
Removing databases will require an upload for KvsDns,
which is a time consuming operation. It will save some
space derived from releasing caches.
"
read -p '[CAUTION] Delete databases? (y/n) ' doDelete
if [ $doDelete == "y" ]; then
    echo "Delete everything"
    if [ -z $daPasswd ]; then
        ansible-playbook -K playbooks/reset_dbs.yml
    else
        ansible-playbook playbooks/reset_dbs.yml --extra-vars "ansible_become_pass=${daPasswd}"
    fi
else
    echo "Aborting... bye bye"
fi