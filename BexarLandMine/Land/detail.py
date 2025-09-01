import logging

logger = logging.getLogger(__name__)


class Detail():
    def __init__(self):
        logger.debug("Detail instance created")

    def __repr__(self):
        return "Detail()"
