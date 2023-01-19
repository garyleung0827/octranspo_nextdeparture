import telebot
import requests
import json
from datetime import datetime
from datetime import timedelta
import re

BOT_TOKEN = '5856206717:AAEKxZ85GK4oLwCiiLYBfbbycqqWbtlqttQ'
bot = telebot.TeleBot(BOT_TOKEN)

# get oc transpo url
def geturl(stopNo, routeNo):
    return "https://www.octranspo.com/next_trips/next_trips?stop_id=" + stopNo + "&route_id=" + routeNo
# crawl text from the url and return into dictionary format
def crawler(url):
    resp = requests.get(url)
    result = json.loads(resp.text)
    return result

def nestedList(list):
    list = [' '.join([str(i) for i in j]) for j in list]
    list = '\n'.join(list)
    return list

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



@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id,'To find Bus Station, press /station')
    
@bot.message_handler(commands=['help'])
def exchange_command(message):
    bot.send_message(message.chat.id, '/s [stop number] - could tell you the station name\n eg. /s 0705')
    bot.send_message(message.chat.id, '/n [stop number] [route number] - could tell you the next departure time at the station\n eg. /n 0705 88')


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if re.match(r'^/s \d+$',message.text):
        stop = re.findall(r'^/s (\d+)$',message.text)
        bot.reply_to(message, getStopLabel(stop[0]))

    if re.match(r'^/n (\d+) (\d+)$',message.text):
        info = re.findall(r'^/n (\d+) (\d+)$',message.text)
        nextDeparture = getNextDeparture(info[0][0], info[0][1])
        bot.reply_to(message, nextDeparture)


bot.infinity_polling()