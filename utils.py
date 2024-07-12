import logging

CURRENT_REGION = "Калининградская обл."

logger = logging.getLogger("app.log")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
