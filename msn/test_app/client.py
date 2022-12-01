import datetime
import requests
import json

start = datetime.datetime.now()
print('client start timestamp ', start)
r = requests.get(url="http://10.0.0.1:5000/")
data = r.json()
print(json.dumps(data))
stop = datetime.datetime.now()
print('client stop timestamp ', stop)
time_diff = (stop - start)
ex_time = time_diff.total_seconds() * 1000
print('execution time + network ', ex_time)
