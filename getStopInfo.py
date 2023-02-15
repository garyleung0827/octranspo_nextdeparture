import re
import csv

#problem to solve
#1. french character wait to solve

# search stop by stop name, return a list of posssible stop
def searchStopByName(Stop_Name):
    stopList = []
    with open('stop_info.csv','r', newline='') as f:
        stops = csv.DictReader(f)
        for stop in stops:
            if re.search(Stop_Name, stop['stop_name'], re.IGNORECASE) and stop['station_name'] == "":
                    stopList.append({'stop_no': stop['stop_no'], 'stop_name': stop['stop_name']})
            if re.search(Stop_Name, stop['station_name'], re.IGNORECASE):
                if {'stop_no': stop['stop_no'], 'stop_name': stop['station_name']} not in stopList:
                    stopList.append({'stop_no': stop['stop_no'], 'stop_name': stop['station_name']})
    return stopList

# search stop by stop number, return a list of posssible stop
def searchStopByNumber(stop_No):
    stopList = []
    with open('stop_info.csv','r', newline='') as f:
        stops = csv.DictReader(f)
        for stop in stops:
            if re.search(stop_No, stop['stop_no'], re.IGNORECASE):
                stopList.append(stop)
    return stopList