FROM python:3.8-alpine
WORKDIR /usr/src/app

COPY ./requirements-apps.txt ./
RUN pip install --upgrade pip
RUN pip install --root-user-action=ignore requests
RUN pip install --no-cache-dir -r requirements-apps.txt

COPY ./lib ./lib
COPY ./center-slice.py .

EXPOSE 8090

CMD ["python", "./center-slice.py"]