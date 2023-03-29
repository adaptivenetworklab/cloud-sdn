#!/bin/bash

# Start FlowVisor service
echo "Starting FlowVisor service..."
sudo /etc/init.d/flowvisor start

echo "Waiting for service to start..."
sleep 10
echo "Done."

# Set Config
echo "FlowVisor topo controller config:"
fvctl -f /etc/flowvisor/flowvisor.passwd set-config --enable-topo-ctrl

# Get FlowVisor current config
echo "FlowVisor initial config:"
fvctl -f /etc/flowvisor/flowvisor.passwd get-config

# Get FlowVisor current defined slices
echo "FlowVisor initially defined slices:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-slices

# Get FlowVisor current defined flowspaces
echo "FlowVisor initially defined flowspaces:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-flowspace

# Get FlowVisor connected switches
echo "FlowVisor connected switches:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-datapaths

# Get FlowVisor connected switches links up
echo "FlowVisor connected switches links:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-links

# Define the FlowVisor slices
echo "Definition of FlowVisor slices..."
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice -p 123 upper tcp:$UPPER_MIDDLEWARE:10001 admin@upperslice

echo "Waiting for slices to be defined..."
sleep 2
echo "Done."

echo "Continuing.."
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice -p 123 middle tcp:$MIDDLE_MIDDLEWARE:10002 admin@middleslice

echo "Waiting for slices to be defined..."
sleep 2
echo "Done."

echo "Continuing.."
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice -p 123 lower tcp:$LOWER_MIDDLEWARE:10003 admin@lowerslice

# Check defined slices
echo "Check slices just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-slices

# Define flowspaces
echo "Definition of flowspaces..."
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1 1 1 any upper=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port3 2 1 in_port=3 middle=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port1 2 1 in_port=1 middle=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port2 2 1 in_port=2 lower=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port4 2 1 in_port=4 lower=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3 3 1 any upper=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-port1 4 1 in_port=1 upper=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-port3 4 1 in_port=3 upper=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-port2 4 1 in_port=2 middle=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-port4 4 1 in_port=4 middle=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5 5 1 any lower=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6 6 1 any upper=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7-port1 7 1 in_port=1 middle=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7-port3 7 1 in_port=3 middle=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7-port2 7 1 in_port=2 lower=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7-port4 7 1 in_port=4 lower=7

# Check all the flowspaces added
echo "Check all flowspaces just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-flowspace

echo "Waiting for service to be configurated..."
sleep 10
echo "Done."

#Stop Flowvisor
sudo /etc/init.d/flowvisor stop

#Run it again
flowvisor








