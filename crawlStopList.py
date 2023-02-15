import requests
import csv

def matchStationPerfix(string1,string2):
    temp = ""
    for i in range(len(string1)):
        if string1[i] == string2[i]:
            temp +=string1[i]
        else:
            break
    
    return temp.rstrip()


# crawl url with json format from website, return it into a dictionary format
def jsonToDict(url):
    resp = requests.get(url)
    return resp.json()

# convert stop list info into a csv file
def csvStopList():
    stops = jsonToDict('https://www.octranspo.com/route/map_data?type=stops')
    
    stations = jsonToDict('https://www.octranspo.com/route/map_data?type=stations')
    rev_dic ={}
    for station in stations:
        if station['info'] in rev_dic.keys():
            rev_dic[station['info']] = matchStationPerfix(rev_dic[station['info']],station['name'])
        else:
            rev_dic[station['info']] = station['name']

    for station in stations:
        if station['info'] in rev_dic.keys():
            station['station_name'] = rev_dic[station['info']]

    fields = ['stop_id', 'info', 'name','station_name']
    new_header= {'stop_id':'stop_id','info':'stop_no','name':'stop_name','station_name':'station_name'}
    with open('stop_info.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames = fields, extrasaction='ignore')
        w.writerow(new_header) #change header 
        w.writerows(stations)
        w.writerows(stops)
    f.close()

def main():
    csvStopList()

main()