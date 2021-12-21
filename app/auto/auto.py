import json
import time
from datetime import datetime, timedelta

import numpy as np
import requests
import schedule
from flask import Flask


app = Flask(__name__, template_folder='../../templates')

flag: bool = True
@app.route("/")
def auto():
    global flag
    count = 0
    endtime = datetime.now() + timedelta(seconds=300)
    while flag:
        if datetime.now() > endtime:
            flag = False
        count += 1
        url = "http://192.168.100.63:5004"
        schedule.every(5).seconds.do(change)
        res = requests.get(url=url)
        schedule.run_pending()
        # time.sleep(0.01)
        print(count)
    rrr = "success"
    return rrr

def change():
    url = "http://192.168.100.63:5004/change"
    res = requests.get(url=url)





# url = "http://192.168.100.63:5004/kirikae"
#         res = requests.post(url=url)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=82)