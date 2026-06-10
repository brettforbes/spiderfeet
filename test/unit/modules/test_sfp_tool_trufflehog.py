import pytest
import unittest
from unittest.mock import patch

from modules.sfp_tool_trufflehog import sfp_tool_trufflehog
from sflib import SpiderFeet
from spiderfeet import SpiderFeetEvent, SpiderFeetTarget


@pytest.mark.usefixtures
class TestModuleToolTrufflehog(unittest.TestCase):

    def test_opts(self):
        module = sfp_tool_trufflehog()
        self.assertEqual(len(module.opts), len(module.optdescs))

    def test_setup(self):
        sf = SpiderFeet(self.default_options)
        module = sfp_tool_trufflehog()
        module.setup(sf, dict())

    def test_watchedEvents_should_return_list(self):
        module = sfp_tool_trufflehog()
        self.assertIsInstance(module.watchedEvents(), list)

    def test_producedEvents_should_return_list(self):
        module = sfp_tool_trufflehog()
        self.assertIsInstance(module.producedEvents(), list)

    @patch.object(sfp_tool_trufflehog, "_trufflehog_command", return_value=None)
    def test_handleEvent_no_tool_path_configured_should_set_errorState(self, _cmd):
        sf = SpiderFeet(self.default_options)

        module = sfp_tool_trufflehog()
        module.setup(sf, dict())

        target_value = 'example target value'
        target_type = 'IP_ADDRESS'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        root = SpiderFeetEvent('ROOT', target_value, '', '')
        event_type = 'SOCIAL_MEDIA'
        event_data = 'GitHub: https://github.com/octocat/Hello-World'
        event_module = 'sfp_test'
        evt = SpiderFeetEvent(event_type, event_data, event_module, root)

        result = module.handleEvent(evt)

        self.assertIsNone(result)
        self.assertTrue(module.errorState)
