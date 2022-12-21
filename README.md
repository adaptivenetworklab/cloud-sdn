#  Implementation of Microservices-Based Ryu Controller for Multi-Tenant Network Slicing

## Design System
In this research, Ryu SDN Controller, which is already based on microservices, will be used as a multi-tenant control of the system. Every sub-function or sub-system in the Ryu SDN Controller that is still monolithic will be broken down and each of these subsystems will be run using a Docker container. 

<img src="https://github.com/adaptivenetworklab/cloud-sdn/blob/main/assets/System%20Design.png" width="128"/>

Then as a controller and slice maker on the data plane, the Flow Space feature from the Flowvisor Controller will be used. This flowvisor will also run as a docker container. The topology will adapt to the test scenarios that will be tested later. The parameters to be tested are delay, throughput, and packet loss, with the load measurement tool using Iperf.

## Testbed Spec
In this research the research was conducted using 2 Virtual machines (VM) which will be built on top of Openstack. The operating system used is Ubuntu 20.04. The first VM will be installed by Minikube as a container orchestrator, and the second VM will be installed by Mininet as a network topology scenario simulation.

Attempt | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 | #9 | #10 | #11
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |--- |---
Seconds | 301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269
Third | 301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269
Fourth | 301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269
