import time
import logging
from andes_addon import dime


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# define the TCP streaming channel
channel_andes = 'tcp://192.168.1.200:5000'
channel_pmu = 'ipc:///tmp/dime'


dimec1 = dime.Dime('PMU_broker', channel_andes)
dimec2 = dime.Dime('PMU_broker', channel_pmu)

try:
    logger.info('Connecting to {}'.format(channel_andes))
    dimec1.start()
except Exception:
    logger.error('Connection to ANDES DiME error')
logger.info('DiME 1 connected')

try:
    logger.info('Connecting to {}'.format(channel_pmu))
    dimec2.start()
except Exception:
    logger.error('Connetion to PMU DiME error')
logger.info('DiME 2 connected')

ws1 = dimec1.workspace
ws2 = dimec2.workspace

while True:
    var1 = dimec1.sync()
    var2 = dimec2.sync()

    if var1:
        dimec2.broadcast(var1, ws1[var1])
        logger.debug('1->2 variable <{}>'.format(var1))
        time.sleep(0.001)
    if var2:
        dimec1.broadcast(var2, ws2[var2])
        logger.debug('2->1 variable <{}>'.format(var2))
        time.sleep(0.001)
