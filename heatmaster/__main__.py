import sys
print ("PYTHONPATH is: {}".format(sys.path))

from heatmaster.ConfigurationLoader.Parser import Parser
from heatmaster.heatmaster import HeatMaster


confFile = sys.argv[1]

ps = Parser(confFile)
hm = HeatMaster(config=ps.getConfiguration())
hm.run(5)
