FROM ubuntu:14.04

RUN sudo apt-get update && sudo apt-get upgrade -y
RUN sudo apt-get install openjdk-6-jdk python2.7 -y
RUN sudo apt-get install build-essential ant make git -y
RUN sudo ln -s /usr/bin/python2.7 /usr/bin/python
RUN sudo useradd -U -s /bin/bash -m flowvisor
RUN echo 'root:123' | chpasswd
RUN echo 'flowvisor:123' | chpasswd
RUN echo 'flowvisor ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/flowvisor

COPY flowvisor/ /home/flowvisor
WORKDIR /home/flowvisor
RUN sudo make install
USER flowvisor:flowvisor

RUN fvconfig generate /etc/flowvisor/config.json flowvisor flowvisor
RUN echo "flowvisor" > /etc/flowvisor/flowvisor.passwd

RUN chown flowvisor:flowvisor /etc/flowvisor/flowvisor.passwd

RUN fvconfig load /etc/flowvisor/config.json

EXPOSE 8081
EXPOSE 8080
EXPOSE 6633

COPY ./flowvisor_slicing.sh .

CMD ["bash", "./flowvisor_slicing.sh"]
