import logging

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s - %(message)s',
    level=logging.INFO
)

def info(msg):
    logging.info(msg)

def erro(msg):
    logging.error(msg)

def debug(msg):
    logging.debug(msg)
