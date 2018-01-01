#!/usr/bin/env python2.7  
# tweetpic.py take a photo with the Pi camera and tweet it  
# by Alex Eames http://raspi.tv/?p=5918  
import tweepy  
from subprocess import call  
from datetime import datetime  
   
i = datetime.now()               #take time and date for filename  
now = i.strftime('%Y%m%d-%H%M%S')  
photo_name = now + '.jpg'  
cmd = 'raspistill -t 500 -w 1024 -h 768 -o /home/pi/' + photo_name   
call ([cmd], shell=True)         #shoot the photo

tempfile = open("/sys/bus/w1/devices/28-0416b116e1ff/w1_slave")
thetext = tempfile.read()
tempfile.close()
tempdata = thetext.split("\n")[1].split(" ")[9]
temperature = float(tempdata[2:])
temperature = temperature / 1000
  
# Consumer keys and access tokens, used for OAuth  
consumer_key = 'x2INWyStWy1PuE6yzReaNV0m4'
consumer_secret = 'SPZwsRZdb2SITLwDM72raECVo3mZErnJUMgfOjsmjSTAQmSqQd'
access_token = '47786667846402048-lDyVbdYjcLOk2QjKMTN7I4v36eRm9Lv'
access_token_secret = 'SYukMDyfFDU80dWEk6Cupi1QFhgHueAXYgVE03iTXVzR6'
  
# OAuth process, using the keys and tokens  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)  
   
# Creation of the actual interface, using authentication  
api = tweepy.API(auth)  
  
# Send the tweet with photo  
photo_path = '/home/pi/' + photo_name  
status = 'Aquarium temperature: ' + temperature + i.strftime('%Y/%m/%d %H:%M:%S')
api.update_with_media(photo_path, status=status)
