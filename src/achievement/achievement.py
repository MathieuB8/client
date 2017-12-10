import logging
logger = logging.getLogger(__name__)
from config import Settings

class Achievement():
    def __init__(self, state, value):
        self.state = state
        self.value = value
