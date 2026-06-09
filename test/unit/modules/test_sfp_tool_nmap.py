import pytest
import unittest
import os
from unittest.mock import patch

from modules.sfp_tool_nmap import sfp_tool_nmap
from sflib import SpiderFeet
from spiderfeet import SpiderFeetEvent, SpiderFeetTarget


@pytest.mark.usefixtures
class TestModuleToolNmap(unittest.TestCase):

    def test_opts(self):
        module = sfp_tool_nmap()
        self.assertEqual(len(module.opts), len(module.optdescs))

    def test_setup(self):
        sf = SpiderFeet(self.default_options)
        module = sfp_tool_nmap()
        module.setup(sf, dict())

    def test_watchedEvents_should_return_list(self):
        module = sfp_tool_nmap()
        self.assertIsInstance(module.watchedEvents(), list)

    def test_producedEvents_should_return_list(self):
        module = sfp_tool_nmap()
        self.assertIsInstance(module.producedEvents(), list)

    @patch.object(sfp_tool_nmap, "_resolve_nmap_executable", return_value=None)
    def test_handleEvent_no_tool_path_configured_should_set_errorState(self, _resolve):
        sf = SpiderFeet(self.default_options)

        module = sfp_tool_nmap()
        module.setup(sf, dict())

        target_value = 'example target value'
        target_type = 'IP_ADDRESS'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        root = SpiderFeetEvent('ROOT', target_value, '', '')
        event_type = 'IP_ADDRESS'
        event_data = '8.8.8.8'
        event_module = 'sfp_test'
        evt = SpiderFeetEvent(event_type, event_data, event_module, root)

        result = module.handleEvent(evt)

        self.assertIsNone(result)
        self.assertTrue(module.errorState)
