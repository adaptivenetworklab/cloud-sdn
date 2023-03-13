#  Implementation of Microservices-Based Ryu Controller for Multi-Tenant Network Slicing

The objectives and benefits to be achieved in this research are:
1. Understand how a microservice-based SDN Controller works.
2. Understand how Network Slicing works.
3. Able to implement an effective microservice-based SDN Controller system for Network Slicing.
4. Able to know the effect of Microservice-based SDN Controller on Network Slicing performance on Fat Tree Topology.

## Design System
<img src="https://github.com/adaptivenetworklab/cloud-sdn/blob/main/assets/Design%20System.svg"/>

In this research, Ryu SDN Controller based on microservices used as a multi-tenant control of the system. Every sub-function in the Ryu SDN Controller that is still monolithic will be broken down and each of these subsystems will be run using a Docker container and managed using Kubernetes. Then as a controller and slice maker on the data plane, the Flow Space feature from the Flowvisor Controller container-based will be used to enable some isolation from each tenant. 

### Network Slicing Spesification

Pada topologi fattree menggunakan skenario slicing untuk beberapa host yang terdiri dari layanan yang biasa digunakan end-user dan memiliki alokasi konsumsi bandwidth yang tidak terlalu besar, berikut diantaranya yaitu:

Service Type | Slice Name | Bandwidth | Slicing Path
--- | --- | --- | ---
Video Streaming |  Left Slice | 3 Mbps  | H1-H4
Web Browsing | Center Slice| 1 Mbps  | H5-H8
VoIP | Right Slice| 500 Kbps  | H9-H12

## Testbed Spec
In this research the research was conducted using 4 Virtual machines (VM) which it is built on top of Openstack.

VM | Image | Spec | IP
--- | --- | --- | ---
Master |  Ubuntu 20.04 | 4 vCPU, 4GB RAM, Storage 30GB  | 10.0.0.241, 172.20.3.237
Worker 1 | Ubuntu 20.04 | 8 vCPU, 4GB RAM, Storage 50GB  | 10.0.2.207, 172.20.3.178
Worker 2 | Ubuntu 20.04 | 4 vCPU, 4GB RAM, Storage 30GB  | 10.0.0.128, 172.20.3.242
Flowvisor | Ubuntu 14.04 | 2 vCPU, 2GB RAM, Storage 20GB | 10.0.1.242, 172.20.0.119


