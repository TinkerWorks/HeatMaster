from thermostate.thermostate import Thermostate
from ConfigurationLoader.AutoGenerated import AutoGenerated
from tigger.trigger import Trigger

import logging

class ThermostateGroup(Trigger, AutoGenerated):

    def __init__(self, config = None):
        AutoGenerated.__init__(self)
        Trigger.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)

        print ("ThermostateGroup config: ", config)

        print (" ################# This is a thermostate GROUP START ############## ")
        self.children = self.loadItemization(config, Thermostate)

        self.registerCallback(self.children, self.propagate)

        print (" ################## This is a thermostate GROUP END ############### ")

    def __str__(self):
        return "Thermostate group to unify control"
