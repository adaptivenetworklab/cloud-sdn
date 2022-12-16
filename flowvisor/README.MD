# How to Install Flowvisor

There are two architecture we use to run Flowvisor, Monolith Architecture and Microservices Architecture. For monolith we use a Virtual Machine (VM) and for microservice we'll use a Kubernetes environment cluster.

Here are the spec for Flowvisor :
- OS : Ubuntu 14.04
- VCPU : 4
- RAM : 4GB
- Storage : 10GB

<em>Above spec will change accordingly as we test and research our scenario</em>

## 1. Monolith

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

## 2. Microservices

We use Docker and Kubernetes for this microservices architecture installation.

```bash
git clone https://github.com/opennetworkinglab/flowvisor.git
```

```bash
docker build -f Dockerfile -t flowvisor .
```
```bash
docker images
```

Upload flowvisor image to your own Registry (Docker Hub or your own Private Registry)
```bash
nano ../manifest/flowvisor-deployment.yaml
```
Change above YAML Kubernetes deploymen accordingly.
```bash
kubectl apply -f ../manifest/flowvisor-deployment.yaml
```