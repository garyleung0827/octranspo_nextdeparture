import requests
import json
from datetime import datetime
from datetime import timedelta
import re

#MAY HAVE TIMEZONE PROBLEM IF USE VPN, i don't know

def geturl(stopNo, routeNo):
    return "https://www.octranspo.com/next_trips/next_trips?stop_id=" + stopNo + "&route_id=" + routeNo

def promptInput(string):
    print(string)
    return input()

def nestedList(list):
    list = [' '.join([str(i) for i in j]) for j in list]
    list = '\n'.join(list)
    return list

# crawl text from the url and return into dictionary format
def crawler(url):
    resp = requests.get(url)
    result = json.loads(resp.text)
    return result

def getStopLabel(stopNo):
    url = geturl(stopNo,'1')
    result = crawler(url)
    if result['GetNextTripsForStopResult']['StopLabel'] == '':
        return 'invalid stop number'
    stopLabel = result['GetNextTripsForStopResult']['StopLabel']
    return stopLabel

def getNextDeparture(stopNo, routNo):
    url = geturl(stopNo,routNo)
    result = crawler(url)
    current_time = datetime.now()
    nextDeparture = []
    if result['GetNextTripsForStopResult']['StopLabel'] == '':
        return 'invalid stop number'
    print(result['GetNextTripsForStopResult']['Route']['RouteDirection']['RouteNo'])
    if result['GetNextTripsForStopResult']['Route']['RouteDirection']['RouteNo'] == '':
        return 'invalid route number'
    
    trips = result['GetNextTripsForStopResult']['Route']['RouteDirection']['Trips']['Trip']
    for trip in trips:
        departureTime = current_time + timedelta(minutes=int(trip['AdjustedScheduleTime']))
        departureTime= departureTime.strftime("%H:%M")
        if trip['GPSSpeed'] != '':
            departureTime += '*'
        destination = trip['TripDestination']
        nextDeparture.append([departureTime, destination])
    return nextDeparture




def main():
    stopNo = promptInput("input stop No :")
    routeNo = promptInput("input route No :")

    stoplabel = getStopLabel(stopNo)
    nextDeparture = getNextDeparture(stopNo, routeNo)
    nextDeparture = nestedList(nextDeparture)
    print(stoplabel)
    print(nextDeparture)


main()