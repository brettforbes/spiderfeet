import pytest
import unittest

from modules.sfp_h1nobbdde import sfp_h1nobbdde
from sflib import SpiderFeet
from spiderfeet import SpiderFeetEvent, SpiderFeetTarget


@pytest.mark.usefixtures
class TestModuleIntegrationH1nobbdde(unittest.TestCase):

    @unittest.skip("todo")
    def test_handleEvent(self):
        sf = SpiderFeet(self.default_options)

        module = sfp_h1nobbdde()
        module.setup(sf, dict())

        target_value = 'example target value'
        target_type = 'IP_ADDRESS'
        target = SpiderFeetTarget(target_value, target_type)
        module.setTarget(target)

        event_type = 'ROOT'
        event_data = 'example data'
        event_module = ''
        source_event = ''
        evt = SpiderFeetEvent(event_type, event_data, event_module, source_event)

        result = module.handleEvent(evt)

        self.assertIsNone(result)
