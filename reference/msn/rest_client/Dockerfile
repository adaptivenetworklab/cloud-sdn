FROM python:3.8-alpine
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --root-user-action=ignore requests
RUN pip install --no-cache-dir -r requirements.txt

COPY lib ./lib
COPY simple_switch_rest.py .

EXPOSE 8090

CMD ["python", "./simple_switch_rest.py"]
