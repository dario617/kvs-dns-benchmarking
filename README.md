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
- memory usage (Work In Progress)
- failure resiliance (Work In Progress)

## Prerequisites

To run the benchmark you need to install **ansible** version 2.
The benchmark is written for a setup of 3 server machines and one or more requesters.

It is recommended but not required to have password-less access between the servers using an SSH-key.

Each machine must have the same user and sudo password with password-less sudo.
This was done in order to avoid setting the root user setting ssh keys with other servers.

The servers must have the following ports open for the *KvsDns server* for its different backends:
  * Redis: 7001,7002,7003,7004,7005,7006 and 17001,17002,17003,17004,17005,17006 since Redis uses "server port + 10" for intercluster gossip.
  * Cassandra: 7000, 9042, 9160
  * Etcd: 2380, 2379

## Run and configuration

Basic configuration requires a non root user, the IP addresses of each machine, and tests configs like which server to test, what test to run, and others. Modify the files:
* ansible/inventory/hosts
* ansible/playbooks/group_vars/all.
* tests.conf

Once the variables are written just run and follow the prompts:
```
user$ ./run_benchmark.sh
```

## Other

### Issues
Mail me at dpalma@dcc.uchile.cl

#### Credits

Hector Castro, Azavea Inc. https://github.com/azavea/ansible-golang
Knot Benchmarking DNS