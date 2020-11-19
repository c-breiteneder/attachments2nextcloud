import os
import datetime
from imap_tools import MailBox,AND
import owncloud
import shutil
import pytz
import configparser


config = configparser.ConfigParser()

config.read('config.ini')


config['Nextcloud']['server']
config['Nextcloud']['username']
config['Nextcloud']['password']
config['Nextcloud']['destination']


if os.path.isfile("lastrun.txt"):
    with open ("lastrun.txt",'r') as f:
        lastRun = f.readline()
        print ("Last Run: {0}".format(lastRun))
        lastRunDate = datetime.datetime.strptime(lastRun,("%Y-%m-%d %H:%M:%S"))
        lastRunTime = datetime.datetime.strptime(lastRun,("%Y-%m-%d %H:%M:%S"))
else:
    lastRunDate = datetime.date(1900,1,1)
    lastRunTime = datetime.time(0,0)

dateString = lastRun.split(" ")[0]
lastRunDate = datetime.date(int(dateString.split("-")[0]),int(dateString.split("-")[1]),int(dateString.split("-")[2]))

timeString = lastRun.split(" ")[1]
lastRunTime = datetime.time(int(timeString.split(":")[0]),int(timeString.split(":")[1]),int(timeString.split(":")[2]))

lastRunDateTime = datetime.datetime.combine(lastRunDate,lastRunTime)
nc = owncloud.Client(config['Nextcloud']['server'])
nc.login(config['Nextcloud']['username'], config['Nextcloud']['password'])

utc = pytz.utc

if os.path.isdir("tmp"):
    shutil.rmtree('tmp')

os.mkdir("tmp")

i = 0
with MailBox(config['IMAP']['server']).login(config['IMAP']['username'], config['IMAP']['password']) as mailbox:
    for msg in mailbox.fetch(AND(date_gte=lastRunDate)):
        if msg.date.replace(tzinfo=utc) > lastRunDateTime.replace(tzinfo=utc):
            for att in msg.attachments:
                if att.filename != "":
                    with open("tmp\\"+format(att.filename), 'wb') as f:
                        f.write(att.payload)
                        nc.put_file(config['Nextcloud']['destination']+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M_")+att.filename, "tmp//"+att.filename)
                        i = i+1

print ("{0} Files uploaded".format(i))

with open ("lastrun.txt",'w') as f:
    f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

shutil.rmtree('tmp')
nc.logout()