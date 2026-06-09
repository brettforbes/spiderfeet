# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_tool_nmap
# Purpose:      SpiderFeet plug-in for using nmap to perform OS fingerprinting.
#
# Author:      Steve Micallef <steve@binarypool.com>
#
# Created:     03/05/2020
# Copyright:   (c) Steve Micallef 2020
# Licence:     Apache-2.0
# -------------------------------------------------------------------------------


# # Stage 5 operator documentation
# Identify what Operating System might be used.
import os.path
import sys
from shutil import which
from subprocess import PIPE, Popen

from netaddr import IPNetwork

from spiderfeet import SpiderFeetEvent, SpiderFeetPlugin


class sfp_tool_nmap(SpiderFeetPlugin):

    meta = {
        'name': "Tool - Nmap",
        'summary': "Identify what Operating System might be used.",
        'flags': ["tool", "slow", "invasive"],
        'useCases': ["Footprint", "Investigate"],
        'categories': ["Crawling and Scanning"],
        'toolDetails': {
            'name': "Nmap",
            'description': "Nmap (\"Network Mapper\") is a free and open source utility for network discovery and security auditing.\n"
            "Nmap uses raw IP packets in novel ways to determine what hosts are available on the network, "
            "what services (application name and version) those hosts are offering, "
            "what operating systems (and OS versions) they are running, "
            "what type of packet filters/firewalls are in use, and dozens of other characteristics.\n",
            'website': "https://nmap.org/",
            'repository': "https://svn.nmap.org/nmap"
        },
    }

    # Default options
    opts = {
        'nmappath': "",
        'netblockscan': True,
        'netblockscanmax': 24
    }

    # Option descriptions
    optdescs = {
        'nmappath': "Path to the nmap binary. Optional if nmap is on PATH.",
        'netblockscan': "Port scan all IPs within identified owned netblocks?",
        'netblockscanmax': "Maximum netblock/subnet size to scan IPs within (CIDR value, 24 = /24, 16 = /16, etc.)"
    }

    results = None
    errorState = False

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()
        self.errorState = False
        self.__dataSource__ = "Target Network"

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    def watchedEvents(self):
        return ['IP_ADDRESS', 'NETBLOCK_OWNER']

    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    def producedEvents(self):
        return ["OPERATING_SYSTEM", "IP_ADDRESS"]

    def _resolve_nmap_executable(self):
        if self.opts.get('nmappath'):
            path = self.opts['nmappath']
            if path.endswith('/') or path.endswith('\\'):
                names = ('nmap.exe', 'nmap') if sys.platform == 'win32' else ('nmap',)
                for name in names:
                    candidate = os.path.join(path, name)
                    if os.path.isfile(candidate):
                        return candidate
            elif path.endswith('nmap') or path.endswith('nmap.exe'):
                if os.path.isfile(path):
                    return path
            self.error("Could not recognize your nmap path configuration.")
            return None

        found = which('nmap') or which('nmap.exe')
        if found and os.path.isfile(found):
            return found

        if sys.platform == 'win32':
            for candidate in (
                r"C:\Program Files (x86)\Nmap\nmap.exe",
                r"C:\Program Files\Nmap\nmap.exe",
            ):
                if os.path.isfile(candidate):
                    return candidate

        self.error("You enabled sfp_tool_nmap but did not set a path to the tool!")
        return None

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if srcModuleName == "sfp_tool_nmap":
            self.debug("Skipping event from myself.")
            return

        self.debug(f"Received event, {eventName}, from {srcModuleName}")

        if self.errorState:
            return

        try:
            if eventName == "NETBLOCK_OWNER" and self.opts['netblockscan']:
                net = IPNetwork(eventData)
                if net.prefixlen < self.opts['netblockscanmax']:
                    self.debug("Skipping port scanning of " + eventData + ", too big.")
                    return

        except Exception as e:
            self.error("Strange netblock identified, unable to parse: " + eventData + " (" + str(e) + ")")
            return

        # Don't look up stuff twice, check IP == IP here
        if eventData in self.results:
            self.debug("Skipping " + eventData + " as already scanned.")
            return

        # Might be a subnet within a subnet or IP within a subnet
        for addr in self.results:
            if IPNetwork(eventData) in IPNetwork(addr):
                self.debug(f"Skipping {eventData} as already within a scanned range.")
                return

        self.results[eventData] = True

        exe = self._resolve_nmap_executable()
        if not exe:
            self.errorState = True
            return

        # Sanitize domain name.
        if not self.sf.validIP(eventData) and not self.sf.validIpNetwork(eventData):
            self.error("Invalid input, refusing to run.")
            return

        try:
            p = Popen([exe, "-O", "--osscan-limit", eventData], stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate(input=None)
            if p.returncode == 0:
                content = stdout.decode('utf-8', errors='replace')
            else:
                self.error("Unable to read Nmap content.")
                self.debug(f"Error running Nmap: {stderr}, {stdout}")
                return

            if "No exact OS matches for host" in content or "OSScan results may be unreliable" in content:
                self.debug(f"Couldn't reliably detect the OS for {eventData}")
                return
        except Exception as e:
            self.error(f"Unable to run Nmap: {e}")
            return

        if not content:
            self.debug("No content from Nmap to parse.")
            return

        if eventName == "IP_ADDRESS":
            try:
                opsys = None
                for line in content.split('\n'):
                    if "OS details:" in line:
                        junk, opsys = line.split(": ")
                if opsys:
                    evt = SpiderFeetEvent("OPERATING_SYSTEM", opsys, self.__name__, event)
                    self.notifyListeners(evt)
            except Exception as e:
                self.error("Couldn't parse the output of Nmap: " + str(e))
                return

        if eventName == "NETBLOCK_OWNER":
            try:
                currentIp = None
                for line in content.split('\n'):
                    opsys = None
                    if "scan report for" in line:
                        currentIp = line.split("(")[1].replace(")", "")
                    if "OS details:" in line:
                        junk, opsys = line.split(": ")

                    if opsys and currentIp:
                        ipevent = SpiderFeetEvent("IP_ADDRESS", currentIp, self.__name__, event)
                        self.notifyListeners(ipevent)

                        evt = SpiderFeetEvent("OPERATING_SYSTEM", opsys, self.__name__, ipevent)
                        self.notifyListeners(evt)
                        currentIp = None
            except Exception as e:
                self.error(f"Couldn't parse the output of Nmap: {e}")
                return

# End of sfp_tool_nmap class
