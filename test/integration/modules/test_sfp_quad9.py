import pytest
import unittest

from modules.sfp_quad9 import sfp_quad9
from sflib import SpiderFeet
from spiderfeet import SpiderFeetEvent, SpiderFeetTarget


@pytest.mark.usefixtures
class TestModuleIntegrationQuad9(unittest.TestCase):

    def test_handleEvent_event_data_safe_internet_name_not_blocked_should_not_return_event(self):
        sf = SpiderFeet(self.default_options)

        module = sfp_quad9()
        module.setup(sf, dict())

        target_value = 'spiderfeet.net'
        target_type = 'INTERNET_NAME'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            raise Exception(f"Raised event {event.eventType}: {event.data}")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_quad9)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        event_type = 'INTERNET_NAME'
        event_data = 'quad9.net'
        event_module = 'example module'
        source_event = evt

        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)
        result = module.handleEvent(evt)

        self.assertIsNone(result)
