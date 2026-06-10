import pytest
import unittest
from unittest.mock import patch

from modules.sfp_tool_nuclei import sfp_tool_nuclei
from sflib import SpiderFeet
from spiderfeet import SpiderFeetEvent, SpiderFeetTarget


@pytest.mark.usefixtures
class TestModuleToolNuclei(unittest.TestCase):

    def test_opts(self):
        module = sfp_tool_nuclei()
        self.assertEqual(len(module.opts), len(module.optdescs))

    def test_setup(self):
        sf = SpiderFeet(self.default_options)
        module = sfp_tool_nuclei()
        module.setup(sf, dict())

    def test_watchedEvents_should_return_list(self):
        module = sfp_tool_nuclei()
        self.assertIsInstance(module.watchedEvents(), list)

    def test_producedEvents_should_return_list(self):
        module = sfp_tool_nuclei()
        self.assertIsInstance(module.producedEvents(), list)

    @patch.object(sfp_tool_nuclei, "_resolve_nuclei_paths", return_value=(None, None))
    def test_handleEvent_no_tool_path_configured_should_set_errorState(self, _resolve):
        sf = SpiderFeet(self.default_options)

        module = sfp_tool_nuclei()
        module.setup(sf, dict())

        target_value = 'example target value'
        target_type = 'IP_ADDRESS'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        root = SpiderFeetEvent('ROOT', target_value, '', '')
        event_type = 'INTERNET_NAME'
        event_data = 'example.com'
        event_module = 'sfp_test'
        evt = SpiderFeetEvent(event_type, event_data, event_module, root)

        result = module.handleEvent(evt)

        self.assertIsNone(result)
        self.assertTrue(module.errorState)
