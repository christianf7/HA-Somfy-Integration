import requests
from typing import Any
from datetime import timedelta

from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)


class BasicHub:
    def __init__(self, host: str, hass="na") -> None:
        self.host = host
        self.hass = hass
        self.actions = 0
        self.blinds = self.get_blinds()

    def verify_connection(self):
        try:
            r = requests.get(f"http://{self.host}/verify", timeout=10000)
            _LOGGER.info("Verified connection to Somfy.")
            return r.status_code == 200
        except:
            return False

    def get_blinds(self):
        r = requests.get(f"http://{self.host}/blinds", timeout=10000)
        return r.json()

    def set_status(self, device, action):
        r = requests.get(
            f"http://{self.host}/{action}/{device}",
            timeout=60000,
        )

        return r.json()