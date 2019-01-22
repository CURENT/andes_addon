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
channel_andes = 'tcp://127.0.0.1:5566'
channel_pmu = 'ipc:///tmp/dime-pmu'


dimec1 = dime.Dime('PMU_broker', channel_andes)
dimec2 = dime.Dime('PMU_broker', channel_pmu)

try:
    dimec1.start()
except Exception:
    logger.error('Connection to ANDES DiME error')
logger.info('DiME 1 connected')

try:
    dimec2.start()
except Exception:
    logger.error('Connetion to PMU DiME error')
logger.info('DiME 2 connected')

ws1 = dimec1.workspace
ws2 = dimec2.workspace

while True:
    var = dimec1.sync()

    if var:
        dimec2.broadcast(var, ws1[var])
        logger.debug('Forwarded variable <{}>'.format(var))