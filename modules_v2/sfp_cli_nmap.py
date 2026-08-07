# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        sfp_cli_nmap
# Purpose:     Check if a host/domain, IP address or netblock is malicious according
#              to Abuse.ch.
#
# Author:       steve@binarypool.com
#
# Created:     14/12/2013
# Copyright:   (c) Steve Micallef, 2013
# Licence:     Apache-2.0
# -------------------------------------------------------------------------------

from netaddr import IPAddress, IPNetwork

from spiderfeet import SpiderFeetEvent, SpiderFeetPlugin

###############################################################################################
# NMAP CLI Ap Class Interface
###############################################################################################

class sfp_cli_nmap(SpiderFeetPlugin):

    meta = {
        'name': "NMAP CLI App",
        'summary': "Run NMAP commands from the command line.",
        'types': ["cli"],
        'useCases': ["Passive", "Investigate"],
        'categories': ["Reputation Systems"],
        'dataSource': {
            'website': "https://nmap.org/",
            'license': "Nmap Public Source License Version 0.95",
            'repository': "https://github.com/nmap/nmap",
            'references': [
                "https://nmap.org/book/toc.html",
            ],
            'cliInstallInstructions': [
                "Install NMAP using your package manager.",
                "For example, on Ubuntu/Debian, run: sudo apt-get install nmap",
                "For example, on Fedora/RHEL, run: sudo dnf install nmap",
                "For example, on macOS, run: brew install nmap",
                "For example, on Windows, run: choco install nmap",
            ],
            'favIcon': "https://nmap.org/images/sitelogo-2x.png",
            'logo': "https://nmap.org/images/sitelogo-2x.png",
            'description': "Nmap ('Network Mapper') is a free and open source utility for network discovery and security auditing. Many systems and network administrators also find it useful for tasks such as network inventory, managing service upgrade schedules, and monitoring host or service uptime. Nmap uses raw IP packets in novel ways to determine what hosts are available on the network, what services (application name and version) those hosts are offering, what operating systems (and OS versions) they are running, what type of packet filters/firewalls are in use, and dozens of other characteristics. It was designed to rapidly scan large networks, but works fine against single hosts. Nmap runs on all major computer operating systems, and official binary packages are available for Linux, Windows, and Mac OS X. ",
        }
    }

    # Default options
    opts = {
        # TARGET SPECIFICATION
        'input_from_list': '-iL <inputfilename>',
        'random_targets': '-iR <num hosts>',
        'exclude_hosts': '--exclude <host1[,host2][,host3],...>',
        'exclude_from_file': '--excludefile <exclude_file>',
        # HOST DISCOVERY
        'list_scan': '-sL',
        'ping_scan': '-sn',
        'skip_host_discovery': '-Pn',
        'tcp_syn_discovery': '-PS[portlist]',
        'tcp_ack_discovery': '-PA[portlist]',
        'udp_discovery': '-PU[portlist]',
        'sctp_discovery': '-PY[portlist]',
        'icmp_echo_discovery': '-PE',
        'icmp_timestamp_discovery': '-PP',
        'icmp_netmask_discovery': '-PM',
        'ip_protocol_ping': '-PO[protocol list]',
        'never_resolve_dns': '-n',
        'always_resolve_dns': '-R',
        'custom_dns_servers': '--dns-servers <serv1[,serv2],...>',
        'use_system_dns': '--system-dns',
        'trace_hop_path': '--traceroute',
        # SCAN TECHNIQUES
        'tcp_syn_scan': '-sS',
        'tcp_connect_scan': '-sT',
        'tcp_ack_scan': '-sA',
        'tcp_window_scan': '-sW',
        'tcp_maimon_scan': '-sM',
        'udp_scan': '-sU',
        'tcp_null_scan': '-sN',
        'tcp_fin_scan': '-sF',
        'tcp_xmas_scan': '-sX',
        'custom_tcp_scan_flags': '--scanflags <flags>',
        'idle_scan': '-sI <zombie host[:probeport]>',
        'sctp_init_scan': '-sY',
        'sctp_cookie_echo_scan': '-sZ',
        'ip_protocol_scan': '-sO',
        'ftp_bounce_scan': '-b <FTP relay host>',
        # PORT SPECIFICATION AND SCAN ORDER
        'scan_ports': '-p <port ranges>',
        'exclude_ports': '--exclude-ports <port ranges>',
        'fast_scan_mode': '-F',
        'sequential_port_scan': '-r',
        'scan_top_ports': '--top-ports <number>',
        'scan_port_ratio': '--port-ratio <ratio>',
        # SERVICE/VERSION DETECTION
        'service_version_detection': '-sV',
        'version_probe_intensity': '--version-intensity <level>',
        'version_light_probes': '--version-light',
        'version_all_probes': '--version-all',
        'version_scan_trace': '--version-trace',
        # SCRIPT SCAN
        'default_script_scan': '-sC',
        'nse_scripts': '--script=<Lua scripts>',
        'nse_script_args': '--script-args=<n1=v1,[n2=v2,...]>',
        'nse_script_args_file': '--script-args-file=filename',
        'nse_script_trace': '--script-trace',
        'update_script_database': '--script-updatedb',
        'nse_script_help': '--script-help=<Lua scripts>',
        # OS DETECTION
        'os_detection': '-O',
        'os_detection_limit': '--osscan-limit',
        'os_detection_guess': '--osscan-guess',
        # TIMING AND PERFORMANCE
        'timing_template': '-T<0-5>',
        'min_hostgroup_size': '--min-hostgroup <size>',
        'max_hostgroup_size': '--max-hostgroup <size>',
        'min_probe_parallelism': '--min-parallelism <numprobes>',
        'max_probe_parallelism': '--max-parallelism <numprobes>',
        'min_rtt_timeout': '--min-rtt-timeout <time>',
        'max_rtt_timeout': '--max-rtt-timeout <time>',
        'initial_rtt_timeout': '--initial-rtt-timeout <time>',
        'max_probe_retries': '--max-retries <tries>',
        'host_scan_timeout': '--host-timeout <time>',
        'probe_scan_delay': '--scan-delay <time>',
        'max_probe_scan_delay': '--max-scan-delay <time>',
        'min_packet_rate': '--min-rate <number>',
        'max_packet_rate': '--max-rate <number>',
        # FIREWALL/IDS EVASION AND SPOOFING
        'fragment_packets': '-f',
        'fragment_mtu': '--mtu <val>',
        'decoy_scan': '-D <decoy1,decoy2[,ME],...>',
        'spoof_source_address': '-S <IP_Address>',
        'network_interface': '-e <iface>',
        'spoof_source_port': '-g/--source-port <portnum>',
        'relay_proxies': '--proxies <url1,[url2],...>',
        'append_hex_payload': '--data <hex string>',
        'append_ascii_payload': '--data-string <string>',
        'append_random_payload': '--data-length <num>',
        'custom_ip_options': '--ip-options <options>',
        'ip_ttl': '--ttl <val>',
        'spoof_mac_address': '--spoof-mac <mac address/prefix/vendor name>',
        'bogus_checksum': '--badsum',
        # OUTPUT
        'output_normal': '-oN <file>',
        'output_xml': '-oX <file>',
        'output_script_kiddie': '-oS <file>',
        'output_grepable': '-oG <file>',
        'output_all_formats': '-oA <basename>',
        'verbosity': '-v',
        'debug_level': '-d',
        'show_port_state_reason': '--reason',
        'show_open_ports_only': '--open',
        'show_packet_trace': '--packet-trace',
        'list_interfaces': '--iflist',
        'append_to_output_files': '--append-output',
        'resume_scan': '--resume <filename>',
        'xml_stylesheet': '--stylesheet <path/URL>',
        'portable_web_xml': '--webxml',
        'disable_xml_stylesheet': '--no-stylesheet',
        # MISC
        'ipv6_scanning': '-6',
        'aggressive_scan': '-A',
        'custom_data_directory': '--datadir <dirname>',
        'send_raw_ethernet': '--send-eth',
        'send_raw_ip': '--send-ip',
        'assume_privileged': '--privileged',
        'assume_unprivileged': '--unprivileged',
        'print_version': '-V',
        'print_help': '-h',
    }

    # Option descriptions
    optdescs = {
        # TARGET SPECIFICATION
        'input_from_list': "Input from list of hosts/networks",
        'random_targets': "Choose random targets",
        'exclude_hosts': "Exclude hosts/networks",
        'exclude_from_file': "Exclude list from file",
        # HOST DISCOVERY
        'list_scan': "List Scan - simply list targets to scan",
        'ping_scan': "Ping Scan - disable port scan",
        'skip_host_discovery': "Treat all hosts as online -- skip host discovery",
        'tcp_syn_discovery': "TCP SYN/ACK, UDP or SCTP discovery to given ports",
        'tcp_ack_discovery': "TCP SYN/ACK, UDP or SCTP discovery to given ports",
        'udp_discovery': "TCP SYN/ACK, UDP or SCTP discovery to given ports",
        'sctp_discovery': "TCP SYN/ACK, UDP or SCTP discovery to given ports",
        'icmp_echo_discovery': "ICMP echo, timestamp, and netmask request discovery probes",
        'icmp_timestamp_discovery': "ICMP echo, timestamp, and netmask request discovery probes",
        'icmp_netmask_discovery': "ICMP echo, timestamp, and netmask request discovery probes",
        'ip_protocol_ping': "IP Protocol Ping",
        'never_resolve_dns': "Never do DNS resolution/Always resolve [default: sometimes]",
        'always_resolve_dns': "Never do DNS resolution/Always resolve [default: sometimes]",
        'custom_dns_servers': "Specify custom DNS servers",
        'use_system_dns': "Use OS's DNS resolver",
        'trace_hop_path': "Trace hop path to each host",
        # SCAN TECHNIQUES
        'tcp_syn_scan': "TCP SYN/Connect()/ACK/Window/Maimon scans",
        'tcp_connect_scan': "TCP SYN/Connect()/ACK/Window/Maimon scans",
        'tcp_ack_scan': "TCP SYN/Connect()/ACK/Window/Maimon scans",
        'tcp_window_scan': "TCP SYN/Connect()/ACK/Window/Maimon scans",
        'tcp_maimon_scan': "TCP SYN/Connect()/ACK/Window/Maimon scans",
        'udp_scan': "UDP Scan",
        'tcp_null_scan': "TCP Null, FIN, and Xmas scans",
        'tcp_fin_scan': "TCP Null, FIN, and Xmas scans",
        'tcp_xmas_scan': "TCP Null, FIN, and Xmas scans",
        'custom_tcp_scan_flags': "Customize TCP scan flags",
        'idle_scan': "Idle scan",
        'sctp_init_scan': "SCTP INIT/COOKIE-ECHO scans",
        'sctp_cookie_echo_scan': "SCTP INIT/COOKIE-ECHO scans",
        'ip_protocol_scan': "IP protocol scan",
        'ftp_bounce_scan': "FTP bounce scan",
        # PORT SPECIFICATION AND SCAN ORDER
        'scan_ports': "Only scan specified ports",
        'exclude_ports': "Exclude the specified ports from scanning",
        'fast_scan_mode': "Fast mode - Scan fewer ports than the default scan",
        'sequential_port_scan': "Scan ports consecutively - don't randomize",
        'scan_top_ports': "Scan <number> most common ports",
        'scan_port_ratio': "Scan ports more common than <ratio>",
        # SERVICE/VERSION DETECTION
        'service_version_detection': "Probe open ports to determine service/version info",
        'version_probe_intensity': "Set from 0 (light) to 9 (try all probes)",
        'version_light_probes': "Limit to most likely probes (intensity 2)",
        'version_all_probes': "Try every single probe (intensity 9)",
        'version_scan_trace': "Show detailed version scan activity (for debugging)",
        # SCRIPT SCAN
        'default_script_scan': "equivalent to --script=default",
        'nse_scripts': "<Lua scripts> is a comma separated list of directories, script-files or script-categories",
        'nse_script_args': "provide arguments to scripts",
        'nse_script_args_file': "provide NSE script args in a file",
        'nse_script_trace': "Show all data sent and received",
        'update_script_database': "Update the script database.",
        'nse_script_help': "Show help about scripts. <Lua scripts> is a comma-separated list of script-files or script-categories.",
        # OS DETECTION
        'os_detection': "Enable OS detection",
        'os_detection_limit': "Limit OS detection to promising targets",
        'os_detection_guess': "Guess OS more aggressively",
        # TIMING AND PERFORMANCE
        'timing_template': "Set timing template (higher is faster)",
        'min_hostgroup_size': "Parallel host scan group sizes",
        'max_hostgroup_size': "Parallel host scan group sizes",
        'min_probe_parallelism': "Probe parallelization",
        'max_probe_parallelism': "Probe parallelization",
        'min_rtt_timeout': "Specifies probe round trip time.",
        'max_rtt_timeout': "Specifies probe round trip time.",
        'initial_rtt_timeout': "Specifies probe round trip time.",
        'max_probe_retries': "Caps number of port scan probe retransmissions.",
        'host_scan_timeout': "Give up on target after this long",
        'probe_scan_delay': "Adjust delay between probes",
        'max_probe_scan_delay': "Adjust delay between probes",
        'min_packet_rate': "Send packets no slower than <number> per second",
        'max_packet_rate': "Send packets no faster than <number> per second",
        # FIREWALL/IDS EVASION AND SPOOFING
        'fragment_packets': "fragment packets (optionally w/given MTU)",
        'fragment_mtu': "fragment packets (optionally w/given MTU)",
        'decoy_scan': "Cloak a scan with decoys",
        'spoof_source_address': "Spoof source address",
        'network_interface': "Use specified interface",
        'spoof_source_port': "Use given port number",
        'relay_proxies': "Relay connections through HTTP/SOCKS4 proxies",
        'append_hex_payload': "Append a custom payload to sent packets",
        'append_ascii_payload': "Append a custom ASCII string to sent packets",
        'append_random_payload': "Append random data to sent packets",
        'custom_ip_options': "Send packets with specified ip options",
        'ip_ttl': "Set IP time-to-live field",
        'spoof_mac_address': "Spoof your MAC address",
        'bogus_checksum': "Send packets with a bogus TCP/UDP/SCTP checksum",
        # OUTPUT
        'output_normal': "Output scan in normal, XML, s|<rIpt kIddi3, and Grepable format, respectively, to the given filename.",
        'output_xml': "Output scan in normal, XML, s|<rIpt kIddi3, and Grepable format, respectively, to the given filename.",
        'output_script_kiddie': "Output scan in normal, XML, s|<rIpt kIddi3, and Grepable format, respectively, to the given filename.",
        'output_grepable': "Output scan in normal, XML, s|<rIpt kIddi3, and Grepable format, respectively, to the given filename.",
        'output_all_formats': "Output in the three major formats at once",
        'verbosity': "Increase verbosity level (use -vv or more for greater effect)",
        'debug_level': "Increase debugging level (use -dd or more for greater effect)",
        'show_port_state_reason': "Display the reason a port is in a particular state",
        'show_open_ports_only': "Only show open (or possibly open) ports",
        'show_packet_trace': "Show all packets sent and received",
        'list_interfaces': "Print host interfaces and routes (for debugging)",
        'append_to_output_files': "Append to rather than clobber specified output files",
        'resume_scan': "Resume an aborted scan",
        'xml_stylesheet': "XSL stylesheet to transform XML output to HTML",
        'portable_web_xml': "Reference stylesheet from Nmap.Org for more portable XML",
        'disable_xml_stylesheet': "Prevent associating of XSL stylesheet w/XML output",
        # MISC
        'ipv6_scanning': "Enable IPv6 scanning",
        'aggressive_scan': "Enable OS detection, version detection, script scanning, and traceroute",
        'custom_data_directory': "Specify custom Nmap data file location",
        'send_raw_ethernet': "Send using raw ethernet frames or IP packets",
        'send_raw_ip': "Send using raw ethernet frames or IP packets",
        'assume_privileged': "Assume that the user is fully privileged",
        'assume_unprivileged': "Assume the user lacks raw socket privileges",
        'print_version': "Print version number",
        'print_help': "Print this help summary page.",
    }

    results = None
    errorState = False

    ###############################################################################################
    # NMAP Adapter Class Methods (skeleton code ideas)
    ###############################################################################################

    def setup(self, sfc, userOpts=dict()):
        pass

    # What types of nuggets can be consumed
    def consumedInputs(self):
        return [
            'IP_ADDRESS', 
            'NETBLOCK_OWNER', 
            'NETBLOCK_MEMBER', 
            'AFFILIATE_IPADDR', 
            'AFFILIATE_INTERNET_NAME', 
            'CO_HOSTED_SITE', 
            'NETBLOCK_OWNER', 
            'NETBLOCK_MEMBER', 
            'AFFILIATE_IPADDR', 
            'PORT'
            'AFFILIATE_INTERNET_NAME'
            ]

    # What list of nuggets can be in a semantic subgraph
    def producedSemanticNuggets(self):
        return [
            "ACCURACY",
            "APPLICATIONS",
            "CPE_URL",
            "DSA",
            "ECDSA",
            "EDDSA",
            "ENVIRONMENT",
            "HOP_ORDER",
            "HOP_RTT",
            "HOP_TTL",
            "HOST",
            "HOST_STATUS",
            "HOST_STATUS_REASON",
            "HTTP_TITLE",
            "INTERNET_NAME",
            "IP_ADDRESS",
            "NETWORKS",
            "OPERATING_SYSTEM",
            "OS_FAMILY",
            "OS_GEN",
            "OS_TYPE",
            "OS_VENDOR",
            "PORT",
            "PORT_PROTOCOL",
            "PORT_SOURCE",
            "PORT_STATE",
            "PORT_STATE_REASON",
            "RSA",
            "SCAN_CLI",
            "SCAN_ELAPSED",
            "SCAN_RECORD",
            "SCAN_START",
            "SCAN_SUMMARY",
            "SCAN_TARGET",
            "SCAN_TOOL",
            "SCAN_VERSION",
            "SERVICE",
            "SERVICE_EXTRAINFO",
            "SERVICE_FINGERPRINT",
            "SERVICE_VERSION",
            "SSH_KEY_BITS",
            "SSH_KEY_KEY",
            "SSH_KEY_TYPE",
            "TRACE",
            "TRACE_HOP",
            "TRACE_PROTOCOL",
            "TRANSPORT",
        ]

    def _resolve_nmap_executable(self):
        pass

    # Handle events sent to this module
    def handleEvent(self, event):
        pass

# End of sfp_cli_nmap class
