FROM python:3.8-alpine
WORKDIR /usr/src/app

COPY ./requirements/requirements-apps.txt ./
COPY ./requirements/lib ./lib
RUN pip install --upgrade pip
RUN pip install --root-user-action=ignore requests
RUN pip install --no-cache-dir -r requirements-apps.txt

COPY ./slice/left/ryu_app.py .
COPY ./slice/left/env.py .

EXPOSE 8090

CMD ["python3", "./ryu_app.py"]