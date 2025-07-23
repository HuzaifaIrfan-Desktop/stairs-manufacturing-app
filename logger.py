
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

assembly_logger=logging.getLogger("assembly")
assembly_logger.setLevel(logging.INFO)  # Or DEBUG if needed
handler=logging.FileHandler('log/assembly.log',mode="a")
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'))
handler.formatter.converter=time.gmtime
assembly_logger.addHandler(handler)

job_logger=logging.getLogger("job")
job_logger.setLevel(logging.INFO)  # Or DEBUG if needed
handler=logging.FileHandler('log/job.log',mode="a")
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'))
handler.formatter.converter=time.gmtime
job_logger.addHandler(handler)


ezdxf_logger=logging.getLogger("ezdxf")
ezdxf_logger.setLevel(logging.INFO)  # Or DEBUG if needed
handler=logging.FileHandler('log/ezdxf.log',mode="a")
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'))
handler.formatter.converter=time.gmtime
ezdxf_logger.addHandler(handler)



# Suppress ezdxf logs
logging.getLogger("ezdxf").setLevel(logging.CRITICAL)
logging.getLogger("PIL").setLevel(logging.CRITICAL)
logging.getLogger("fontTools").setLevel(logging.CRITICAL)
