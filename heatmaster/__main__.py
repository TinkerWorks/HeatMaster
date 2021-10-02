from ConfigurationLoader.Parser import Parser
from heatmaster import HeatMaster

import os

absFilePath = os.path.abspath(__file__)
path, filename = os.path.split(absFilePath)
confFile = path + "/../data/config.json"

ps = Parser(confFile)
hm = HeatMaster(config=ps.getConfiguration())
hm.run(5)
