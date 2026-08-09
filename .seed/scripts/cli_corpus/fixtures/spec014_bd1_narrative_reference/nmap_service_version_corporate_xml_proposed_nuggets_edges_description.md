# Nmap OSINT Scan Report — service_version_corporate_xml

## Introduction

This report narrates the findings of a **Nmap** scan against **bbc.co.uk**. The story follows the scan itself, each discovered host, and any traceroute path recorded during the run. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan was executed with **nmap** version **7.80**, targeting **bbc.co.uk** from **Fri Jun 26 03:59:36 2026**. The operator invoked: `nmap -sT -sV -T3 -p 80,443 -oX - bbc.co.uk`.
 The run completed in **15.40** seconds.

Nmap done at Fri Jun 26 03:59:51 2026; 1 IP address (1 host up) scanned in 15.40 seconds

During this scan, **1** host was placed under investigation.

## Host 151.101.128.81

The host was observed as **up** (reason: **syn-ack**).
It answers to the internet name **bbc.co.uk**.

### Networks

Network address **151.101.128.81**:
- Port **443** on **tcp** is **open** (syn-ack), associated with **https**.
- Port **80** on **tcp** is **open** (syn-ack), associated with **http**.

### Applications

Application service **http** listening on port **80**. It runs **Varnish**.
- **Nmap Service Fingerprint** (`SF-Port80-TCP:V=7.80%I=7%D=6/26%Time=6A3D6C8F%P=i686-pc-windows-windows%r(GetRequest,201,"HTTP/1\.1\x20500\x20Domain\x20Not\x20Found\r\nConnection:\x20close\r\nContent-Length:\x20238\r\nServer:\x20Varnish\r\nRetry-After:\x200\r\ncontent-type:\x20text/html\r\nCache-Control:\x20private,\x20no-cache\r\nX-Served-By:\x20cache-syd10132-SYD\r\nAccept-Ranges:\x20bytes\r\nDate:\x20Thu,\x2025\x20Jun\x202026\x2017:59:43\x20GMT\r\nVia:\x201\.1\x20varnish\r\n\r\n\n<html>\n<head>\n<title>Fastly\x20error:\x20unknown\x20domain\x20</title>\n</head>\n<body>\n<p>Fastly\x20error:\x20unknown\x20domain:\x20\.\x20Please\x20check\x20that\x20this\x20domain\x20has\x20been\x20added\x20to\x20a\x20service\.</p>\n<p>Details:\x20cache-syd10132-SYD\x20\(151\.101\.128\.81\)</p></body></html>")%r(HTTPOptions,201,"HTTP/1\.1\x20500\x20Domain\x20Not\x20Found\r\nConnection:\x20close\r\nContent-Length:\x20238\r\nServer:\x20Varnish\r\nRetry-After:\x200\r\ncontent-type:\x20text/html\r\nCache-Control:\x20private,\x20no-cache\r\nX-Served-By:\x20cache-syd10136-SYD\r\nAccept-Ranges:\x20bytes\r\nDate:\x20Thu,\x2025\x20Jun\x202026\x2017:59:43\x20GMT\r\nVia:\x201\.1\x20varnish\r\n\r\n\n<html>\n<head>\n<title>Fastly\x20error:\x20unknown\x20domain\x20</title>\n</head>\n<body>\n<p>Fastly\x20error:\x20unknown\x20domain:\x20\.\x20Please\x20check\x20that\x20this\x20domain\x20has\x20been\x20added\x20to\x20a\x20service\.</p>\n<p>Details:\x20cache-syd10136-SYD\x20\(151\.101\.128\.81\)</p></body></html>")%r(RTSPRequest,94,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\nContent-Length:\x2011\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10134\r\n\r\nBad\x20Request")%r(X11Probe,94,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\nContent-Length:\x2011\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10128\r\n\r\nBad\x20Request")%r(FourOhFourRequest,201,"HTTP/1\.1\x20500\x20Domain\x20Not\x20Found\r\nConnection:\x20close\r\nContent-Length:\x20238\r\nServer:\x20Varnish\r\nRetry-After:\x200\r\ncontent-type:\x20text/html\r\nCache-Control:\x20private,\x20no-cache\r\nX-Served-By:\x20cache-syd10172-SYD\r\nAccept-Ranges:\x20bytes\r\nDate:\x20Thu,\x2025\x20Jun\x202026\x2017:59:43\x20GMT\r\nVia:\x201\.1\x20varnish\r\n\r\n\n<html>\n<head>\n<title>Fastly\x20error:\x20unknown\x20domain\x20</title>\n</head>\n<body>\n<p>Fastly\x20error:\x20unknown\x20domain:\x20\.\x20Please\x20check\x20that\x20this\x20domain\x20has\x20been\x20added\x20to\x20a\x20service\.</p>\n<p>Details:\x20cache-syd10172-SYD\x20\(151\.101\.128\.81\)</p></body></html>");`)
Application service **https** listening on port **443**. It runs **Varnish**.
- **Nmap Service Fingerprint** (`SF-Port443-TCP:V=7.80%T=SSL%I=7%D=6/26%Time=6A3D6C95%P=i686-pc-windows-windows%r(GetRequest,1B5,"HTTP/1\.1\x20421\x20Misdirected\x20Request\r\nConnection:\x20close\r\nContent-Length:\x20291\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10176\r\n\r\nRequested\x20host\x20does\x20not\x20match\x20any\x20Subject\x20Alternative\x20Names\x20\(SANs\)\x20on\x20TLS\x20certificate\x20\[4f59c34e59485b4439fd5998fadffe221ed9ecf678ca1416253643054a21ac31\]\x20in\x20use\x20with\x20this\x20connection\.\r\n\r\nVisit\x20https://www\.fastly\.com/documentation/guides/concepts/errors/#routing-errors\x20for\x20more\x20information\.\r\n\r")%r(HTTPOptions,1B5,"HTTP/1\.1\x20421\x20Misdirected\x20Request\r\nConnection:\x20close\r\nContent-Length:\x20291\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10175\r\n\r\nRequested\x20host\x20does\x20not\x20match\x20any\x20Subject\x20Alternative\x20Names\x20\(SANs\)\x20on\x20TLS\x20certificate\x20\[4f59c34e59485b4439fd5998fadffe221ed9ecf678ca1416253643054a21ac31\]\x20in\x20use\x20with\x20this\x20connection\.\r\n\r\nVisit\x20https://www\.fastly\.com/documentation/guides/concepts/errors/#routing-errors\x20for\x20more\x20information\.\r\n\r")%r(FourOhFourRequest,1B5,"HTTP/1\.1\x20421\x20Misdirected\x20Request\r\nConnection:\x20close\r\nContent-Length:\x20291\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10161\r\n\r\nRequested\x20host\x20does\x20not\x20match\x20any\x20Subject\x20Alternative\x20Names\x20\(SANs\)\x20on\x20TLS\x20certificate\x20\[4f59c34e59485b4439fd5998fadffe221ed9ecf678ca1416253643054a21ac31\]\x20in\x20use\x20with\x20this\x20connection\.\r\n\r\nVisit\x20https://www\.fastly\.com/documentation/guides/concepts/errors/#routing-errors\x20for\x20more\x20information\.\r\n\r")%r(tor-versions,94,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\nContent-Length:\x2011\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10148\r\n\r\nBad\x20Request")%r(RTSPRequest,94,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\nContent-Length:\x2011\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10132\r\n\r\nBad\x20Request");`)

