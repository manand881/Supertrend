import json
import plotly.graph_objects as go

# loading file which contains json data got from recievedata.py

with open('data/1623583088.8387012 marketdata.json') as f:
    data = json.load(f)
    pairs = data["Time Series (5min)"].items()

# initializing variables for usage

timestampslist = list()
openlist = list()
highlist = list()
lowlist = list()
closelist = list()
volumelist = list()
highlowby2 = list()
upperbandbasic = list()
lowerbandbasic = list()
truerangelist = list()
multiplier = 3.3
days = 7
atrlist = [0]*days
upperband = [0]*100
lowerband = [0]*100
supertrend=[0]*100

# copying all the time stands to a list for sorting

for key, value in pairs:
    timestampslist.append(key)

# sorting json data by time

timestampslist.sort()
for x in timestampslist:
    dummylist = []
    openlist.append(data["Time Series (5min)"][x]["1. open"])
    highlist.append(data["Time Series (5min)"][x]["2. high"])
    lowlist.append(data["Time Series (5min)"][x]["3. low"])
    closelist.append(float(data["Time Series (5min)"][x]["4. close"]))
    volumelist.append(data["Time Series (5min)"][x]["5. volume"])
    upperbandbasic.append(((float((data["Time Series (5min)"][x]["2. high"]))-float(
        (data["Time Series (5min)"][x]["3. low"])))/2))
    lowerbandbasic.append(((float((data["Time Series (5min)"][x]["2. high"]))-float(
        (data["Time Series (5min)"][x]["3. low"])))/2))
    dummylist.append(float(data["Time Series (5min)"][x]["2. high"]) -
                     float(data["Time Series (5min)"][x]["3. low"]))
    dummylist.append(float(data["Time Series (5min)"][x]["2. high"]) -
                     float(data["Time Series (5min)"][x]["4. close"]))
    dummylist.append(float(data["Time Series (5min)"][x]["3. low"]) -
                     float(data["Time Series (5min)"][x]["4. close"]))
    truerangelist.append(max(dummylist))

# calculating ATR

z = 0
for x in range(days, len(truerangelist)):
    sum = 0
    for y in range(z, days+z):
        sum += truerangelist[y]
    z += 1
    atrlist.append(sum*(1/days))

# calculating upperband basic and lowerband basic

for x in range(0, len(lowerbandbasic)):
    try:
        lowerbandbasic[x] -= multiplier*atrlist[x]
        upperbandbasic[x] += multiplier*atrlist[x]
    except:
        lowerbandbasic[x] = 0
        upperbandbasic[x] = 0

# calculating upperband and lower band

for x in range(days, len(lowerbandbasic)):
    if ((upperbandbasic[x] < upperband[x-1]) or (closelist[x-1] > upperband[x-1])):
        upperband[x] = upperbandbasic[x]
    else:
        upperband[x] = upperband[x-1]

    if ((lowerbandbasic[x] > lowerband[x-1]) or (closelist[x-1] < lowerband[x-1])):
        lowerband[x] = lowerbandbasic[x]
    else:
        lowerband[x] = lowerband[x-1]

# calculating supertrend

for x in range(days, len(lowerband)):
    if((supertrend[x-1]==upperband[x-1])and(closelist[x]<upperband[x])):
        supertrend[x]=upperband[x]
    if((supertrend[x-1]==upperband[x-1])and(closelist[x]>upperband[x])):
        supertrend[x]=lowerband[x]
    if((supertrend[x-1]==lowerband[x-1])and(closelist[x]>lowerband[x])):
        supertrend[x]=lowerband[x]
    if((supertrend[x-1]==lowerband[x-1])and(closelist[x]<lowerband[x])):
        supertrend[x]=upperband[x]

# passing high low open and close data to plotly api to plot candlestick

fig = go.Figure(data=[go.Candlestick(x=timestampslist,
                                     open=openlist,
                                     high=highlist,
                                     low=lowlist,
                                     close=closelist)])

# adding title to graph from json values

fig.update_layout(
    title=data["Meta Data"]["1. Information"] +
    " for "+data["Meta Data"]["2. Symbol"],
)

# displaying graph in localhost

fig.show()