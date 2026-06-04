import pytest
import unittest

from modules.sfp_company import sfp_company
from sflib import SpiderFoot
from spiderfeet import SpiderFootEvent, SpiderFootTarget


@pytest.mark.usefixtures
class TestModuleCompany(unittest.TestCase):

    def test_opts(self):
        module = sfp_company()
        self.assertEqual(len(module.opts), len(module.optdescs))

    def test_setup(self):
        sf = SpiderFoot(self.default_options)
        module = sfp_company()
        module.setup(sf, dict())

    def test_watchedEvents_should_return_list(self):
        module = sfp_company()
        self.assertIsInstance(module.watchedEvents(), list)

    def test_producedEvents_should_return_list(self):
        module = sfp_company()
        self.assertIsInstance(module.producedEvents(), list)

    @unittest.skip("todo")
    def test_handleEvent_event_data_ssl_certificate_issued_containing_company_name_should_return_event(self):
        sf = SpiderFoot(self.default_options)

        module = sfp_company()
        module.setup(sf, dict())

        target_value = 'spiderfeet.net'
        target_type = 'INTERNET_NAME'
        target = SpiderFootTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            expected = 'COMPANY_NAME'
            if str(event.eventType) != expected:
                raise Exception(f"{event.eventType} != {expected}")

            expected = "Spiderfeet Corporation"
            if str(event.data) != expected:
                raise Exception(f"{event.data} != {expected}")

            raise Exception("OK")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_company)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFootEvent(event_type, event_data, event_module, source_event)

        event_type = 'SSL_CERTIFICATE_ISSUED'
        event_data = 'O=Spiderfeet Corporation'
        event_module = 'example module'
        source_event = evt
        evt = SpiderFootEvent(event_type, event_data, event_module, source_event)

        with self.assertRaises(Exception) as cm:
            module.handleEvent(evt)

        self.assertEqual("OK", str(cm.exception))

    @unittest.skip("todo")
    def test_handleEvent_event_data_domain_whois_containing_company_name_should_return_event(self):
        sf = SpiderFoot(self.default_options)

        module = sfp_company()
        module.setup(sf, dict())

        target_value = 'spiderfeet.net'
        target_type = 'INTERNET_NAME'
        target = SpiderFootTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            expected = 'COMPANY_NAME'
            if str(event.eventType) != expected:
                raise Exception(f"{event.eventType} != {expected}")

            expected = "Spiderfeet Corporation"
            if str(event.data) != expected:
                raise Exception(f"{event.data} != {expected}")

            raise Exception("OK")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_company)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFootEvent(event_type, event_data, event_module, source_event)

        event_type = 'DOMAIN_WHOIS'
        event_data = 'Registrant Organization: Spiderfeet Corporation'
        event_module = 'example module'
        source_event = evt
        evt = SpiderFootEvent(event_type, event_data, event_module, source_event)

        with self.assertRaises(Exception) as cm:
            module.handleEvent(evt)

        self.assertEqual("OK", str(cm.exception))

    @unittest.skip("todo")
    def test_handleEvent_event_data_target_web_content_containing_company_name_should_return_event(self):
        sf = SpiderFoot(self.default_options)

        module = sfp_company()
        module.setup(sf, dict())

        target_value = 'spiderfeet.net'
        target_type = 'INTERNET_NAME'
        target = SpiderFootTarget(target_value, target_type)
        module.setTarget(target)

        def new_notifyListeners(self, event):
            expected = 'COMPANY_NAME'
            if str(event.eventType) != expected:
                raise Exception(f"{event.eventType} != {expected}")

            expected = "Spiderfeet Corporation"
            if str(event.data) != expected:
                raise Exception(f"{event.data} != {expected}")

            raise Exception("OK")

        module.notifyListeners = new_notifyListeners.__get__(module, sfp_company)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFootEvent(event_type, event_data, event_module, source_event)

        event_type = 'TARGET_WEB_CONTENT'
        event_data = '<p>Copyright Spiderfeet Corporation 2022.</p>'
        event_module = 'example module'
        source_event = evt
        evt = SpiderFootEvent(event_type, event_data, event_module, source_event)

        with self.assertRaises(Exception) as cm:
            module.handleEvent(evt)

        self.assertEqual("OK", str(cm.exception))
