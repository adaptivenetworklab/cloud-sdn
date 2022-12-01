FROM python:3.8-alpine
WORKDIR /usr/src/app

COPY ofp_emitter.py .
COPY ofctl_rest.py .
COPY requirements.txt .

#RUN pip install ryu
RUN pip install -r requirements.txt

EXPOSE 8080
EXPOSE 6633

CMD ["ryu-manager", "ofp_emitter.py", "ofctl_rest.py"]
