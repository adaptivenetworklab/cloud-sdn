#! /bin/bash

duration=10
interval=2
dst_host=10.0.0.2

end=$((SECONDS+$duration))


while [ $SECONDS -lt $end ]
do
        curl $dst_host
        sleep $interval
done
