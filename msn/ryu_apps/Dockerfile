FROM python:3.9.7
WORKDIR /usr/src/app

COPY ofp_emitter.py .
COPY ofctl_rest.py .
COPY requirements.txt .

#RUN pip install ryu 
RUN pip install --upgrade pip
RUN apt-get update -y && \ apt-get install -y python-pip python-dev
RUN pip install -r requirement.text

EXPOSE 8080
EXPOSE 6633

CMD ["ryu-manager", "ofp_emitter.py", "ofctl_rest.py"]
