#!/bin/bash

arp -a -d
while true; do
        echo "running change detection script "
        arp -a -n -l > routingtable.txt
        sleep 10
done
