import os
import datetime
from imap_tools import MailBox,AND
import owncloud
import shutil
import pytz

###### Configuration Mailserver ##############
imap_server = "<imap-server>"
email_user = "<imap-user>"
email_pass = "<imap-pass>"
##############################################

###### Configuration Nextcloud/Owncloud ######
nc_server ="<cloud-server>"
nc_user = "<cloud-user>"
nc_pass  = "<cloud-pass>"
nc_folder = "<path/to/destination>"
##############################################


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
nc = owncloud.Client(nc_server)
nc.login(nc_user, nc_pass)

utc = pytz.utc

if os.path.isdir("tmp"):
    shutil.rmtree('tmp')

os.mkdir("tmp")

i = 0
with MailBox(imap_server).login(email_user, email_pass) as mailbox:
    for msg in mailbox.fetch(AND(date_gte=lastRunDate)):
        if msg.date.replace(tzinfo=utc) > lastRunDateTime.replace(tzinfo=utc):
            for att in msg.attachments:
                if att.filename != "":
                    with open("tmp\\"+format(att.filename), 'wb') as f:
                        f.write(att.payload)
                        nc.put_file(nc_folder+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M_")+att.filename, "tmp//"+att.filename)
                        i = i+1

print ("{0} Files uploaded".format(i))

with open ("lastrun.txt",'w') as f:
    f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

shutil.rmtree('tmp')
nc.logout()