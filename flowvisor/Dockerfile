FROM ubuntu:trusty

RUN sudo apt-get update && sudo apt-get upgrade -y
RUN sudo apt-get install openjdk-6-jdk python2.7 -y
RUN sudo apt-get install build-essential ant make -y
RUN sudo ln -s /usr/bin/python2.7 /usr/bin/python
RUN sudo useradd -U -s /bin/bash -p 123 -m flowvisor
RUN su - flowvisor

COPY flowvisor /home/flowvisor/
WORKDIR /home/flowvisor/
RUN sudo make fvuser=flowvisor fvgroup=flowvisor install

CMD ["sudo", "/etc/init.d/flowvisor", "start"]
 
