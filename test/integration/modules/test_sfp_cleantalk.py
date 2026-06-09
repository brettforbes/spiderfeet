import pytest
import unittest

from modules.sfp_cleantalk import sfp_cleantalk
from sflib import SpiderFeet
from spiderfeet import SpiderFeetEvent, SpiderFeetTarget


@pytest.mark.usefixtures
class TestModuleIntegrationcleantalk(unittest.TestCase):

    def test_handleEvent_event_data_safe_ip_address_not_blocked_should_not_return_event(self):
        sf = SpiderFeet(self.default_options)

        module = sfp_cleantalk()
        module.setup(sf, dict())

        target_value = 'spiderfeet.net'
        target_type = 'INTERNET_NAME'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        module.opts['_fetchtimeout'] = 15
        module.optdescs['_fetchtimeout'] = ''
        module.opts['_useragent'] = ''
        module.optdescs['_useragent'] = ''

        def new_notifyListeners(self, event):
            raise Exception(f"Raised event {event.eventType}: {event.data}")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_cleantalk)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        event_type = 'IP_ADDRESS'
        event_data = '1.0.0.1'
        event_module = 'example module'
        source_event = evt

        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)
        result = module.handleEvent(evt)

        self.assertIsNone(result)
