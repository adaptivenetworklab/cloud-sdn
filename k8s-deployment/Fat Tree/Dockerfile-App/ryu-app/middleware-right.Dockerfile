FROM python:3.8-alpine
WORKDIR /usr/src/app

COPY ./requirements/requirements-middleware.txt .

#RUN pip install ryu 
RUN pip install --upgrade pip
RUN pip install --root-user-action=ignore requests
RUN pip install -r requirements-middleware.txt

COPY ./slice/right/middleware.py .

EXPOSE 8080
EXPOSE 10003

CMD ["ryu-manager", "middleware", "--ofp-tcp-listen-port", "10003"]