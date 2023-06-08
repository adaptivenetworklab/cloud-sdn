#! /bin/bash

duration=30
interval=0.000001
dst_host=10.0.0.7

end=$((SECONDS+$duration))


while [ $SECONDS -lt $end ]
do
        curl $dst_host
        sleep $interval
done