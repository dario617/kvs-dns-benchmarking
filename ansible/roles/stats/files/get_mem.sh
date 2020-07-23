#!/usr/bin/env bash

free -m|awk '{print $3}'|tail -n 2 >> $1
mem=()
while read line; do
mem+=($line)
done < $1
diff_mem=$(bc <<< "${mem[2]} - ${mem[0]}")
diff_swap=$(bc <<< "${mem[3]} - ${mem[1]}")

echo "mem ${diff_mem} swap ${diff_swap}" > $1