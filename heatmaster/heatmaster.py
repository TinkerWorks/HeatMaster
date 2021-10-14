from heatmaster.ConfigurationLoader.AutoGenerated import AutoGenerated

from heatmaster.thermostate.thermostategroup import ThermostateGroup
from heatmaster.temperature.mqttproxy import MqttProxy
from heatmaster.heater.heater import Heater
from heatmaster.utils.trigger import Trigger

from signal import signal, SIGINT, SIGTERM
from threading import Event
import time

from heatmaster.utils import logging
logger = logging.getLogger(__name__)


class HeatMaster(Trigger, AutoGenerated):

    def __init__(self, config=None):
        AutoGenerated.__init__(self)
        Trigger.__init__(self)

        logger.success("Starting HeatMaster ...")
        self.initialize_stop()  # initialize stop here so we are prepared

        self.recalculateEvent = Event()

        self.start_time = None

        self.classFinder = {
            "mqtt": MqttProxy.initializeConfig,
            "thermostates": ThermostateGroup,
            "heater": Heater}
        logger.info(self.classFinder)

        if(config):
            self.children = self.loadConfig(config)

        self.registerCallback(self.children, self.recalculateTrigger)

        logger.warning("-"*16 + " INSPECT START TIME " + "-"*16)
        self.inspect(True)
        logger.warning("-"*16 + " INSPECT END TIME " + "-"*16)

    def stop_everything(self, signal_received, frame) -> None:
        self.stop_event.set()

    def initialize_stop(self):
        self.stop_event = Event()
        signal(SIGINT, self.stop_everything)
        signal(SIGTERM, self.stop_everything)

    def recalculateTrigger(self, chain, arg):
        logger.notice("trigger recalculation because of %s" % chain)
        self.recalculateEvent.set()

    def timeDeadline(self, deadline):
        if self.start_time is None:
            self.start_time = time.time()

        return (deadline == 0 or time.time() < self.start_time + deadline)
        
    def run(self, timeout_seconds=0):
        while self.timeDeadline(timeout_seconds) and not self.stop_event.is_set():
            self.recalculateEvent.wait(10)
            logger.info("!"*20 + " Woken up " + "!"*20)
            self.recalculateEvent.clear()

        self.sendstop()

    def stop(self):
        pass
