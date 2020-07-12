#!/usr/bin/env bash

echo -e "
    \033[0;31m__ ___    _______    ____  _   _______
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
and set the corresponding variables

"
cd ansible
read -p 'Do you wish to setup the systems? (y/n)' doSetup
if [ $doSetup == "y" ]; then
    echo "Starting setup"
    ansible-playbook -K playbooks/setup.yml
else
    echo "Skipping setup"
fi
read -p 'Run all tests and measure? (y/n)' doAll
if [ $doAll == "y" ]; then
    echo "Running all tests"
    ansible-playbook -K playbooks/run_and_measure.yml 
else
    echo "Continue..."
fi
echo "Results saved at ansible/roles/clean/results"