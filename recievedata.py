import requests
import json
import time
import os
try:
    x = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo')
    json_obj = json.loads(x.text)
    vartime=time.time()
    # timestamp={"timestamp":vartime}
    # timestamp.update(json_obj)
    try:
        os.mkdir('data')
    except:
        pass
    with open('data/'+str(vartime)+' marketdata.json', 'w+') as outfile:
        json.dump(json_obj, outfile)
except Exception as e:
        f=open('Exception marketdata.txt', 'a+')
        f.writelines(e)
        f.close()