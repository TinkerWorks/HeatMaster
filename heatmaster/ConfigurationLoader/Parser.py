import json
import sys


class Parser:
    def __init__(self, configurationFilename):
        self.loadConfigurationFile(configurationFilename)

    def loadConfigurationFile(self, configurationFilename):
        with open(configurationFilename) as json_file:
            self.data = json.load(json_file)

    def getConfiguration(self):
        return self.data

    def populateThermostates(self, generatorFunction=None):
        print('')
        print('')

        for p in self.data['thermostates']:
            print('Name: ' + p['name'])
            try:
                print('Relay: ' + p['relay'])
            except KeyError as e:
                print("No key ", e)

            temperature = p['temperature']
            print('Temperature Type: ' + temperature['type'])
            if (temperature['type'] == 'mqtt'):
                print('Temperature Topic: ' + temperature['topic'])
            elif (temperature['type'] == 'daikin'):
                print('Temperature Host: ' + temperature['host'])

            print('')
        print('')

    def populateMqtt(self, generatorFunction=None):
        mqttBroker = self.data['mqtt']
        host = mqttBroker['host']
        port = mqttBroker['port']

        print('')
        print('')
        print("Mqtt server at ", host, " : ", port)
        print('')
        print('')

        if (generatorFunction is not None):
            generatorFunction(host, port)

            
if __name__ == "__main__":
    confFile = sys.argv[1]

    print(confFile)

    ps = Parser(confFile)

    def thermostateGenerator():
        print("thermostateGenerator")

    def mqttGenerator(host, port):
        print("mqttGenerator")

    ps.populateMqtt(mqttGenerator)
    ps.populateThermostates(thermostateGenerator)