## Conclusion

The scan captured **26** semantic nuggets across **1** host.
 Nmap done at Fri Jun 26 03:59:51 2026; 1 IP address (1 host up) scanned in 15.40 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| CATEGORY | APPLICATIONS | Applications Category | `applications:151.101.128.81` |
| CATEGORY | NETWORKS | Networks Category | `networks:151.101.128.81` |
| DESCRIPTOR | HOST_STATUS | Host Status | `up` |
| DESCRIPTOR | HOST_STATUS_REASON | Host Status Reason | `syn-ack` |
| DESCRIPTOR | INTERNET_NAME | Internet Name | `bbc.co.uk` |
| DESCRIPTOR | PORT_PROTOCOL | Port Protocol | `tcp` |
| DESCRIPTOR | PORT_STATE | Port State | `open` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `syn-ack` |
| DESCRIPTOR | SCAN_CLI | Scan CLI | `nmap -sT -sV -T3 -p 80,443 -oX - bbc.co.uk` |
| DESCRIPTOR | SCAN_ELAPSED | Scan Elapsed Time | `15.40` |
| DESCRIPTOR | SCAN_START | Scan Start | `Fri Jun 26 03:59:36 2026` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `Nmap done at Fri Jun 26 03:59:51 2026; 1 IP address (1 host up) scanned in 15.40 seconds` |
| DESCRIPTOR | SCAN_TARGET | Scan Target | `bbc.co.uk` |
| DESCRIPTOR | SCAN_TOOL | Scan Tool | `nmap` |
| DESCRIPTOR | SCAN_VERSION | Scan Version | `7.80` |
| DESCRIPTOR | SERVICE_FINGERPRINT | Nmap Service Fingerprint | `SF-Port443-TCP:V=7.80%T=SSL%I=7%D=6/26%Time=6A3D6C95%P=i686-pc-windows-windows%r(GetRequest,1B5,"HTTP/1\.1\x20421\x20Misdirected\x20Request\r\nConnection:\x20close\r\nContent-Length:\x20291\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10176\r\n\r\nRequested\x20host\x20does\x20not\x20match\x20any\x20Subject\x20Alternative\x20Names\x20\(SANs\)\x20on\x20TLS\x20certificate\x20\[4f59c34e59485b4439fd5998fadffe221ed9ecf678ca1416253643054a21ac31\]\x20in\x20use\x20with\x20this\x20connection\.\r\n\r\nVisit\x20https://www\.fastly\.com/documentation/guides/concepts/errors/#routing-errors\x20for\x20more\x20information\.\r\n\r")%r(HTTPOptions,1B5,"HTTP/1\.1\x20421\x20Misdirected\x20Request\r\nConnection:\x20close\r\nContent-Length:\x20291\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10175\r\n\r\nRequested\x20host\x20does\x20not\x20match\x20any\x20Subject\x20Alternative\x20Names\x20\(SANs\)\x20on\x20TLS\x20certificate\x20\[4f59c34e59485b4439fd5998fadffe221ed9ecf678ca1416253643054a21ac31\]\x20in\x20use\x20with\x20this\x20connection\.\r\n\r\nVisit\x20https://www\.fastly\.com/documentation/guides/concepts/errors/#routing-errors\x20for\x20more\x20information\.\r\n\r")%r(FourOhFourRequest,1B5,"HTTP/1\.1\x20421\x20Misdirected\x20Request\r\nConnection:\x20close\r\nContent-Length:\x20291\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10161\r\n\r\nRequested\x20host\x20does\x20not\x20match\x20any\x20Subject\x20Alternative\x20Names\x20\(SANs\)\x20on\x20TLS\x20certificate\x20\[4f59c34e59485b4439fd5998fadffe221ed9ecf678ca1416253643054a21ac31\]\x20in\x20use\x20with\x20this\x20connection\.\r\n\r\nVisit\x20https://www\.fastly\.com/documentation/guides/concepts/errors/#routing-errors\x20for\x20more\x20information\.\r\n\r")%r(tor-versions,94,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\nContent-Length:\x2011\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10148\r\n\r\nBad\x20Request")%r(RTSPRequest,94,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\nContent-Length:\x2011\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10132\r\n\r\nBad\x20Request");` |
| DESCRIPTOR | SERVICE_FINGERPRINT | Nmap Service Fingerprint | `SF-Port80-TCP:V=7.80%I=7%D=6/26%Time=6A3D6C8F%P=i686-pc-windows-windows%r(GetRequest,201,"HTTP/1\.1\x20500\x20Domain\x20Not\x20Found\r\nConnection:\x20close\r\nContent-Length:\x20238\r\nServer:\x20Varnish\r\nRetry-After:\x200\r\ncontent-type:\x20text/html\r\nCache-Control:\x20private,\x20no-cache\r\nX-Served-By:\x20cache-syd10132-SYD\r\nAccept-Ranges:\x20bytes\r\nDate:\x20Thu,\x2025\x20Jun\x202026\x2017:59:43\x20GMT\r\nVia:\x201\.1\x20varnish\r\n\r\n\n<html>\n<head>\n<title>Fastly\x20error:\x20unknown\x20domain\x20</title>\n</head>\n<body>\n<p>Fastly\x20error:\x20unknown\x20domain:\x20\.\x20Please\x20check\x20that\x20this\x20domain\x20has\x20been\x20added\x20to\x20a\x20service\.</p>\n<p>Details:\x20cache-syd10132-SYD\x20\(151\.101\.128\.81\)</p></body></html>")%r(HTTPOptions,201,"HTTP/1\.1\x20500\x20Domain\x20Not\x20Found\r\nConnection:\x20close\r\nContent-Length:\x20238\r\nServer:\x20Varnish\r\nRetry-After:\x200\r\ncontent-type:\x20text/html\r\nCache-Control:\x20private,\x20no-cache\r\nX-Served-By:\x20cache-syd10136-SYD\r\nAccept-Ranges:\x20bytes\r\nDate:\x20Thu,\x2025\x20Jun\x202026\x2017:59:43\x20GMT\r\nVia:\x201\.1\x20varnish\r\n\r\n\n<html>\n<head>\n<title>Fastly\x20error:\x20unknown\x20domain\x20</title>\n</head>\n<body>\n<p>Fastly\x20error:\x20unknown\x20domain:\x20\.\x20Please\x20check\x20that\x20this\x20domain\x20has\x20been\x20added\x20to\x20a\x20service\.</p>\n<p>Details:\x20cache-syd10136-SYD\x20\(151\.101\.128\.81\)</p></body></html>")%r(RTSPRequest,94,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\nContent-Length:\x2011\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10134\r\n\r\nBad\x20Request")%r(X11Probe,94,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\nContent-Length:\x2011\r\ncontent-type:\x20text/plain;\x20charset=utf-8\r\nx-served-by:\x20cache-syd10128\r\n\r\nBad\x20Request")%r(FourOhFourRequest,201,"HTTP/1\.1\x20500\x20Domain\x20Not\x20Found\r\nConnection:\x20close\r\nContent-Length:\x20238\r\nServer:\x20Varnish\r\nRetry-After:\x200\r\ncontent-type:\x20text/html\r\nCache-Control:\x20private,\x20no-cache\r\nX-Served-By:\x20cache-syd10172-SYD\r\nAccept-Ranges:\x20bytes\r\nDate:\x20Thu,\x2025\x20Jun\x202026\x2017:59:43\x20GMT\r\nVia:\x201\.1\x20varnish\r\n\r\n\n<html>\n<head>\n<title>Fastly\x20error:\x20unknown\x20domain\x20</title>\n</head>\n<body>\n<p>Fastly\x20error:\x20unknown\x20domain:\x20\.\x20Please\x20check\x20that\x20this\x20domain\x20has\x20been\x20added\x20to\x20a\x20service\.</p>\n<p>Details:\x20cache-syd10172-SYD\x20\(151\.101\.128\.81\)</p></body></html>");` |
| DESCRIPTOR | SERVICE_VERSION | Service Version | `Varnish` |
| ENTITY | HOST | Host | `151.101.128.81` |
| ENTITY | IPV4_ADDRESS | IP Address | `151.101.128.81` |
| ENTITY | SCAN_RECORD | Scan Record | `nmap:bbc.co.uk:Fri Jun 26 03:59:36 2026` |
| ENTITY | SERVICE | Network Service | `http` |
| ENTITY | SERVICE | Network Service | `https` |
| ENTITY | TRANSPORT | Transport Protocol | `tcp` |
| SUBENTITY | PORT | Network Port | `443` |
| SUBENTITY | PORT | Network Port | `80` |

---

*OS-Intel Scan · Fri Jun 26 03:59:36 2026 · Page 1*
