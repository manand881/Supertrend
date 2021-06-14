import requests
import json
import time
import os

# trying to get response from api. using try catch in case of connectivity issues

try:
    x = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo')
    json_obj = json.loads(x.text)
    vartime=time.time()
    try:
        os.mkdir('data')
    except:
        pass
    with open('data/'+str(vartime)+' marketdata.json', 'w+') as outfile:
        
        # storing response to file

        json.dump(json_obj, outfile)

except Exception as e:
        
        # recording exceptions 
        
        f=open('Exception marketdata.txt', 'a+')
        f.writelines(e)
        f.close()