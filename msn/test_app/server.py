import datetime
from flask import Flask

app = Flask(__name__)


@app.route('/')
def get_services():
    start = datetime.datetime.now()
    print('server start timestamp ', start)
    return {
        "service": "service1",
    }


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

