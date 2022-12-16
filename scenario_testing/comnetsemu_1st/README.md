# Multi-Tenant Slicing

## 1. Mininet

In case your Flowvisor is on a different Instance or inside a container/pod than you can change above script with the following command. Just change the 'FLOWVISOR IP ADDRESS' part.

```bash
sed -i '62s/localhost/FLOWVISOR IP ADDRESS/' mininet-topology.py
```

```bash
sudo python3 first-topology.py
```

## 2. Ryu

Make sure these port is free on your instance.
```bash
ryu run --observe-links --ofp-tcp-listen-port 10001 --wsapi-port 8082 /usr/local/lib/python3.8/dist-packages/ryu/app/gui_topology/gui_topology.py ryu-upperslice.py
```

```bash
ryu run --observe-links --ofp-tcp-listen-port 10002 --wsapi-port 8083 /usr/local/lib/python3.8/dist-packages/ryu/app/gui_topology/gui_topology.py ryu-middleslice.py
```

```bash
ryu run --observe-links --ofp-tcp-listen-port 10003 --wsapi-port 8084 /usr/local/lib/python3.8/dist-packages/ryu/app/gui_topology/gui_topology.py ryu-lowerslice.py
```

## 3. Flowvisor

Change 'localhost' to your Flowvisor instance or container/pod IP, in case your Flowvisor is installed on a different Instance.
```bash
nano flowvisor_slicing.sh
```

```bash
# Define the FlowVisor slices
echo "Definition of FlowVisor slices..."
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice upper tcp:localhost:10001 admin@upperslice
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice middle tcp:localhost:10002 admin@middleslice
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice lower tcp:localhost:10003 admin@lowerslice
```
