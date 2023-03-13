# Ryu Microservices

Ryu SDN Controller as microservices

## Start simple_switch microservice
### Setting
Current Directory: ryu_microservices/rest_client/

Prerequisites: pip install -r requirements.txt

```bash
python3 simple_switch_rest.py
```

## Start ryu with ofp_emitter e ofctl_rest
### Setting
Current Directory: ryu_microservices/ryu_apps

Prerequisites: pip install -r requirements.txt

```bash
ryu-manager ofp_emitter.py ofctl_rest.py
```
	
## Start mininet with 10 host e 5 switch
### Setting
Current Directory: ryu_microservices/scripts

Prerequisites: mininet

```bash
./mininet_10_5.sh
```
	
! Wait some times at the startup before using mininet

## Set IP addresses

### IP address uses by ryu to communicate with simple_switch_rest 
Set variable simpleswitch in the file ryu_app/ofp_emitter.py

### IP address uses by simple_switch_rest to communicate with ryu
Set variable RYU_BASE_URL in the file rest_client/simple_switch_rest.py

## Configure timeout per flow entry

Set in the file rest_client/simple_switch_rest.py parameters named idle_timeout (seconds) and hard_timeout (seconds) in the function build_flow(..) [default value is 0 that means no timeout]

## Execute with docker

Start the ryu container before, then the container named simple_switch_rest