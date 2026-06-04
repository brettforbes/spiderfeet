import pytest
import unittest

from modules.sfp_names import sfp_names
from sflib import SpiderFeet
from spiderfeet import SpiderFeetEvent, SpiderFeetTarget


@pytest.mark.usefixtures
class TestModuleNames(unittest.TestCase):

    def test_opts(self):
        module = sfp_names()
        self.assertEqual(len(module.opts), len(module.optdescs))

    def test_setup(self):
        sf = SpiderFeet(self.default_options)
        module = sfp_names()
        module.setup(sf, dict())

    def test_watchedEvents_should_return_list(self):
        module = sfp_names()
        self.assertIsInstance(module.watchedEvents(), list)

    def test_producedEvents_should_return_list(self):
        module = sfp_names()
        self.assertIsInstance(module.producedEvents(), list)

    def test_handleEvent_event_data_email_address_containing_human_names_should_return_event(self):
        sf = SpiderFeet(self.default_options)

        module = sfp_names()
        module.setup(sf, dict())

        target_value = 'spiderfeet.net'
        target_type = 'INTERNET_NAME'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            expected = 'HUMAN_NAME'
            if str(event.eventType) != expected:
                raise Exception(f"{event.eventType} != {expected}")

            expected = "Firstname Lastname"
            if str(event.data) != expected:
                raise Exception(f"{event.data} != {expected}")

            raise Exception("OK")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_names)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        event_type = 'EMAILADDR'
        event_data = 'firstname.lastname@spiderfeet.net'
        event_module = 'example module'
        source_event = evt
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        with self.assertRaises(Exception) as cm:
            module.handleEvent(evt)

        self.assertEqual("OK", str(cm.exception))

    def test_handleEvent_event_data_email_address_containing_human_names_containing_numbers_should_not_return_event(self):
        sf = SpiderFeet(self.default_options)

        module = sfp_names()
        module.setup(sf, dict())

        target_value = 'spiderfeet.net'
        target_type = 'INTERNET_NAME'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            raise Exception(f"Raised event {event.eventType}: {event.data}")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_names)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        event_type = 'EMAILADDR'
        event_data = 'firstname.lastname1@spiderfeet.net'
        event_module = 'example module'
        source_event = evt
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        result = module.handleEvent(evt)

        self.assertIsNone(result)

    def test_handleEvent_event_data_email_address_not_containing_names_should_not_return_event(self):
        sf = SpiderFeet(self.default_options)

        module = sfp_names()
        module.setup(sf, dict())

        target_value = 'spiderfeet.net'
        target_type = 'INTERNET_NAME'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            raise Exception(f"Raised event {event.eventType}: {event.data}")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_names)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        event_type = 'EMAILADDR'
        event_data = 'lastname@spiderfeet.net'
        event_module = 'example module'
        source_event = evt
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        result = module.handleEvent(evt)

        self.assertIsNone(result)
