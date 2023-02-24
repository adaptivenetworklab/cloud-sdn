#!/bin/bash

# Start FlowVisor service
echo "Starting FlowVisor service..."
sudo /etc/init.d/flowvisor start

echo "Waiting for service to start..."
sleep 10
echo "Done."

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
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice left tcp:10.244.2.36:10004 admin@leftslice
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice center tcp:10.244.2.36:10005 admin@centerslice
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice right tcp:10.244.2.36:10006 admin@rightslice

# Check defined slices
echo "Check slices just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-slices

# Left Slice

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid10 a 1 any left=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid11-port1 b 1 in_port=1 left=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid11-port2 b 1 in_port=2 left=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid11-port4 b 1 in_port=4 left=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid11-port5 b 1 in_port=5 left=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-port1 4 1 in_port=1 left=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-port4 4 1 in_port=4 left=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-port5 4 1 in_port=5 left=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5-port1 5 1 in_port=1 left=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5-port4 5 1 in_port=4 left=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5-port5 5 1 in_port=5 left=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port1 1 1 in_port=1 left=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port2 1 1 in_port=2 left=7

# Center Slice

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid12 c 1 any center=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid13 d 1 any center=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6 6 1 any center=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7 7 1 any center=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2 2 1 any center=7

# Right Slice

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid14-port2 e 1 in_port=2 right=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid14-port3 e 1 in_port=3 right=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid14-port4 e 1 in_port=4 right=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid14-port5 e 1 in_port=5 right=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid15 f 1 any right=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid8-port3 8 1 in_port=3 right=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid8-port5 8 1 in_port=5 right=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid8-port6 8 1 in_port=6 right=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid9-port3 9 1 in_port=3 right=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid9-port4 9 1 in_port=4 right=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid9-port5 9 1 in_port=5 right=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-port5 3 1 in_port=5 right=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-port6 3 1 in_port=6 right=7
