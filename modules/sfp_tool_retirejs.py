# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_tool_retirejs
# Purpose:      SpiderFeet plug-in for using the 'Retire.js' tool.
#
# Author:      Steve Micallef <steve@binarypool.com>
#
# Created:     2022-04-02
# Copyright:   (c) Steve Micallef 2022
# Licence:     Apache-2.0
# -------------------------------------------------------------------------------


# # Stage 5 operator documentation
# Scanner detecting the use of JavaScript libraries with known vulnerabilities
import os
import sys
import json
import shutil
import tempfile
from shutil import which
from subprocess import Popen, PIPE, TimeoutExpired

from spiderfeet import SpiderFeetPlugin, SpiderFeetEvent


class sfp_tool_retirejs(SpiderFeetPlugin):

    meta = {
        "name": "Tool - Retire.js",
        "summary": "Scanner detecting the use of JavaScript libraries with known vulnerabilities",
        "flags": ["tool"],
        "useCases": ["Footprint", "Investigate"],
        "categories": ["Content Analysis"],
        "toolDetails": {
            "name": "Retire.js",
            "description": "Scanner detecting the use of JavaScript libraries with known vulnerabilities",
            "website": "http://retirejs.github.io/retire.js/",
            "repository": "https://github.com/RetireJS/retire.js"
        }
    }

    # Default options
    opts = {
        "retirejs_path": "",
    }

    # Option descriptions
    optdescs = {
        "retirejs_path": "Path to your retire binary. Optional if retire is on PATH."
    }

    # Target
    results = None
    errorState = False

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in userOpts.keys():
            self.opts[opt] = userOpts[opt]

    def watchedEvents(self):
        return ["LINKED_URL_INTERNAL", "LINKED_URL_EXTERNAL"]

    def producedEvents(self):
        return [
            "VULNERABILITY_CVE_CRITICAL",
            "VULNERABILITY_CVE_HIGH",
            "VULNERABILITY_CVE_MEDIUM",
            "VULNERABILITY_CVE_LOW",
            "VULNERABILITY_GENERAL"
        ]

    def _resolve_retire_executable(self):
        found = which("retire") or which("retire.cmd") or which("retire.exe")
        if not found:
            for folder in os.environ.get("PATH", "").split(os.pathsep):
                for name in ("retire", "retire.cmd", "retire.exe"):
                    candidate = os.path.join(folder, name)
                    if os.path.isfile(candidate):
                        found = candidate
                        break
                if found:
                    break
        if found and os.path.isfile(found):
            return found

        if not self.opts['retirejs_path']:
            self.error("You enabled sfp_tool_retirejs but did not set a path to the tool!")
            return None

        exe = self.opts['retirejs_path']
        if self.opts['retirejs_path'].endswith('/'):
            exe = f"{exe}retire"

        if not os.path.isfile(exe):
            self.error(f"File does not exist: {exe}")
            return None

        return exe

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        self.debug(f"Received event, {eventName}, from {srcModuleName}")

        if self.errorState:
            return

        if ".js" not in eventData:
            return

        # Don't look up stuff twice
        if eventData in self.results:
            self.debug(f"Skipping {eventData} as already scanned.")
            return
        self.results[eventData] = True

        exe = self._resolve_retire_executable()
        if not exe:
            self.errorState = True
            return

        # Store the javascript file being analyzed somewhere temporary
        tmpdirname = tempfile.mkdtemp()
        res = self.sf.fetchUrl(
            eventData,
            timeout=self.opts["_fetchtimeout"],
            useragent=self.opts["_useragent"],
            disableContentEncoding=True
        )

        if res["content"] is None:
            self.error(f"Unable to fetch {eventData}")
            return

        p = None
        try:
            with open(f"{tmpdirname}/lib.js", "wb") as f:
                f.write(res["content"])

            p = Popen(
                [exe, "--outputformat", "json", "--path", "."],
                cwd=tmpdirname,
                stdout=PIPE,
                stderr=PIPE,
            )
            stdout, stderr = p.communicate(input=None, timeout=60)
            if p.returncode == 0 or p.returncode == 13:
                content = stdout.decode(sys.stdin.encoding)
            else:
                self.error("Unable to read Retire.js content.")
                self.debug(f"Error running Retire.js: {stderr} - {stdout}")
                shutil.rmtree(tmpdirname)
                return
        except TimeoutExpired:
            if p:
                p.kill()
                stdout, stderr = p.communicate()
                self.debug("Timed out waiting for Retire.js to finish")
            shutil.rmtree(tmpdirname)
            return

        try:
            data = json.loads(content)
            for item in data.get("data", []):
                for result in item["results"]:
                    for vuln in result["vulnerabilities"]:
                        if "CVE" not in vuln["identifiers"]:
                            text = f"{vuln['identifiers']['summary']}\n"
                            text += f"Severity: {vuln['severity']}\n"
                            text += f"Info: <SFURL>{vuln['info'][0]}</SFURL>"
                            evt = SpiderFeetEvent(
                                "VULNERABILITY_GENERAL", text, self.__name__, event
                            )
                            self.notifyListeners(evt)
                        else:
                            for cve in vuln["identifiers"]["CVE"]:
                                etype, cvetext = self.sf.cveInfo(cve)
                                evt = SpiderFeetEvent(
                                    etype, cvetext, self.__name__, event
                                )
                                self.notifyListeners(evt)
            shutil.rmtree(tmpdirname)
        except BaseException as e:
            self.error(f"Couldn't parse the JSON output of Retire.js: {e}")
            shutil.rmtree(tmpdirname)
            return

# End of sfp_tool_retirejs class
