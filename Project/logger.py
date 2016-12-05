import datetime, json, smtplib
from email.mime.text import MIMEText

class Logger:
    def __init__(self,username,softwareVersion,domainFile):
        currentDateTime = datetime.datetime.now()
        timestamp = currentDateTime.strftime("%Y-%m-%d-%H_%M_%S")
        self.fileName=timestamp+"_"+username+".json"
        #TODO CHECK FILE EXISTENCE
        self._data={
            "date":{
                "day":currentDateTime.day,
                "month":currentDateTime.month,
                "year":currentDateTime.year
            },
            "username":username,
            "Software Version":softwareVersion,
            "domain":domainFile,
            "actions":[]
        }
        self._actionsRef=self._data["actions"]
        self.containsData=False

    def logAction(self, actionType, actionData):
        """
        writes action to log after inserting timestamp
        :param action:
        :return:
        """
        now=datetime.datetime.now()
        assert(type(actionData) is dict)
        action=actionData.copy()
        action["timestamp"]={
            "H":now.hour,
            "M":now.minute,
            "S":now.second,
            "ms":int(now.microsecond/1000),
            "time":now.strftime("%H:%M:%S.%f")
        }
        action["actionType"]=actionType
        self._actionsRef.append(action)
        self.containsData = True

    def sendEmail(self,username):
        fromaddr="ICcsresearch1@gmail.com"
        toaddr="ICcsresearch1@gmail.com"
        # msg = '''
        #     From: {}
        #     To: {}
        #     Subject: testin'
        #     This is a test
        #     .
        # '''.format(fromaddr,toaddr)
        msg=MIMEText(json.dumps(self._data,indent="\t"))
        msg["Subject"]="Data: {}".format(username)
        msg["From"]=fromaddr
        msg["To"]=toaddr
        try:
            server=smtplib.SMTP("smtp.gmail.com:587")
            server.ehlo()
            server.starttls()
            server.login("ICcsresearch1@gmail.com","E4h65*dL")
            #server.sendmail(fromaddr,toaddr,msg)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print("ERROR: Probably no internet connection\n",e)

    def saveForExit(self):
        _file = open("userdata/"+self.fileName, "w")
        json.dump(self._data, _file, indent="\t")
        _file.close()