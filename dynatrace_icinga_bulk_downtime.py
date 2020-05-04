#!/usr/bin/python
import sys
import subprocess
import time
import subprocess import Popen, PIPE
import datetime
import random
import requests
import json


list = []

# Part1 - Icinga

duration=sys.argv[1]
comments=sys.argv[2]
filename="text.txt"

# Below vairables for Dynatrace to convert into seconds into right datetime Human readable format

duration_in_seconds = int(duration)

# Below variabels is calling a SHELL script writeen for creating downtime in ICINGA and using in PYTHON they are splitted using SHLEX module via PYTHON CLI CONSOLE
session = subprocess.Popen(['/adshome/aanatha/silver_downtime' , '-f', filename, '-d', duration, '-c', comments], stdout=PIPE,stderr=PIPE)
stdout, stderr = session.communicate()



# part 2 - Dynatrace


# PUtting all the ICINGA hostnames in a list in variable "host"

with open("text.txt","r") as file:
    host = file.read().splitlines()


# Capturing USER ID details


user_session = subprocess.Popen(['whoami'], stdout=PIPE, stderr=PIPE)
stdout, stderr = user_session.communicate()
user_ids = stdout.rstrip() 
user_ids_ic = "icinga" # After userid , call user id like "aanatha_icinga_12" with some random number so that Downtime is not overriden, rather it creates a new downtime in DYNA and dont override existing one.

id_random = random.choice([1,2,3,4,5,6,7,8,9,10,11,12])
id_randoms = str("{}_{}_{}".format(user_ids,user_ids_ic,id_random))

def dyna():
    token="adsfasXwer34213DDS" # need to get from DYna tool
    headers = {'Authorization':'Api-Token adsfasXwer34213DDS'}
    r = requests.get('https://dyntrace.com/752143.210.0-35120/api/v1/entity/infrastructure/hosts', headers=headers, verify=False)
    j = json.loads(r.text)
    with open ("hello.txt","w") as f:
        json.dump(j,f, indent=4) # THis is dumping the "j" variable results in JSON format in file


# part 2
    with open("hello.txt","r") as file:
        data = json.load(file)
        name = str(p['displayName'])
        ent = p['entity']
        for i in name:
            if i in name:
                list.append(ent)


    return list


entity = dyna() #Storing as object
normal_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

###############################################
# To convert Duration in minutes to DATEIME object in Python
# ALmst spent 2 hours, Below variables are all for future time
#####################################

duration_in_seconds_to_minutes = duration_in_secs * 60
future = time.time() + duration_in_seconds_to_minutes
a = time.ctime(future)

# Very important
# converting the output format so that it can be passed to "Dateime.datetime" object

format = '%a %b %d %H:%M%S %Y'
datetime_str = datetime.datetime.strptime(a,format)
normal_end_time = datetime_str.strftime('%Y-%m-%d %H:%M')


payload = { 'id' : id_randoms, 'type' : 'Planned', 'description': 'Nagios all donw', 'uppressAlerts': 'False', 'upressProblems''False', 'scope': '{ 'entities' : entity, 'matches' : [] }, 'schedule': { 'type': 'Once', 'timezoneId': 'America/Pheonix', 'maintenanceStart': normal_start_time, 'maintenanceEnd': normal_end_time } }

headers { 'Authorization' : 'Api-Token xasdnasdfasdf', 'content-type': 'application/json' }

r_last = requests.post{'https://dynatrace.com/e/asdfadsf-1234234-asdf/api/v1/maintenance', data=json.dumps(payload), headers=headers, verify=False)
