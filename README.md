# kvs-dns-benchmarking
```shell
    __ ___    _______    ____  _   _______
   / //_/ |  / / ___/   / __ \/ | / / ___/
  / ,<  | | / /\__ \   / / / /  |/ /\__ \ 
 / /| | | |/ /___/ /  / /_/ / /|  /___/ / 
/_/ |_| |___//____/  /_____/_/ |_//____/  
                                          
    ____                  __                         __  
   / __ )___  ____  _____/ /_  ____ ___  ____ ______/ /__
  / __  / _ \/ __ \/ ___/ __ \/ __ `__ \/ __ `/ ___/ //_/
 / /_/ /  __/ / / / /__/ / / / / / / / / /_/ / /  / ,<   
/_____/\___/_/ /_/\___/_/ /_/_/ /_/ /_/\__,_/_/  /_/|_|
```

Compare the average throughput of different dns servers.

It compares
- queries per second
- answered responeses
- memory usage
- failure resiliance

## Prerequisites

To run the benchmark you need to install **ansible** version 2.
The benchmark is written for a setup of 3 server machines and one or more requesters (yet to test multiple requesters).

It is required to have password-less access between the servers using an SSH-key. In particular:
- Each machine must have the same user with password-less sudo (same password as well). This was done in order to avoid setting the root user setting ssh keys with other servers.
- One of the servers will orchestrate backends so this one needs to have password-less SSH access to the others.
- The requester (or requesters) must be able to connect to the servers using a password-less connection.

The servers must have the following ports open for the *KvsDns server* for its different backends:
  * Redis: 7001,7002,7003,7004,7005,7006 and 17001,17002,17003,17004,17005,17006 since Redis uses "server port + 10" for intercluster gossip.
  * Cassandra: 7000, 9042, 9160
  * Etcd: 2380, 2379

To compute the results and create charts the python3 environment needs to install the requisites.txt 

## Run and configuration

Basic configuration requires a non root user, the IP addresses of each machine, and tests configs like which server to test, what test to run, and others. Modify the files:
* ansible/inventory/hosts
* ansible/playbooks/group_vars/all.
* tests.conf; each line sets the variables SERVER and ZONES, the choices are the supported servers/backends and for the zones "random" or "real".

Once the variables are written just run and follow the prompts:
```
user$ ./run_benchmark.sh
```

## Other

### Tools
If you wish to create a new dataset to test run
```bash
user$ ./reset_data.sh
```
and if you want to remove all data from caches (to have a clean test) using the same script accept the delete databases option.

### Remove files

Just remove the working_directory you have configured, and the databases caches if you used etcd.

### Issues
Mail me at dpalma@dcc.uchile.cl

#### Credits

Hector Castro, Azavea Inc. https://github.com/azavea/ansible-golang

Knot Benchmarking DNS