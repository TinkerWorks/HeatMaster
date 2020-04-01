from temperature.temperature import Temperature
import datetime;
import requests as req
import sched, time

class DaikinTemperature(Temperature):

    def __init__(self, host = None, updateFunc = None, pollrate=15):
        self.host_ = host
        self.temperature_ = float('nan')
        self.updateFunc_ = updateFunc
        self.pollrate_ = pollrate
        self.sensors = {}

        if(host is not None):
            self.startPolling()

    def setHost(self, host):
        self.host_ = host
        self.startPolling()


    def loadConfig(self, config):
        print(config)

        classFinder = {"host": self.setHost}

        for k,v in config.items():
            print (" Key: ", k, " v ", v)
            keyClass = classFinder[k]
            print (keyClass)

            o = keyClass(v)
            #.loadConfig(v)

    def startPolling(self):
        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(self.pollrate_, 1, self.scheduledUpdate)
        self.s.run()

    def interrogate(self):
        url = 'http://' + self.host_ + "/aircon/get_sensor_info"
        headers = {'Host': self.host_ }
        r = req.get(url, headers=headers)
        return r

    def parseSensor(self, response):
        split = response.split(",")
        #print (split)

        for sensor in split:
            k, v = sensor.split("=")
            print ("Entry ", k, " is ", v)

            self.sensors[k] = v

    def scheduledUpdate(self):
        self.updateTemperature()
        self.s.enter(self.pollrate_, 1, self.scheduledUpdate)

    def updateTemperature(self):
        response = self.interrogate()
        self.parseSensor(response.text)
        self.temperature_ = self.sensors['htemp']
        self.timestamp_ = datetime.datetime.now().timestamp()

        if (self.updateFunc_ is not None):
            self.updateFunc_()

    def get(self):
        return self.temperature_

    def getTime(self):
        return self.timestamp_ini


if __name__ == "__main__":
    host = '10.10.31.61'
    port = 80

    def updatefunc():
        print ("needchangenow !!\n")

    m1 = DaikinTemperature(host, pollrate=1, updateFunc = updatefunc)


    while True:
        import time

        print("Temperature 1 is ", m1.get())

        time.sleep(30)
