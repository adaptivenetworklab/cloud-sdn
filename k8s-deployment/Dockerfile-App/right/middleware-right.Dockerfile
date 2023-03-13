FROM python:3.8-alpine
WORKDIR /usr/src/app

COPY ./requirements-middleware.txt .

#RUN pip install ryu 
RUN pip install --upgrade pip
RUN pip install --root-user-action=ignore requests
RUN pip install -r requirements-middleware.txt

COPY ./ofp_emitter.py .
COPY ./ofctl_rest.py .

EXPOSE 8080
EXPOSE 10003

CMD ["ryu-manager", "ofp_emitter.py", "ofctl_rest.py", "--ofp-tcp-listen-port", "10003"]