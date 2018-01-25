"""
Support for Linky.
For more details about this component, please refer to the documentation at
http://github.com/tiste/roost/custom_components/linky.py/
"""
import logging
import json
import voluptuous as vol

from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['pylinky==0.1.3']
_LOGGER = logging.getLogger(__name__)

DOMAIN = 'linky'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    from pylinky.client import LinkyClient
    client = LinkyClient(username, password)

    try:
        client.fetch_data()
    except BaseException as exp:
        _LOGGER.error(exp)
    finally:
        client.close_session()

    _LOGGER.info(json.dumps(client.get_data(), indent=2))

    add_devices([LinkySensor('Linky', {})], True)

class LinkySensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, name, linky_data):
        self._name = name
        self._linky_data = linky_data
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'kWh'

    def update(self):
        """Fetch new state data for the sensor."""
        self._state = 23