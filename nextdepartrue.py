import requests
import json
from datetime import datetime
from datetime import timedelta
import getStopInfo

#MAY HAVE TIMEZONE PROBLEM IF USE VPN, i don't know

def crawlStopDeparture(stopNo, routeNo):
    resp = requests.get("https://www.octranspo.com/next_trips/next_trips?stop_id=" + stopNo + "&route_id=" + routeNo)
    return resp.json()

def promptInput(string):
    print(string)
    return input()

def nestedList(list):
    list = [' '.join([str(i) for i in j]) for j in list]
    list = '\n'.join(list)
    return list

def getNextDeparture(stopNo, routeNo):
    result = crawlStopDeparture(stopNo, routeNo)
    current_time = datetime.now()
    nextDeparture = []
    
    if result['GetNextTripsForStopResult']['StopLabel'] == '':
        return 'invalid stop number'
    routeDirection = result['GetNextTripsForStopResult']['Route']['RouteDirection']
    if type(routeDirection) is dict and routeDirection['RouteNo']=='':
        return 'invalid route number or no service'
    
    if type(routeDirection) is list:
        trips = []
        for i in routeDirection:
            trips += i['Trips']['Trip']
    else:
        trips = routeDirection['Trips']['Trip']
    
    for trip in trips:
        departureTime = current_time + timedelta(minutes=int(trip['AdjustedScheduleTime']))
        departureTime= departureTime.strftime("%H:%M")
        if trip['GPSSpeed'] != '':
            departureTime += '*'
        destination = trip['TripDestination']
        nextDeparture.append([departureTime, destination])
    return nestedList(nextDeparture)

def main():
    stopNo = promptInput("input stop No :")
    routeNo = promptInput("input route No :")

    88
    #stoplabel = getStopInfo.searchStopByNumber(stopNo)
    stoplabel = getStopInfo.searchStopByName("baseline")
    
    #nextDeparture = getNextDeparture(stopNo, routeNo)
    print(stoplabel)
    #print(nextDeparture)

main()