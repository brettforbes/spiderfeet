import pytest
import unittest

from modules.sfp_webframework import sfp_webframework
from sflib import SpiderFeet
from spiderfeet import SpiderFeetEvent, SpiderFeetTarget


@pytest.mark.usefixtures
class TestModuleWebFramework(unittest.TestCase):

    def test_opts(self):
        module = sfp_webframework()
        self.assertEqual(len(module.opts), len(module.optdescs))

    def test_setup(self):
        sf = SpiderFeet(self.default_options)
        module = sfp_webframework()
        module.setup(sf, dict())

    def test_watchedEvents_should_return_list(self):
        module = sfp_webframework()
        self.assertIsInstance(module.watchedEvents(), list)

    def test_producedEvents_should_return_list(self):
        module = sfp_webframework()
        self.assertIsInstance(module.producedEvents(), list)

    def test_handleEvent_event_data_web_content_containing_webframework_string_should_create_url_web_framework_event(self):
        sf = SpiderFeet(self.default_options)

        module = sfp_webframework()
        module.setup(sf, dict())

        target_value = 'spiderfeet.net'
        target_type = 'INTERNET_NAME'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            expected = 'URL_WEB_FRAMEWORK'
            if str(event.eventType) != expected:
                raise Exception(f"{event.eventType} != {expected}")

            expected = "Wordpress"
            if str(event.data) != expected:
                raise Exception(f"{event.data} != {expected}")

            raise Exception("OK")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_webframework)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        event_type = 'TARGET_WEB_CONTENT'
        event_data = 'example data /wp-includes/ example data'
        event_module = 'sfp_spider'
        source_event = evt
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)
        evt.actualSource = "https://spiderfeet.net/"

        with self.assertRaises(Exception) as cm:
            module.handleEvent(evt)

        self.assertEqual("OK", str(cm.exception))

    def test_handleEvent_event_data_web_content_not_containing_webframework_string_should_not_create_event(self):
        sf = SpiderFeet(self.default_options)

        module = sfp_webframework()
        module.setup(sf, dict())

        target_value = 'spiderfeet.net'
        target_type = 'INTERNET_NAME'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            raise Exception(f"Raised event {event.eventType}: {event.data}")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_webframework)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        event_type = 'TARGET_WEB_CONTENT'
        event_data = 'example data'
        event_module = 'example module'
        source_event = evt
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)
        evt.actualSource = "https://spiderfeet.net/"

        result = module.handleEvent(evt)

        self.assertIsNone(result)

    def test_handleEvent_event_data_web_content_from_external_url_containing_webframework_string_should_not_create_event(self):
        sf = SpiderFeet(self.default_options)

        module = sfp_webframework()
        module.setup(sf, dict())

        target_value = 'spiderfeet.net'
        target_type = 'INTERNET_NAME'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            raise Exception(f"Raised event {event.eventType}: {event.data}")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_webframework)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        event_type = 'TARGET_WEB_CONTENT'
        event_data = 'example data /wp-includes/ example data'
        event_module = 'sfp_spider'
        source_event = evt
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)
        evt.actualSource = "https://externalhost.local/"

        result = module.handleEvent(evt)

        self.assertIsNone(result)
