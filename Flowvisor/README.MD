# Flowvisor

## What is Flowvisor

Flowvisor is a network virtualization tool that allows administrators to divide a single physical network into multiple logical networks, or "slices." Each slice is isolated from the others and can be configured independently, allowing administrators to test new network configurations or deploy multiple virtual networks on a single physical infrastructure. 


Flowvisor uses a centralized controller to manage the traffic flows between slices and can also be used to monitor traffic, collect statistics, and perform other network management tasks. Flowvisor is often used in research and education environments, where it can provide a flexible and cost-effective way to support multiple experimental or instructional networks on a single infrastructure.

## How to Install Flowvisor

Flowvisor will be deployed in a single VM and will act as a proxy controller between data plane and controllers.

Here are the spec for Flowvisor :
- OS : Ubuntu 14.04
- VCPU : 2
- RAM : 2GB
- Storage : 20GB

```bash
sudo apt install git openjdk-6-jdk -y
```
Make sure you install <em>build-essential</em>, <em>make</em> and <em>ant</em> after you install <em>openjdk-6</em>, or else ant and make will based on openjdk-7. What we need is openjdk-6.

```bash
sudo apt install build-essential ant make -y
```

```bash
sudo useradd -U -s /bin/bash -m flowvisor
sudo passwd flowvisor
sudo echo 'flowvisor ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/flowvisor
su - flowvisor
sudo echo 'flowvisor' >> /etc/flowvisor/flowvisor.passwd 
```

```bash
git clone https://github.com/opennetworkinglab/flowvisor.git
```

Install Flowvisor
```bash
cd flowvisor/ && sudo make install
```

Run Flowvisor
```bash
sudo /etc/init.d/flowvisor start
```

Check if Flowvisor is running, it will use port 8080, 8081, and 6633.
```bash
netstat -tulpn
```

Configure Flowvisor
```bash
fvctl set-config --enable-topo-ctrl
```

## How to Integrate Flowviser with Ryu

### 1. Ryu Monolith

To integrate to the Ryu Monolith Deployment, you can simply change the IP Address in flowvisor_slicing-monolith.py to your IP Address of the Ryu Monolith VM. You can use your text editor or simply use below command and change the ```<Your VM's IP For Ryu-Monolith>``` to your Ryu IP Address.

```bash
sed -i 's/10.0.1.125/<Your VM's IP For Ryu-Monolith>/g' flowvisor_slicing-monolith.py
```

### 2. Ryu Microservices

To integrate to the Ryu Microservices Deployment, you can simply change the IP Address in flowvisor_slicing-microservices.py to your Kubernetes Master Node IP Address as we implement NodePort in our services deployment. You can use your text editor or simply use below command and change the ```<Your VM's IP For Kubernetes Master Node>``` to your Ryu IP Address.

```bash
sed -i 's/10.0.0.241/<Your VM's IP For Kubernetes Master Node>/g' flowvisor_slicing-microservices.py
```

## How to Run the Flowvisor Script

You can simply use the below command.

### 1. Ryu Monolith

```bash
bash flowvisor_slicing-monolith.sh
```

### 2. Ryu Microservices

```bash
bash flowvisor_slicing-microservices.sh
```

## Remove Existing Flowvisor Slices

For efficiency purposes of changing from testing the integration of Monolith and Microservices deployment, we provide a script to remove existing Flowvisor Slices.

```bash
bash flowvisor_remove-slices.sh
```