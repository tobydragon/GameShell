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

    def sendEmail(self):
        msg = MIMEText("TESTING 123")
        msg["From"] = "benjaminwelsh2@gmail.com"
        msg["To"] = "benjaminwelsh2@gmail.com"
        msg["Subject"] = "test"
        server=smtplib.SMTP("smtp.gmail.com")
        server.send_message(msg)
        server.quit()

    def saveForExit(self):
        _file = open("userdata/"+self.fileName, "w")
        json.dump(self._data, _file, indent="\t")
        _file.close()