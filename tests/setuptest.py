#!/usr/bin/env python3

import sys

from mock import Mock
if 'RPi' not in sys.modules.keys():
    sys.modules['RPi'] = Mock()
if 'RPi.GPIO' not in sys.modules.keys():
    sys.modules['RPi.GPIO'] = Mock()

from heatmaster.actuators.electrovalve import Electrovalve
Electrovalve.OPEN_TIME_SECONDS = 1
Electrovalve.CLOSE_TIME_SECONDS = 2
