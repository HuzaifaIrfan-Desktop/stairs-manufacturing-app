
import os
if not os.path.exists('log'):
    os.makedirs('log')

import logging
import time
# Configure logging
part_logger=logging.getLogger("part")
part_logger.setLevel(logging.INFO)  # Or DEBUG if needed
handler=logging.FileHandler('log/part.log',mode="a")
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'))
handler.formatter.converter=time.gmtime
part_logger.addHandler(handler)