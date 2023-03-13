#  Implementation of Microservices-Based Ryu Controller for Multi-Tenant Network Slicing

Testing halo saya branch mana?

## Design System
<img src="https://github.com/adaptivenetworklab/cloud-sdn/blob/main/assets/Design%20System.svg"/>

In this research, Ryu SDN Controller based on microservices, will be used as a multi-tenant control of the system. Every sub-function in the Ryu SDN Controller that is still monolithic will be broken down and each of these subsystems will be run using a Docker container and managed using Kubernetes. Then as a controller and slice maker on the data plane, the Flow Space feature from the Flowvisor Controller container-based will be used to enable some isolation. 

## Testbed Spec
In this research the research was conducted using 2 Virtual machines (VM) which will be built on top of Openstack. The operating system used is Ubuntu 20.04. The first VM will be installed by Minikube as a container orchestrator, and the second VM will be installed by Mininet as a network topology scenario simulation.

VM | Image | Spec | IP
--- | --- | --- |
Master |  Ubuntu 20.04 | 4 vCPU, 4GB RAM, Storage 30GB  | 10.0.0.241, 172.20.3.237
Worker 1 | Ubuntu 20.04 | 8 vCPU, 4GB RAM, Storage 50GB  | 10.0.2.207, 172.20.3.178
Worker 2 | Ubuntu 20.04 | 4 vCPU, 4GB RAM, Storage 30GB  | 10.0.0.128, 172.20.3.242
Flowvisor | Ubuntu 14.04 | 2 vCPU, 2GB RAM, Storage 20GB | 10.0.1.242, 172.20.0.119
