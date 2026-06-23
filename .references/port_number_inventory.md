# Port Number Inventory

**Source:** [https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers)

Comprehensive TCP/UDP port listing from Wikipedia, extended with an **Observations** column for scan-derived port/service combinations. This file is the working single source of truth until the inventory is promoted into TypeDB.

Descriptions include Wikipedia article links (`https://en.wikipedia.org/wiki/...`) where the source article provides them.

**Generated from:** `ee22c200-ffd9-4e4d-83aa-73fd28fd4fc7.txt` + `List_of_TCP_and_UDP_port_numbers-0.md` (links)

## Observations column

Record port/protocol/service combinations discovered during scanning that are not already captured in the IANA/Wikipedia description — for example an unexpected service banner on a well-known port, or a non-standard use of a registered port. Keep entries concise; one observation per cell unless multiple distinct findings warrant a semicolon-separated list.

## Table legend

| Cell | Meaning |
|------|---------|
| Yes | IANA-assigned and standardized, specified, or widely used on the port |
| Unofficial | Not IANA-assigned but standardized, specified, or widely used |
| Assigned | IANA-assigned but not standardized, specified, or widely used |
| No | Not IANA-assigned or widely used |
| Reserved | Reserved by IANA; may be available on request |

---

## Well-known ports (0–1023)

| Port | TCP | UDP | Observations | Description |
|------|-----|-----|--------------|-------------|
| 0 | Reserved |  |  | In programming APIs (not in communication between hosts), requests a system-allocated (dynamic) port |
| 1 | Yes | Assigned |  | [TCP Port Service Multiplexer](https://en.wikipedia.org/wiki/TCP_Port_Service_Multiplexer "TCP Port Service Multiplexer") (TCPMUX). Historic. Both TCP and UDP have been assigned to TCPMUX by IANA, but by design only TCP is specified |
| 2 | Reserved |  |  | De-assigned on 2025-02-13, previously compressnet |
| 3 | Reserved |  |  | De-assigned on 2025-02-13, previously compressnet |
| 5 | Assigned |  |  | [Remote Job Entry](https://en.wikipedia.org/wiki/Remote_Job_Entry "Remote Job Entry") was historically using socket 5 in its [old socket form](https://en.wikipedia.org/wiki/Network_socket#History "Network socket"), while [MIB](https://en.wikipedia.org/wiki/Management_information_base "Management information base") [PIM](https://en.wikipedia.org/wiki/Protocol_Independent_Multicast "Protocol Independent Multicast") has identified it as TCP/5 and IANA has assigned both TCP and UDP 5 to it |
| 7 | Yes |  |  | [Echo Protocol](https://en.wikipedia.org/wiki/Echo_Protocol "Echo Protocol") |
| 9 | Yes | Yes |  | [Discard Protocol](https://en.wikipedia.org/wiki/Discard_Protocol "Discard Protocol") |
| 9 | No | Unofficial |  | [Wake-on-LAN](https://en.wikipedia.org/wiki/Wake-on-LAN "Wake-on-LAN") |
| 11 | Yes |  |  | Active Users ([systat](https://en.wikipedia.org/wiki/Systat_(protocol) "Systat (protocol)") service) |
| 13 | Yes |  |  | [Daytime Protocol](https://en.wikipedia.org/wiki/Daytime_Protocol "Daytime Protocol") |
| 15 | Unofficial | No |  | Previously [netstat](https://en.wikipedia.org/wiki/Netstat "Netstat") service |
| 17 | Yes |  |  | [Quote of the Day](https://en.wikipedia.org/wiki/QOTD "QOTD") (QOTD) |
| 18 | Yes |  |  | [Message Send Protocol](https://en.wikipedia.org/wiki/Message_Send_Protocol "Message Send Protocol") |
| 19 | Yes |  |  | [Character Generator Protocol](https://en.wikipedia.org/wiki/Character_Generator_Protocol "Character Generator Protocol") (CHARGEN) |
| 20 | Yes | Assigned |  | [File Transfer Protocol](https://en.wikipedia.org/wiki/File_Transfer_Protocol "File Transfer Protocol") (FTP) data transfer |
| 21 | Yes | Assigned |  | File Transfer Protocol (FTP) control (command) |
| 22 | Yes | Assigned |  | [Secure Shell](https://en.wikipedia.org/wiki/Secure_Shell "Secure Shell") (SSH), secure logins, [file transfers](https://en.wikipedia.org/wiki/File_transfer "File transfer") ([scp](https://en.wikipedia.org/wiki/Secure_copy "Secure copy"), [sftp](https://en.wikipedia.org/wiki/SSH_file_transfer_protocol "SSH file transfer protocol")) and port forwarding |
| 23 | Yes | Assigned |  | [Telnet](https://en.wikipedia.org/wiki/Telnet "Telnet") protocol—unencrypted text communications |
| 24 | Yes | Assigned |  | "any private mail system", often used for [LMTP](https://en.wikipedia.org/wiki/Local_Mail_Transfer_Protocol "Local Mail Transfer Protocol") |
| 25 | Yes | Assigned |  | [Simple Mail Transfer Protocol](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol "Simple Mail Transfer Protocol") (SMTP), used for email routing between mail servers |
| 27 | Assigned |  |  | nsw-fe (NSW User System FE) |
| 28 | Unofficial |  |  | Palo Alto Networks' Panorama High Availability (HA) sync encrypted port |
| 29 | Assigned |  |  | msg-icp (MSG ICP) |
| 31 | Assigned |  |  | msg-auth (MSG Authentication) |
| 33 | Assigned |  |  | dsp (Display Support Protocol) |
| 37 | Yes |  |  | [Time Protocol](https://en.wikipedia.org/wiki/Time_Protocol "Time Protocol") |
| 38 | Assigned |  |  | rap (Route Access Protocol) |
| 39 | Assigned |  |  | rlp (Resource Location Protocol) |
| 41 | Assigned |  |  | graphics (Graphics) |
| 42 | Assigned | Yes |  | [Host Name Server Protocol](https://en.wikipedia.org/wiki/ARPA_Host_Name_Server_Protocol "ARPA Host Name Server Protocol") |
| 43 | Yes | Assigned |  | [WHOIS](https://en.wikipedia.org/wiki/WHOIS "WHOIS") protocol |
| 44 | Assigned |  |  | mpm-flags (MPM FLAGS Protocol) |
| 45 | Assigned |  |  | mpm (Message Processing Module \[recv\]) |
| 46 | Assigned |  |  | mpm-snd (MPM \[default send\]) |
| 47 | Reserved |  |  | Removed by IANA on 2017-05-18, previously used for NI FTP |
| 48 | Assigned |  |  | auditd (Digital Audit Daemon) |
| 49 | Yes |  |  | [TACACS](https://en.wikipedia.org/wiki/TACACS "TACACS") Login Host protocol. [TACACS+](https://en.wikipedia.org/wiki/TACACS+ "TACACS+"), still in draft which is an improved but distinct version of TACACS, only uses TCP 49 |
| 50 | Assigned |  |  | re-mail-ck (Remote Mail Checking Protocol) |
| 51 | Reserved |  |  | Historically used for [Interface Message Processor](https://en.wikipedia.org/wiki/Interface_Message_Processor "Interface Message Processor") logical address management, entry has been removed by IANA on 2013-05-25 |
| 52 | Assigned |  |  | [Xerox Network Systems](https://en.wikipedia.org/wiki/Xerox_Network_Systems "Xerox Network Systems") (XNS) Time Protocol. Despite this port being assigned by IANA, the service is meant to work on [SPP](https://en.wikipedia.org/wiki/Sequenced_Packet_Protocol "Sequenced Packet Protocol") (ancestor of [IPX/SPX](https://en.wikipedia.org/wiki/IPX/SPX "IPX/SPX")), instead of TCP/IP |
| 53 | Yes |  |  | [Domain Name System](https://en.wikipedia.org/wiki/Domain_Name_System "Domain Name System") (DNS) |
| 54 | Assigned |  |  | Xerox Network Systems (XNS) Clearinghouse (Name Server). Despite this port being assigned by IANA, the service is meant to work on [SPP](https://en.wikipedia.org/wiki/Sequenced_Packet_Protocol "Sequenced Packet Protocol") (ancestor of [IPX/SPX](https://en.wikipedia.org/wiki/IPX/SPX "IPX/SPX")), instead of TCP/IP |
| 55 | Assigned |  |  | isi-gl (ISI Graphics Language) |
| 56 | Assigned |  |  | Xerox Network Systems (XNS) Authentication Protocol. Despite this port being assigned by IANA, the service is meant to work on [SPP](https://en.wikipedia.org/wiki/Sequenced_Packet_Protocol "Sequenced Packet Protocol") (ancestor of [IPX/SPX](https://en.wikipedia.org/wiki/IPX/SPX "IPX/SPX")), instead of TCP/IP |
| 58 | Assigned |  |  | Xerox Network Systems (XNS) Mail. Despite this port being assigned by IANA, the service is meant to work on [SPP](https://en.wikipedia.org/wiki/Sequenced_Packet_Protocol "Sequenced Packet Protocol") (ancestor of [IPX/SPX](https://en.wikipedia.org/wiki/IPX/SPX "IPX/SPX")), instead of TCP/IP |
| 61 | Reserved |  |  | Historically assigned to the [NIFTP-Based Mail](/w/index.php?title=NIFTP-Based%5FMail&action=edit&redlink=1 "NIFTP-Based Mail (page does not exist)") protocol, but was never documented in the related [IEN](https://en.wikipedia.org/wiki/Internet_Experiment_Note "Internet Experiment Note"). The port number entry was removed from IANA's registry on 2017-05-18 |
| 62 | Assigned |  |  | acas (ACA Services) |
| 63 | Assigned |  |  | whoispp (whois++) |
| 64 | Assigned |  |  | covia (Communications Integrator (CI)) |
| 65 | Assigned |  |  | tacacs-ds (TACACS-Database Service) |
| 66 | Assigned |  |  | sql-net (Oracle SQL*NET) |
| 67 | Assigned | Yes |  | [Bootstrap Protocol](https://en.wikipedia.org/wiki/Bootstrap_Protocol "Bootstrap Protocol") (BOOTP) server; also used by [Dynamic Host Configuration Protocol](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol "Dynamic Host Configuration Protocol") (DHCP) |
| 68 | Assigned | Yes |  | Bootstrap Protocol (BOOTP) client; also used by Dynamic Host Configuration Protocol (DHCP) |
| 69 | Assigned | Yes |  | [Trivial File Transfer Protocol](https://en.wikipedia.org/wiki/Trivial_File_Transfer_Protocol "Trivial File Transfer Protocol") (TFTP) |
| 70 | Yes | Assigned |  | [Gopher](https://en.wikipedia.org/wiki/Gopher_(protocol) "Gopher (protocol)") protocol |
| 71–74 | Yes |  |  | [NETRJS](https://en.wikipedia.org/wiki/NETRJS "NETRJS") protocol |
| 76 | Assigned |  |  | deos (Distributed External Object Store) |
| 78 | Assigned |  |  | vettcp (vettcp) |
| 79 | Yes | Assigned |  | [Finger protocol](https://en.wikipedia.org/wiki/Finger_protocol "Finger protocol") |
| 80 | Yes | Yes |  | [Hypertext Transfer Protocol](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol "Hypertext Transfer Protocol") (HTTP) uses TCP in versions 1.x and 2\. [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3 "HTTP/3") uses [QUIC](https://en.wikipedia.org/wiki/QUIC "QUIC"), a transport protocol on top of UDP |
| 81 | Unofficial |  |  | [TorPark](https://en.wikipedia.org/wiki/TorPark "TorPark") [onion routing](https://en.wikipedia.org/wiki/Onion_routing "Onion routing") |
| 82 | Assigned |  |  | xfer (XFER Utility) |
| 82 | Unofficial |  |  | TorPark control |
| 83 | Assigned |  |  | mit-ml-dev (MIT ML Device) |
| 84 | Assigned |  |  | ctf (Common Trace Facility) |
| 85 | Assigned |  |  | mit-ml-dev (MIT ML Device) |
| 86 | Assigned |  |  | mfcobol (Micro Focus Cobol) |
| 88 | Yes |  |  | [Kerberos](https://en.wikipedia.org/wiki/Kerberos_(protocol) "Kerberos (protocol)") authentication system |
| 89 | Assigned |  |  | su-mit-tg (SU/MIT Telnet Gateway) |
| 90 | Assigned |  |  | [PointCast (dotcom)](https://en.wikipedia.org/wiki/PointCast_(dotcom) "PointCast (dotcom)") |
| 90 | Unofficial |  |  | [PointCast (dotcom)](https://en.wikipedia.org/wiki/PointCast_(dotcom) "PointCast (dotcom)") |
| 91 | Assigned |  |  | mit-dov (MIT Dover Spooler) |
| 92 | Assigned |  |  | npp (Network Printing Protocol) |
| 93 | Assigned |  |  | dcp (Device Control Protocol) |
| 94 | Assigned |  |  | objcall (Tivoli Object Dispatcher) |
| 95 | Yes | Assigned |  | SUPDUP, terminal-independent remote login |
| 96 | Assigned |  |  | dixie (DIXIE Protocol Specification) |
| 97 | Assigned |  |  | swift-rvf (Swift Remote Virtual File Protocol) |
| 98 | Assigned |  |  | tacnews (TAC News) |
| 99 | Assigned |  |  | metagram (Metagram Relay) |
| 101 | Yes | Assigned |  | [NIC](https://en.wikipedia.org/wiki/History_of_the_Internet#NIC,_InterNIC,_IANA,_and_ICANN "History of the Internet") [host name](https://en.wikipedia.org/wiki/Hostname "Hostname") |
| 102 | Yes | Assigned |  | [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization "International Organization for Standardization") Transport Service Access Point ([TSAP](https://en.wikipedia.org/wiki/TSAP "TSAP")) Class 0 protocol; |
| 104 | Yes |  |  | [Digital Imaging and Communications in Medicine](https://en.wikipedia.org/wiki/Digital_Imaging_and_Communications_in_Medicine "Digital Imaging and Communications in Medicine") (DICOM; also port 11112) |
| 105 | Yes |  |  | [CCSO Nameserver](https://en.wikipedia.org/wiki/CCSO_Nameserver "CCSO Nameserver") |
| 106 | Unofficial | No |  | [macOS Server](https://en.wikipedia.org/wiki/MacOS_Server "MacOS Server"), (macOS) password server |
| 107 | Yes |  |  | [Remote User Telnet Service](https://en.wikipedia.org/wiki/Rtelnet "Rtelnet") (RTelnet) |
| 108 | Yes |  |  | IBM [Systems Network Architecture](https://en.wikipedia.org/wiki/Systems_Network_Architecture "Systems Network Architecture") (SNA) gateway access server |
| 109 | Yes | Assigned |  | [Post Office Protocol](https://en.wikipedia.org/wiki/Post_Office_Protocol "Post Office Protocol"), version 2 (POP2) |
| 110 | Yes | Assigned |  | Post Office Protocol, version 3 (POP3) |
| 111 | Yes |  |  | [Open Network Computing Remote Procedure Call](https://en.wikipedia.org/wiki/Open_Network_Computing_Remote_Procedure_Call "Open Network Computing Remote Procedure Call") (ONC RPC, sometimes referred to as Sun RPC) |
| 112 | Yes |  |  | [McIDAS](https://en.wikipedia.org/wiki/McIDAS "McIDAS") Data Transmission Protocol |
| 113 | Yes | No |  | [Ident](https://en.wikipedia.org/wiki/Ident_protocol "Ident protocol"), authentication service/identification protocol, used by [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat "Internet Relay Chat") servers to identify users |
| 113 | Yes | Assigned |  | [Ident](https://en.wikipedia.org/wiki/Ident_protocol "Ident protocol"), authentication service/identification protocol, used by [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat "Internet Relay Chat") servers to identify users |
| 115 | Yes | Assigned |  | [Simple File Transfer Protocol](https://en.wikipedia.org/wiki/Simple_File_Transfer_Protocol "Simple File Transfer Protocol") |
| 117 | Yes |  |  | [UUCP Mapping Project](https://en.wikipedia.org/wiki/UUCP_Mapping_Project "UUCP Mapping Project") (path service) |
| 118 | Yes |  |  | Structured Query Language ([SQL](https://en.wikipedia.org/wiki/SQL "SQL")) Services\[_[jargon](https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style#Technical_language "Wikipedia:Manual of Style")_\] |
| 119 | Yes | Assigned |  | [Network News Transfer Protocol](https://en.wikipedia.org/wiki/Network_News_Transfer_Protocol "Network News Transfer Protocol") (NNTP), retrieval of newsgroup messages |
| 123 | Assigned | Yes |  | [Network Time Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol "Network Time Protocol") (NTP), used for time synchronization |
| 126 | Yes |  |  | Formerly [Unisys](https://en.wikipedia.org/wiki/Unisys "Unisys") Unitary Login, renamed by Unisys to NXEdit. Used by Unisys Programmer's Workbench for Clearpath MCP, an IDE for [Unisys MCP software development](https://en.wikipedia.org/wiki/Unisys_MCP_programming_languages "Unisys MCP programming languages") |
| 135 | Yes |  |  | [Microsoft](https://en.wikipedia.org/wiki/Microsoft "Microsoft") EPMAP (End Point Mapper), also known as DCE/[RPC](https://en.wikipedia.org/wiki/Remote_procedure_call "Remote procedure call") Locator service, used to remotely manage services including [DHCP server](https://en.wikipedia.org/wiki/DHCP_server "DHCP server"), [DNS](https://en.wikipedia.org/wiki/Domain_Name_System "Domain Name System") server and [WINS](https://en.wikipedia.org/wiki/Windows_Internet_Name_Service "Windows Internet Name Service"). Also used by [DCOM](https://en.wikipedia.org/wiki/Distributed_Component_Object_Model "Distributed Component Object Model") |
| 135 | Yes |  |  | [Microsoft](https://en.wikipedia.org/wiki/Microsoft "Microsoft") EPMAP (End Point Mapper), also known as DCE/[RPC](https://en.wikipedia.org/wiki/Remote_procedure_call "Remote procedure call") Locator service, used to remotely manage services including [DHCP server](https://en.wikipedia.org/wiki/DHCP_server "DHCP server"), [DNS](https://en.wikipedia.org/wiki/Domain_Name_System "Domain Name System") server and [WINS](https://en.wikipedia.org/wiki/Windows_Internet_Name_Service "Windows Internet Name Service"). Also used by [DCOM](https://en.wikipedia.org/wiki/Distributed_Component_Object_Model "Distributed Component Object Model") |
| 137 | Yes |  |  | [NetBIOS](https://en.wikipedia.org/wiki/NetBIOS "NetBIOS") Name Service, used for name registration and [resolution](https://en.wikipedia.org/wiki/Name_resolution_(computer_systems) "Name resolution (computer systems)") |
| 138 | Assigned | Yes |  | NetBIOS Datagram Service |
| 139 | Yes | Assigned |  | NetBIOS Session Service |
| 143 | Yes | Assigned |  | [Internet Message Access Protocol](https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol "Internet Message Access Protocol") (IMAP), management of [electronic mail](https://en.wikipedia.org/wiki/Email "Email") messages on a server |
| 151 | Assigned |  |  | [HEMS](https://en.wikipedia.org/wiki/Energy_management_system_(electrical_grid) "Energy management system (electrical grid)") |
| 152 | Yes |  |  | [Background File Transfer Program](/w/index.php?title=Background%5FFile%5FTransfer%5FProgram&action=edit&redlink=1 "Background File Transfer Program (page does not exist)") (BFTP)\[_[importance?](https://en.wikipedia.org/wiki/Wikipedia:What_Wikipedia_is_not#Encyclopedic_content "Wikipedia:What Wikipedia is not")_\] |
| 153 | Yes |  |  | [Simple Gateway Monitoring Protocol](https://en.wikipedia.org/wiki/Simple_Gateway_Monitoring_Protocol "Simple Gateway Monitoring Protocol") (SGMP), a protocol for remote inspection and alteration of gateway management information |
| 156 | Yes |  |  | Structured Query Language ([SQL](https://en.wikipedia.org/wiki/SQL "SQL")) Service\[_[jargon](https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style#Technical_language "Wikipedia:Manual of Style")_\] |
| 158 | Yes |  |  | [Distributed Mail System Protocol](/w/index.php?title=Distributed%5FMail%5FSystem%5FProtocol&action=edit&redlink=1 "Distributed Mail System Protocol (page does not exist)") (DMSP, sometimes referred to as Pcmail)\[_[importance?](https://en.wikipedia.org/wiki/Wikipedia:What_Wikipedia_is_not#Encyclopedic_content "Wikipedia:What Wikipedia is not")_\] |
| 161 | Assigned | Yes |  | [Simple Network Management Protocol](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol "Simple Network Management Protocol") (SNMP) |
| 162 | Yes |  |  | [Simple Network Management Protocol](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol "Simple Network Management Protocol") Trap (SNMPTRAP) |
| 165 | Assigned |  |  | [Xerox](https://en.wikipedia.org/wiki/Xerox "Xerox") |
| 169 | Assigned |  |  | [SEND](https://en.wikipedia.org/wiki/Secure_Neighbor_Discovery "Secure Neighbor Discovery") |
| 170 | Yes |  |  | Network [PostScript](https://en.wikipedia.org/wiki/PostScript "PostScript") [print server](https://en.wikipedia.org/wiki/Print_server "Print server") |
| 175 | Yes |  |  | [VMNET](https://en.wikipedia.org/wiki/VMNET "VMNET") service using [NJE](https://en.wikipedia.org/wiki/Remote_job_entry#Network_Job_Entry "Remote job entry") |
| 177 | Yes |  |  | [X Display Manager Control Protocol](https://en.wikipedia.org/wiki/X_Display_Manager_Control_Protocol "X Display Manager Control Protocol") (XDMCP), used for remote logins to an [X Display Manager](https://en.wikipedia.org/wiki/X_display_manager "X display manager") server\[_[self-published source](https://en.wikipedia.org/wiki/Wikipedia:Verifiability#Self-published_sources "Wikipedia:Verifiability")_\] |
| 179 | Yes | Assigned |  | [Border Gateway Protocol](https://en.wikipedia.org/wiki/Border_Gateway_Protocol "Border Gateway Protocol") (BGP), used to exchange routing and reachability information among [autonomous systems](https://en.wikipedia.org/wiki/Autonomous_system_(Internet) "Autonomous system (Internet)") (AS) on the [Internet](https://en.wikipedia.org/wiki/Internet "Internet") |
| 180 | Assigned |  |  | [ris](https://en.wikipedia.org/wiki/Remote_Installation_Services "Remote Installation Services") |
| 194 | Yes |  |  | [Internet Relay Chat](https://en.wikipedia.org/wiki/Internet_Relay_Chat "Internet Relay Chat") (IRC) |
| 199 | Yes |  |  | [SNMP](https://en.wikipedia.org/wiki/SNMP "SNMP") Unix Multiplexer (SMUX) |
| 201 | Yes |  |  | [AppleTalk](https://en.wikipedia.org/wiki/AppleTalk "AppleTalk") Routing Maintenance |
| 209 | Yes | Assigned |  | [Quick Mail Transfer Protocol](https://en.wikipedia.org/wiki/Quick_Mail_Transfer_Protocol "Quick Mail Transfer Protocol")\[_[self-published source](https://en.wikipedia.org/wiki/Wikipedia:Verifiability#Self-published_sources "Wikipedia:Verifiability")_\] |
| 210 | Yes |  |  | [ANSI](https://en.wikipedia.org/wiki/ANSI "ANSI") [Z39.50](https://en.wikipedia.org/wiki/Z39.50 "Z39.50") |
| 213 | Yes |  |  | [Internetwork Packet Exchange](https://en.wikipedia.org/wiki/Internetwork_Packet_Exchange "Internetwork Packet Exchange") (IPX) |
| 218 | Yes |  |  | Message posting protocol (MPP) |
| 220 | Yes |  |  | [Internet Message Access Protocol](https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol "Internet Message Access Protocol") (IMAP), version 3 |
| 225–241 | Reserved |  |  | [RFC](https://en.wikipedia.org/wiki/RFC_(identifier) "RFC (identifier)") (https://www.rfc-editor.org/rfc/rfc1060) |
| 249–255 | Reserved |  |  | [RFC](https://en.wikipedia.org/wiki/RFC_(identifier) "RFC (identifier)") (https://www.rfc-editor.org/rfc/rfc1060) |
| 259 | Yes |  |  | Efficient Short Remote Operations (ESRO) |
| 262 | Yes |  |  | Arcisdms |
| 264 | Yes |  |  | [Border Gateway Multicast Protocol](https://en.wikipedia.org/wiki/Border_Gateway_Multicast_Protocol "Border Gateway Multicast Protocol") (BGMP) |
| 280 | Yes |  |  | http-mgmt |
| 300 | Unofficial |  |  | [ThinLinc](https://en.wikipedia.org/wiki/ThinLinc "ThinLinc") Web Access, Spartan protocol |
| 308 | Yes |  |  | Novastor Online Backup |
| 311 | Yes | Assigned |  | [macOS Server](https://en.wikipedia.org/wiki/MacOS_Server "MacOS Server") Admin (officially [AppleShare](https://en.wikipedia.org/wiki/AppleShare "AppleShare") IP Web administration) |
| 312 | Unofficial | No |  | macOS [Xsan](https://en.wikipedia.org/wiki/Xsan "Xsan") administration |
| 318 | Yes |  |  | PKIX [Time Stamp Protocol](https://en.wikipedia.org/wiki/Time_Stamp_Protocol "Time Stamp Protocol") (TSP) |
| 319 | Yes |  |  | [Precision Time Protocol](https://en.wikipedia.org/wiki/Precision_Time_Protocol "Precision Time Protocol") (PTP) event messages |
| 320 | Yes |  |  | [Precision Time Protocol](https://en.wikipedia.org/wiki/Precision_Time_Protocol "Precision Time Protocol") (PTP) general messages |
| 323 | Yes |  |  | [Resource Public Key Infrastructure](https://en.wikipedia.org/wiki/Resource_Public_Key_Infrastructure "Resource Public Key Infrastructure") |
| 350 | Yes |  |  | [Mapping of Airline Traffic over Internet Protocol](https://en.wikipedia.org/wiki/Mapping_of_Airline_Traffic_over_Internet_Protocol "Mapping of Airline Traffic over Internet Protocol") (MATIP) type A |
| 351 | Yes |  |  | MATIP type B |
| 356 | Yes |  |  | cloanto-net-1 (used by Cloanto Amiga Explorer and VMs) |
| 366 | Yes |  |  | On-Demand Mail Relay (ODMR) |
| 369 | Yes |  |  | Rpc2portmap |
| 370 | Yes |  |  | securecast1, outgoing packets to [NAI](https://en.wikipedia.org/wiki/McAfee "McAfee")'s SecureCast serversAs of 2000[\[update\]](https://en.wikipedia.org/w/index.php?title=List%5Fof%5FTCP%5Fand%5FUDP%5Fport%5Fnumbers&action=edit) |
| 370 | Yes |  |  | securecast1, outgoing packets to [NAI](https://en.wikipedia.org/wiki/McAfee "McAfee")'s SecureCast serversAs of 2000[\[update\]](https://en.wikipedia.org/w/index.php?title=List%5Fof%5FTCP%5Fand%5FUDP%5Fport%5Fnumbers&action=edit) |
| 371 | Yes |  |  | ClearCase albd |
| 376 | Yes |  |  | [Amiga](https://en.wikipedia.org/wiki/Amiga "Amiga") Envoy Network Inquiry Protocol |
| 383 | Yes |  |  | HP data alarm manager |
| 384 | Yes |  |  | A Remote Network Server System |
| 387 | Yes |  |  | AURP ([AppleTalk](https://en.wikipedia.org/wiki/AppleTalk "AppleTalk") Update-based Routing Protocol) |
| 388 | Yes | Assigned |  | [Unidata LDM](https://en.wikipedia.org/wiki/Local_Data_Manager "Local Data Manager") near real-time data distribution protocol\[_[self-published source](https://en.wikipedia.org/wiki/Wikipedia:Verifiability#Self-published_sources "Wikipedia:Verifiability")_\]\[_[self-published source](https://en.wikipedia.org/wiki/Wikipedia:Verifiability#Self-published_sources "Wikipedia:Verifiability")_\] |
| 389 | Yes | Assigned |  | [Lightweight Directory Access Protocol](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol "Lightweight Directory Access Protocol") (LDAP) |
| 399 | Yes |  |  | [Digital Equipment Corporation](https://en.wikipedia.org/wiki/Digital_Equipment_Corporation "Digital Equipment Corporation") [DECnet+](/w/index.php?title=DECnet%2B&action=edit&redlink=1 "DECnet+ (page does not exist)") (Phase V) over TCP/IP (RFC1859) |
| 401 | Yes |  |  | [Uninterruptible power supply](https://en.wikipedia.org/wiki/Uninterruptible_power_supply "Uninterruptible power supply") (UPS) |
| 427 | Yes |  |  | [Service Location Protocol](https://en.wikipedia.org/wiki/Service_Location_Protocol "Service Location Protocol") (SLP) |
| 433 | Yes |  |  | NNTP, part of [Network News Transfer Protocol](https://en.wikipedia.org/wiki/Network_News_Transfer_Protocol "Network News Transfer Protocol") |
| 434 | Yes |  |  | [Mobile IP](https://en.wikipedia.org/wiki/Mobile_IP "Mobile IP") Agent (RFC 5944) |
| 443 | Yes | Yes |  | [Hypertext Transfer Protocol Secure](https://en.wikipedia.org/wiki/HTTPS "HTTPS") (HTTPS) uses TCP in versions 1.x and 2\. [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3 "HTTP/3") uses QUIC, a transport protocol on top of UDP |
| 444 | Yes |  |  | [Simple Network Paging Protocol](https://en.wikipedia.org/wiki/Simple_Network_Paging_Protocol "Simple Network Paging Protocol") (SNPP), RFC 1568 |
| 445 | Yes |  |  | Microsoft-DS (Directory Services) [Active Directory](https://en.wikipedia.org/wiki/Active_Directory "Active Directory"), Windows shares |
| 445 | Yes | Assigned |  | Microsoft-DS (Directory Services) [SMB](https://en.wikipedia.org/wiki/Server_Message_Block "Server Message Block") file sharing |
| 464 | Yes |  |  | Kpasswd: [Kerberos](https://en.wikipedia.org/wiki/Kerberos_(protocol) "Kerberos (protocol)") Change/Set password |
| 465 | Yes | No |  | Message Submission over TLS protocol |
| 465 | Yes | No |  | URL Rendezvous Directory for Cisco SSM |
| 475 | Yes |  |  | tcpnethaspsrv, [Aladdin Knowledge Systems](https://en.wikipedia.org/wiki/Aladdin_Knowledge_Systems "Aladdin Knowledge Systems") Hasp services |
| 476–490 | Unofficial |  |  | Centro Software ERP ports |
| 491 | Unofficial |  |  | [GO-Global remote access and application publishing software](https://en.wikipedia.org/wiki/GO-Global "GO-Global") |
| 497 | Yes |  |  | [Retrospect](https://en.wikipedia.org/wiki/Retrospect_(software) "Retrospect (software)") |
| 500 | Assigned | Yes |  | [Internet Security Association and Key Management Protocol](https://en.wikipedia.org/wiki/Internet_Security_Association_and_Key_Management_Protocol "Internet Security Association and Key Management Protocol") (ISAKMP) / [Internet Key Exchange](https://en.wikipedia.org/wiki/Internet_Key_Exchange "Internet Key Exchange") (IKE) |
| 502 | Yes |  |  | [Modbus](https://en.wikipedia.org/wiki/Modbus "Modbus") Protocol |
| 504 | Yes |  |  | [Citadel](https://en.wikipedia.org/wiki/Citadel/UX "Citadel/UX"), multiservice protocol for dedicated clients for the Citadel groupware system |
| 510 | Yes |  |  | FirstClass Protocol (FCP), used by [FirstClass](https://en.wikipedia.org/wiki/FirstClass "FirstClass") client/server groupware system |
| 512 | Yes |  |  | [Rexec](https://en.wikipedia.org/wiki/Remote_Process_Execution "Remote Process Execution"), Remote Process Execution |
| 512 | Yes |  |  | [Rexec](https://en.wikipedia.org/wiki/Remote_Process_Execution "Remote Process Execution"), Remote Process Execution |
| 513 | Yes |  |  | [rlogin](https://en.wikipedia.org/wiki/Rlogin "Rlogin") |
| 513 | Yes |  |  | [rlogin](https://en.wikipedia.org/wiki/Rlogin "Rlogin") |
| 514 | Unofficial |  |  | [Remote Shell](https://en.wikipedia.org/wiki/Remote_Shell "Remote Shell"), used to execute non-interactive commands on a remote system (Remote Shell, rsh, remsh) |
| 514 | No | Yes |  | [Syslog](https://en.wikipedia.org/wiki/Syslog "Syslog"), used for system logging |
| 515 | Yes | Assigned |  | [Line Printer Daemon](https://en.wikipedia.org/wiki/Line_Printer_Daemon_protocol "Line Printer Daemon protocol") (LPD), print service |
| 517 | Yes |  |  | [Talk](https://en.wikipedia.org/wiki/Talk_(software) "Talk (software)") |
| 518 | Yes |  |  | NTalk |
| 520 | Yes |  |  | [Routing Information Protocol](https://en.wikipedia.org/wiki/Routing_Information_Protocol "Routing Information Protocol") (RIP) |
| 520 | Yes |  |  | [Routing Information Protocol](https://en.wikipedia.org/wiki/Routing_Information_Protocol "Routing Information Protocol") (RIP) |
| 521 | Yes |  |  | [Routing Information Protocol Next Generation](https://en.wikipedia.org/wiki/RIPng "RIPng") (RIPng) |
| 524 | Yes |  |  | [NetWare Core Protocol](https://en.wikipedia.org/wiki/NetWare_Core_Protocol "NetWare Core Protocol") (NCP) is used for a variety things such as access to primary NetWare server resources, Time Synchronization, etc |
| 525 | Yes |  |  | Timed, [Timeserver](https://en.wikipedia.org/wiki/Timeserver "Timeserver") |
| 530 | Yes |  |  | [Remote procedure call](https://en.wikipedia.org/wiki/Remote_procedure_call "Remote procedure call") (RPC) |
| 532 | Yes | Assigned |  | netnews |
| 533 | Yes |  |  | netwall, for emergency broadcasts |
| 540 | Yes |  |  | Unix-to-Unix Copy Protocol ([UUCP](https://en.wikipedia.org/wiki/UUCP "UUCP")) |
| 542 | Yes |  |  | [commerce](https://en.wikipedia.org/wiki/Commerce "Commerce") (Commerce Applications) |
| 543 | Yes |  |  | klogin, [Kerberos](https://en.wikipedia.org/wiki/Kerberos_(protocol) "Kerberos (protocol)") login |
| 544 | Yes |  |  | kshell, Kerberos Remote shell |
| 546 | Yes |  |  | [DHCPv6](https://en.wikipedia.org/wiki/DHCPv6 "DHCPv6") client |
| 547 | Yes |  |  | DHCPv6 server |
| 548 | Yes | Assigned |  | [Apple Filing Protocol](https://en.wikipedia.org/wiki/Apple_Filing_Protocol "Apple Filing Protocol") (AFP) over [TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol "Transmission Control Protocol") |
| 550 | Yes |  |  | new-rwho, new-who |
| 554 | Yes |  |  | [Real Time Streaming Protocol](https://en.wikipedia.org/wiki/Real_Time_Streaming_Protocol "Real Time Streaming Protocol") (RTSP) |
| 556 | Yes |  |  | Remotefs, [RFS](https://en.wikipedia.org/wiki/Remote_File_System "Remote File System"), rfs\_server |
| 560 | Yes |  |  | rmonitor, Remote Monitor |
| 561 | Yes |  |  | monitor |
| 563 | Yes |  |  | [NNTP](https://en.wikipedia.org/wiki/NNTP "NNTP") over [TLS/SSL](https://en.wikipedia.org/wiki/Transport_Layer_Security "Transport Layer Security") (NNTPS) |
| 564 | Unofficial |  |  | [9P](https://en.wikipedia.org/wiki/9P_(protocol) "9P (protocol)") ([Plan 9](https://en.wikipedia.org/wiki/Plan_9_from_Bell_Labs "Plan 9 from Bell Labs")) |
| 585 | No |  |  | Previously assigned for use of [Internet Message Access Protocol](https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol "Internet Message Access Protocol") over [TLS/SSL](https://en.wikipedia.org/wiki/Transport_Layer_Security "Transport Layer Security") (IMAPS), now deregistered in favour of port 993 |
| 587 | Yes | Assigned |  | [Email Message Submission](https://en.wikipedia.org/wiki/Mail_submission_agent "Mail submission agent") (No longer preferred; see port 465.) |
| 591 | Yes |  |  | [FileMaker](https://en.wikipedia.org/wiki/FileMaker "FileMaker") 6.0 (and later) Web Sharing (HTTP Alternate, also see port 80) |
| 593 | Yes |  |  | HTTP RPC Ep Map, [Remote procedure call](https://en.wikipedia.org/wiki/Remote_procedure_call "Remote procedure call") over [Hypertext Transfer Protocol](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol "Hypertext Transfer Protocol"), often used by [Distributed Component Object Model](https://en.wikipedia.org/wiki/Distributed_Component_Object_Model "Distributed Component Object Model") services and [Microsoft Exchange Server](https://en.wikipedia.org/wiki/Microsoft_Exchange_Server "Microsoft Exchange Server") |
| 601 | Yes |  |  | Reliable [Syslog](https://en.wikipedia.org/wiki/Syslog "Syslog") Service — used for system logging |
| 604 | Yes |  |  | TUNNEL profile, a protocol for [BEEP](https://en.wikipedia.org/wiki/BEEP "BEEP") [peers](https://en.wikipedia.org/wiki/Peer-to-peer "Peer-to-peer") to form an [application layer](https://en.wikipedia.org/wiki/Application_layer "Application layer") [tunnel](https://en.wikipedia.org/wiki/Tunneling_protocol "Tunneling protocol") |
| 623 | Yes |  |  | ASF Remote Management and Control Protocol (ASF-[RMCP](https://en.wikipedia.org/wiki/Intelligent_Platform_Management_Interface#RMCP "Intelligent Platform Management Interface")) & IPMI Remote Management Protocol |
| 625 | Unofficial | No |  | Open Directory Proxy (ODProxy) |
| 631 | Yes |  |  | [Internet Printing Protocol](https://en.wikipedia.org/wiki/Internet_Printing_Protocol "Internet Printing Protocol") (IPP) |
| 631 | Unofficial |  |  | [CUPS](https://en.wikipedia.org/wiki/CUPS "CUPS") administration console (extension to IPP) |
| 635 | Yes |  |  | RLZ DBase |
| 636 | Yes | Assigned |  | [Lightweight Directory Access Protocol](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol "Lightweight Directory Access Protocol") over [TLS/SSL](https://en.wikipedia.org/wiki/Transport_Layer_Security "Transport Layer Security") (LDAPS) |
| 639 | Yes |  |  | [Multicast Source Discovery Protocol](https://en.wikipedia.org/wiki/Multicast_Source_Discovery_Protocol "Multicast Source Discovery Protocol"), MSDP |
| 641 | Yes |  |  | SupportSoft Nexus Remote Command (control/listening), a proxy gateway connecting remote control traffic |
| 643 | Yes |  |  | SANity |
| 646 | Yes |  |  | [Label Distribution Protocol](https://en.wikipedia.org/wiki/Label_Distribution_Protocol "Label Distribution Protocol") (LDP), a routing protocol used in [MPLS](https://en.wikipedia.org/wiki/Multiprotocol_Label_Switching "Multiprotocol Label Switching") networks |
| 647 | Yes |  |  | [DHCP Failover](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol#Reliability "Dynamic Host Configuration Protocol") protocol |
| 648 | Yes |  |  | Registry Registrar Protocol (RRP) |
| 651 | Yes |  |  | IEEE-MMS |
| 653 | Yes |  |  | SupportSoft Nexus Remote Command (data), a proxy gateway connecting remote control traffic |
| 654 | Yes |  |  | Media Management System (MMS) Media Management Protocol (MMP) |
| 655 | Yes |  |  | [Tinc](https://en.wikipedia.org/wiki/Tinc_(protocol) "Tinc (protocol)") VPN daemon |
| 657 | Yes |  |  | [IBM](https://en.wikipedia.org/wiki/IBM "IBM") RMC (Remote monitoring and Control) protocol, used by [System p5](https://en.wikipedia.org/wiki/IBM_System_p "IBM System p") [AIX](https://en.wikipedia.org/wiki/IBM_AIX "IBM AIX") Integrated Virtualization Manager (IVM) and [Hardware Management Console](https://en.wikipedia.org/wiki/IBM_Hardware_Management_Console "IBM Hardware Management Console") to connect managed [logical partitions (LPAR)](https://en.wikipedia.org/wiki/LPAR "LPAR") to enable dynamic partition reconfiguration |
| 660 | Yes | Assigned |  | [macOS Server](https://en.wikipedia.org/wiki/MacOS_Server "MacOS Server") administration, version 10.4 and earlier |
| 662 | Yes |  |  | NFS v3 Statd port |
| 666 | Yes |  |  | _[Doom](https://en.wikipedia.org/wiki/Doom_(1993_video_game) "Doom (1993 video game)")_, the first online [first-person shooter](https://en.wikipedia.org/wiki/First-person_shooter "First-person shooter") |
| 666 | Unofficial |  |  | airserv-ng, [aircrack-ng](https://en.wikipedia.org/wiki/Aircrack-ng "Aircrack-ng")'s server for remote-controlling wireless devices |
| 674 | Yes |  |  | [Application Configuration Access Protocol](https://en.wikipedia.org/wiki/Application_Configuration_Access_Protocol "Application Configuration Access Protocol") (ACAP) |
| 684 | Yes |  |  | [CORBA](https://en.wikipedia.org/wiki/Common_Object_Request_Broker_Architecture "Common Object Request Broker Architecture") IIOP SSL |
| 688 | Yes |  |  | REALM-RUSD (ApplianceWare Server Appliance Management Protocol) |
| 690 | Yes |  |  | Velneo Application Transfer Protocol (VATP) |
| 691 | Yes |  |  | [MS](https://en.wikipedia.org/wiki/Microsoft "Microsoft") [Exchange](https://en.wikipedia.org/wiki/Microsoft_Exchange_Server "Microsoft Exchange Server") Routing |
| 694 | Yes |  |  | [Linux-HA](https://en.wikipedia.org/wiki/Linux-HA "Linux-HA") high-availability heartbeat |
| 695 | Yes | Assigned |  | [IEEE](https://en.wikipedia.org/wiki/IEEE "IEEE") Media Management System over [SSL](https://en.wikipedia.org/wiki/Transport_Layer_Security "Transport Layer Security") (IEEE-MMS-SSL) |
| 698 | Yes |  |  | [Optimized Link State Routing](https://en.wikipedia.org/wiki/Optimized_Link_State_Routing_protocol "Optimized Link State Routing protocol") (OLSR) |
| 700 | Yes |  |  | [Extensible Provisioning Protocol](https://en.wikipedia.org/wiki/Extensible_Provisioning_Protocol "Extensible Provisioning Protocol") (EPP), a protocol for communication between [domain name registries](https://en.wikipedia.org/wiki/Domain_name_registry "Domain name registry") and [registrars](https://en.wikipedia.org/wiki/Domain_name_registrar "Domain name registrar") (RFC 5734) |
| 701 | Yes |  |  | Link Management Protocol (LMP), a protocol that runs between a pair of [nodes](https://en.wikipedia.org/wiki/Node_(networking) "Node (networking)") and is used to manage [traffic engineering](https://en.wikipedia.org/wiki/Teletraffic_engineering "Teletraffic engineering") (TE) [links](https://en.wikipedia.org/wiki/Telecommunications_link "Telecommunications link") |
| 702 | Yes |  |  | IRIS (Internet Registry Information Service) over [BEEP](https://en.wikipedia.org/wiki/BEEP "BEEP") (Blocks Extensible Exchange Protocol) (RFC 3983) |
| 706 | Yes |  |  | [Secure Internet Live Conferencing](https://en.wikipedia.org/wiki/SILC_(protocol) "SILC (protocol)") (SILC) |
| 711 | Yes |  |  | [Cisco](https://en.wikipedia.org/wiki/Cisco "Cisco") Tag Distribution Protocol—being replaced by the MPLS [Label Distribution Protocol](https://en.wikipedia.org/wiki/Label_Distribution_Protocol "Label Distribution Protocol") |
| 712 | Yes |  |  | [Topology Broadcast based on Reverse-Path Forwarding routing protocol](https://en.wikipedia.org/wiki/Topology_Broadcast_based_on_Reverse-Path_Forwarding_routing_protocol "Topology Broadcast based on Reverse-Path Forwarding routing protocol") (TBRPF; RFC 3684) |
| 749 | Yes |  |  | Kerberos administration |
| 750 | Yes |  |  | kerberos-iv, [Kerberos](https://en.wikipedia.org/wiki/Kerberos_(protocol) "Kerberos (protocol)") version IV |
| 751 | Unofficial |  |  | kerberos_master, Kerberos authentication |
| 752 | Unofficial |  |  | passwd_server, Kerberos password (kpasswd) server |
| 753 | Yes |  |  | Reverse Routing Header (RRH) |
| 753 | Unofficial |  |  | userreg_server, Kerberos userreg server |
| 754 | Yes |  |  | tell send |
| 754 | Unofficial |  |  | krb5_prop, Kerberos v5 slave propagation |
| 760 | Unofficial |  |  | krbupdate \[kreg\], Kerberos registration |
| 777 | Unofficial |  |  | machine socket eXtension \[msx\] protocol |
| 782 | Unofficial |  |  | [Conserver](https://en.wikipedia.org/wiki/Conserver "Conserver") serial-console management server |
| 783 | Unofficial |  |  | [SpamAssassin](https://en.wikipedia.org/wiki/SpamAssassin "SpamAssassin") spamd daemon |
| 800 | Yes |  |  | mdbs-daemon |
| 802 | Yes |  |  | [MODBUS](https://en.wikipedia.org/wiki/Modbus "Modbus")/TCP Security |
| 808 | Unofficial |  |  | Microsoft Net.TCP Port Sharing Service |
| 829 | Yes | Assigned |  | [Certificate Management Protocol](https://en.wikipedia.org/wiki/Certificate_Management_Protocol "Certificate Management Protocol") |
| 830 | Yes |  |  | [NETCONF](https://en.wikipedia.org/wiki/NETCONF "NETCONF") over [SSH](https://en.wikipedia.org/wiki/Secure_Shell "Secure Shell") |
| 831 | Yes |  |  | NETCONF over [BEEP](https://en.wikipedia.org/wiki/BEEP "BEEP") |
| 832 | Yes |  |  | NETCONF for [SOAP](https://en.wikipedia.org/wiki/SOAP "SOAP") over HTTPS |
| 833 | Yes |  |  | NETCONF for SOAP over BEEP |
| 843 | Unofficial |  |  | [Adobe Flash](https://en.wikipedia.org/wiki/Adobe_Flash "Adobe Flash") |
| 847 | Yes |  |  | DHCP Failover protocol |
| 848 | Yes |  |  | Group Domain Of Interpretation (GDOI) protocol |
| 853 | Yes |  |  | DNS over TLS(RFC 7858) |
| 853 | Yes |  |  | DNS over QUIC or DNS over DTLS |
| 860 | Yes |  |  | iSCSI(RFC 3720) |
| 861 | Yes |  |  | OWAMP control (RFC 4656) |
| 862 | Yes |  |  | TWAMP control (RFC 5357) |
| 873 | Yes |  |  | rsync file synchronization protocol |
| 888 | Unofficial |  |  | cddbp, CD DataBase(CDDB) protocol (CDDBP) |
| 888 | Unofficial |  |  | IBM Endpoint Manager Remote Control |
| 892 | Yes |  |  | NFS v3 Mountd port |
| 897 | Unofficial |  |  | Brocade SMI-S RPC |
| 898 | Unofficial |  |  | Brocade SMI-S RPC SSL |
| 902 | Unofficial |  |  | VMware ESXi |
| 903 | Unofficial |  |  | VMware ESXi |
| 953 | Yes | Reserved |  | BIND remote name daemon control (RNDC) |
| 981 | Unofficial |  |  | Remote HTTPS management for firewall devices running embedded Check Point VPN-1 software |
| 987 | Unofficial |  |  | Sony PlayStation Wake On Lan |
| 987 | Unofficial |  |  | Microsoft Remote Web Workplace, a feature of Windows Small Business Server |
| 988 | Unofficial |  |  | Lustre (file system) Protocol (data) |
| 989 | Yes |  |  | FTPS Protocol (data), FTP over TLS/SSL |
| 990 | Yes |  |  | FTPS Protocol (control), FTP over TLS/SSL |
| 991 | Yes |  |  | Netnews Administration System (NAS) |
| 992 | Yes |  |  | Telnet protocol over TLS/SSL |
| 993 | Yes | Assigned |  | Internet Message Access Protocol over TLS/SSL(IMAPS) |
| 994 | Reserved |  |  | Previously assigned to Internet Relay Chat over TLS/SSL(IRCS), but was not used in common practice |
| 995 | Yes |  |  | Post Office Protocol 3 over TLS/SSL(POP3S) |
| 1010 | Unofficial |  |  | ThinLinc web-based administration interface |
| 1011–1020 | Reserved |  |  |  |
| 1023 | Reserved |  |  |  |
| 1023 | Unofficial |  |  | z/OS Network File System (NFS) (potentially ports 991–1023) |

---

## Registered ports (1024–49151)

| Port | TCP | UDP | Observations | Description |
|------|-----|-----|--------------|-------------|
| 1024 | Reserved | Reserved |  |  |
| 1025 | Assigned |  |  | network blackjack |
| 1027 | Reserved | Reserved |  |  |
| 1027 | Yes |  |  | Native IPv6 behind IPv4-to-IPv4 NAT Customer Premises Equipment (6a44) |
| 1029 | Unofficial |  |  | Microsoft DCOM services |
| 1058 | Yes |  |  | nim, IBM AIX Network Installation Manager(NIM) |
| 1059 | Yes |  |  | nimreg, IBM AIX Network Installation Manager (NIM) |
| 1080 | Yes |  |  | SOCKS proxy |
| 1085 | Yes |  |  | WebObjects |
| 1098 | Yes |  |  | rmiactivation, Java remote method invocation(RMI) activation |
| 1099 | Yes | Assigned |  | rmiregistry, Java remote method invocation (RMI) registry |
| 1100 | Unofficial |  |  | SaltoSystems – Handshake for IP-Components |
| 1112 | Unofficial |  |  | ESET virus updates |
| 1113 | Assigned | Yes |  | Licklider Transmission Protocol(LTP) delay tolerant networking protocol |
| 1119 | Yes |  |  | Battle.net chat/game protocol, used by Blizzard's games |
| 1144 | Yes |  |  | fuscript (Fusion Script) used by Blackmagic Design Fusion and DaVinci Resolve |
| 1167 | Yes | Yes |  | Cisco IP SLA(Service Assurance Agent) |
| 1194 | Yes |  |  | OpenVPN |
| 1198 | Yes |  |  | The cajo project Free dynamic transparent distributed computing in Java |
| 1212 | Unofficial |  |  | Equalsocial Fediverse protocol |
| 1214 | Yes |  |  | Kazaa |
| 1220 | Yes | Assigned |  | QuickTime Streaming Server administration |
| 1234 | Yes |  |  | Infoseek search agent |
| 1234 | Unofficial |  |  | VLC media player default port for UDP/RTP stream |
| 1241 | Unofficial |  |  | Nessus Security Scanner |
| 1270 | Yes |  |  | Microsoft System Center Operations Manager(SCOM) (formerly Microsoft Operations Manager (MOM)) agent |
| 1293 | Yes |  |  | Internet Protocol Security (IPSec) |
| 1311 | Yes |  |  | Windows`RxMon.exe` |
| 1311 | Unofficial |  |  | Dell OpenManage HTTPS |
| 1314 | Unofficial |  |  | Festival Speech Synthesis System server |
| 1319 | Yes |  |  | AMX ICSP (Protocol for communications with AMX control systems devices) |
| 1337 | Yes |  |  | Men&Mice DNS |
| 1337 | Unofficial |  |  | Strapi |
| 1337 | Unofficial |  |  | Razer Chroma SDK Server |
| 1337 | Unofficial |  |  | Sails.js default port |
| 1341 | Yes |  |  | Qubes (Manufacturing Execution System) |
| 1344 | Yes |  |  | Internet Content Adaptation Protocol |
| 1352 | Yes |  |  | HCL Notes / Domino(RPC) protocol |
| 1360 | Yes |  |  | Mimer SQL |
| 1414 | Yes |  |  | IBM WebSphere MQ(formerly known as MQSeries) |
| 1417 | Yes |  |  | Timbuktu Service 1 Port |
| 1418 | Yes |  |  | Timbuktu Service 2 Port |
| 1419 | Yes |  |  | Timbuktu Service 3 Port |
| 1420 | Yes |  |  | Timbuktu Service 4 Port |
| 1431 | Yes |  |  | Reverse Gossip Transport Protocol(RGTP), used to access a General-purpose Reverse-Ordered Gossip Gathering System (GROGGS) bulletin board, such as that implemented on the Cambridge University's Phoenix system |
| 1433 | Yes |  |  | Microsoft SQL Server database management system(MSSQL) server |
| 1434 | Yes |  |  | Microsoft SQL Server database management system (MSSQL) monitor |
| 1476 | Yes |  |  | WiFi Pineapple Hak5 |
| 1481 | Yes |  |  | AIRS data interchange |
| 1492 | Unofficial |  |  | Sid Meier's CivNet, a multiplayer remake of the original Sid Meier's Civilization game |
| 1494 | Unofficial |  |  | Citrix Independent Computing Architecture(ICA) |
| 1500 | Unofficial |  |  | IBM Tivoli Storage Manager server |
| 1501 | Unofficial |  |  | IBM Tivoli Storage Manager client scheduler |
| 1503 | Unofficial |  |  | Windows Live Messenger(Whiteboard and Application Sharing) |
| 1512 | Yes |  |  | Microsoft's Windows Internet Name Service(WINS) |
| 1513 | Unofficial |  |  | Garena game client |
| 1521 | Yes |  |  | nCUBE License Manager |
| 1521 | Unofficial |  |  | Oracle database default listener, in future releases official port 2483 (TCP/IP) and 2484 (TCP/IP with SSL) |
| 1524 | Yes |  |  | ingreslock, ingres |
| 1527 | Yes |  |  | Oracle Net Services, formerly known as SQL*Net |
| 1527 | Unofficial |  |  | Apache Derby Network Server |
| 1533 | Yes |  |  | IBM Sametime Virtual Places Chat |
| 1534 | No | Unofficial |  | Eclipse Target Communication Framework |
| 1540 | Unofficial |  |  | 1C:Enterprise server agent (ragent) |
| 1541 | Unofficial |  |  | 1C:Enterprise master cluster manager (rmngr) |
| 1542 | Unofficial |  |  | 1C:Enterprise configuration repository server |
| 1545 | Unofficial |  |  | 1C:Enterprise cluster administration server (RAS) |
| 1547 | Yes |  |  | Laplink |
| 1550 | Unofficial |  |  | 1C:Enterprise debug server |
| 1550 | Unofficial |  |  | Gadu-Gadu(direct client-to-client) |
| 1560–1590 | Unofficial |  |  | 1C:Enterprise cluster working processes |
| 1581 | Yes |  |  | MIL STD 2045-47001 VMF |
| 1581 | Unofficial |  |  | IBM Tivoli Storage Manager web client |
| 1582–1583 | Unofficial |  |  | IBM Tivoli Storage Manager server web interface |
| 1583 | Unofficial |  |  | Pervasive PSQL |
| 1589 | Yes |  |  | Cisco VLAN Query Protocol (VQP) |
| 1604 | Unofficial |  |  | DarkComet remote administration tool (RAT) |
| 1626 | Unofficial |  |  | iSketch |
| 1627 | Unofficial |  |  | iSketch |
| 1628 | Yes |  |  | LonTalk normal |
| 1629 | Yes |  |  | LonTalk urgent |
| 1645 | No | Unofficial |  | Early deployment of RADIUS before RFC standardization was done using UDP port number 1645. Enabled for compatibility reasons by default on Cisco and Juniper Networks RADIUS servers. Official port is 1812. TCP port 1645 must not be used for RADIUS |
| 1646 | No | Unofficial |  | Old`radacct` port, RADIUS accounting protocol. Enabled for compatibility reasons by default on Cisco and Juniper Networks RADIUS servers. Official port is 1813. TCP port 1646 must not be used for RADIUS |
| 1666 | Unofficial |  |  | Perforce |
| 1677 | Yes |  |  | Novell GroupWise clients in client/server access mode |
| 1688 | Unofficial |  |  | Microsoft Key Management Service(KMS) for Windows Activation |
| 1701 | Yes |  |  | Layer 2 Forwarding Protocol(L2F) |
| 1701 | Assigned | Yes |  | Layer 2 Tunneling Protocol(L2TP) |
| 1707 | Yes |  |  | Windward Studios games (vdmplay) |
| 1707 | Unofficial |  |  | L2TP/IPsec, for establishing an initial connection |
| 1714–1764 | Unofficial |  |  | KDE Connect |
| 1716 | Unofficial |  |  | America's Army, a massively multiplayer online game(MMO) |
| 1719 | Yes |  |  | H.323 registration and alternate communication |
| 1720 | Yes |  |  | H.323 call signaling |
| 1723 | Yes | Assigned |  | Point-to-Point Tunneling Protocol(PPTP) |
| 1755 | Yes |  |  | Microsoft Media Services(MMS,`ms-streaming`) |
| 1761 | Unofficial |  |  | Novell ZENworks |
| 1776 | Yes |  |  | Emergency management information system |
| 1801 | Yes |  |  | Microsoft Message Queuing |
| 1812 | Yes |  |  | RADIUS authentication protocol,`radius` |
| 1813 | Yes |  |  | RADIUS accounting protocol,`radius-acct` |
| 1863 | Yes |  |  | Microsoft Notification Protocol(MSNP), used by the Microsoft Messenger service and a number of instant messaging Messenger clients |
| 1880 | Unofficial |  |  | Node-RED |
| 1883 | Yes |  |  | MQTT(formerly MQ Telemetry Transport) |
| 1900 | Assigned | Yes |  | Simple Service Discovery Protocol(SSDP), discovery of UPnP devices |
| 1935 | Yes |  |  | Macromedia Flash Communications Server MX, the precursor to Adobe Flash Media Server before Macromedia's acquisition by Adobe on December 3, 2005 |
| 1935 | Unofficial |  |  | Real Time Messaging Protocol(RTMP), primarily used in Adobe Flash |
| 1965 | Unofficial | No |  | Gemini, a lightweight, collaboratively designed protocol, striving to fill the gap between Gopher and HTTP |
| 1967 | Unofficial |  |  | Cisco IOS IP Service Level Agreements (IP SLAs) Control Protocol |
| 1972 | Yes |  |  | InterSystems Caché, and InterSystems IRIS versions 2020.3 and later |
| 1984 | Yes |  |  | Big Brother |
| 1984 | Unofficial |  |  | Arweave mining node |
| 1985 | Assigned | Yes |  | Cisco Hot Standby Router Protocol(HSRP) |
| 1998 | Yes |  |  | Cisco X.25 over TCP (XOT) service |
| 2000 | Yes |  |  | Cisco Skinny Client Control Protocol(SCCP) |
| 2001–2009 | Unofficial |  |  | hexss http server (python package) |
| 2010 | Unofficial |  |  | Artemis: Spaceship Bridge Simulator |
| 2019 | Unofficial |  |  | Caddy admin API endpoint |
| 2033 | Unofficial |  |  | Civilization IV multiplayer |
| 2049 | Yes | Yes |  | Network File System(NFS) |
| 2056 | Unofficial |  |  | Civilization IV multiplayer |
| 2080 | Yes |  |  | Autodesk NLM (FLEXlm) |
| 2082 | Unofficial |  |  | cPanel default |
| 2083 | Yes |  |  | Secure RADIUS Service (radsec) |
| 2083 | Unofficial |  |  | cPanel default TLS |
| 2086 | Yes |  |  | GNUnet |
| 2086 | Unofficial |  |  | WebHost Manager default |
| 2087 | Unofficial |  |  | WebHost Manager default TLS |
| 2095 | Yes |  |  | cPanel default web mail |
| 2096 | Unofficial |  |  | cPanel default TLS web mail |
| 2100 | Unofficial |  |  | Warzone 2100 multiplayer |
| 2101 | Unofficial |  |  | Networked Transport of RTCM via Internet Protocol(NTRIP) |
| 2102 | Yes |  |  | Zephyr Notification Service server |
| 2103 | Yes |  |  | Zephyr Notification Service`serv-hm` connection |
| 2104 | Yes |  |  | Zephyr Notification Service hostmanager |
| 2123 | Yes |  |  | GTP control messages (GTP-C) |
| 2142 | Yes |  |  | TDMoIP(TDM over IP) |
| 2152 | Yes |  |  | GTP user data messages (GTP-U) |
| 2159 | Yes |  |  | GDB remote debug port |
| 2181 | Yes |  |  | EForward-document transport system |
| 2181 | Unofficial |  |  | Apache ZooKeeper default client port |
| 2195 | Unofficial |  |  | Apple Push Notification Service, binary, gateway. Deprecated March 2021 |
| 2196 | Unofficial |  |  | Apple Push Notification Service, binary, feedback. Deprecated March 2021 |
| 2197 | Unofficial |  |  | Apple Push Notification Service, HTTP/2, JSON-based API |
| 2210 | Yes |  |  | NOAAPORT Broadcast Network |
| 2211 | Yes |  |  | EMWIN |
| 2221 | Unofficial |  |  | ESET anti-virus updates |
| 2222 | Yes |  |  | EtherNet/IP implicit messaging for IO data |
| 2222 | Unofficial |  |  | DirectAdmin Access |
| 2222–2226 | Yes |  |  | ESET Remote administrator |
| 2240 | Yes |  |  | General Dynamics Remote Encryptor Configuration Information Protocol (RECIPe) |
| 2261 | Yes |  |  | CoMotion master |
| 2262 | Yes |  |  | CoMotion backup |
| 2302 | Unofficial |  |  | ArmA multiplayer |
| 2302 | Unofficial |  |  | Halo: Combat Evolved multiplayer host |
| 2303 | Unofficial |  |  | ArmA multiplayer (default port for game +1) |
| 2303 | Unofficial |  |  | Halo: Combat Evolved multiplayer listener |
| 2305 | Unofficial |  |  | ArmA multiplayer (default port for game +3) |
| 2351 | Unofficial |  |  | AIM game LAN network port |
| 2368 | Unofficial |  |  | Ghost (blogging platform) |
| 2369 | Unofficial |  |  | Default for BMC Control-M/Server Configuration Agent |
| 2370 | Unofficial |  |  | Default for BMC Control-M/Server, to allow the Control-M/Enterprise Manager to connect to the Control-M/Server |
| 2372 | Unofficial |  |  | Default for K9 Web Protection/parental controls, content filtering agent |
| 2375 | Yes | Reserved |  | Docker REST API (plain) |
| 2376 | Yes | Reserved |  | Docker REST API (SSL) |
| 2377 | Yes | Reserved |  | Docker Swarm cluster management communications |
| 2379 | Yes | Reserved |  | CoreOS etcd client communication |
| 2379 | Unofficial |  |  | KGS Go Server |
| 2380 | Yes | Reserved |  | CoreOS etcd server communication |
| 2389 | Assigned |  |  | OpenView Session Mgr |
| 2399 | Yes |  |  | FileMaker Data Access Layer (ODBC/JDBC) |
| 2401 | Yes |  |  | CVS version control system password-based server |
| 2404 | Yes |  |  | IEC 60870-5-104, used to send electric power telecontrol messages between two systems via directly connected data circuits |
| 2424 | Unofficial |  |  | OrientDB database listening for binary client connections |
| 2426 | Unofficial |  |  | VMware VeloCloud Multipath Protocol (VCMP) Dynamic Multipath Optimization (DMPO) |
| 2427 | Yes |  |  | Media Gateway Control Protocol(MGCP) media gateway |
| 2447 | Yes |  |  | ovwdb— OpenView Network Node Manager(NNM) daemon |
| 2456 | Unofficial |  |  | Valheim |
| 2459 | Yes |  |  | XRPL |
| 2480 | Unofficial |  |  | OrientDB database listening for HTTP client connections |
| 2483 | Yes |  |  | Oracle database listening for insecure client connections, replaces port 1521 |
| 2484 | Yes |  |  | Oracle database listening for SSL client connections |
| 2500 | Unofficial |  |  | NetFS communication |
| 2501 | Unofficial |  |  | NetFS probe |
| 2535 | Yes |  |  | Multicast Address Dynamic Client Allocation Protocol(MADCAP). All standard messages are UDP datagrams |
| 2541 | Yes |  |  | LonTalk/IP |
| 2546–2548 | Yes |  |  | EVault data protection services |
| 2593 | Unofficial |  |  | Ultima Online servers |
| 2598 | Unofficial |  |  | Citrix Independent Computing Architecture(ICA) with Session Reliability; port 1494 without session reliability |
| 2599 | Unofficial |  |  | Ultima Online servers |
| 2628 | Yes |  |  | DICT |
| 2638 | Yes |  |  | SQL Anywhere database server |
| 2710 | Unofficial |  |  | XBT Tracker. UDP tracker extension is considered experimental |
| 2727 | Yes |  |  | Media Gateway Control Protocol(MGCP) media gateway controller (call agent) |
| 2759 | Unofficial |  |  | SuperTuxKart server |
| 2761 | Yes |  |  | DICOM over Integrated Secure Communication Layer(ISCL) |
| 2762 | Yes |  |  | DICOM over TLS |
| 2775 | Yes |  |  | Short Message Peer-to-Peer(SMPP) |
| 2809 | Yes |  |  | corbaloc:iiop URL, per the CORBA 3.0.3 specification |
| 2811 | Yes |  |  | gsi ftp, per the GridFTP specification |
| 2827 | Unofficial |  |  | I2P BOB Bridge |
| 2944 | Yes |  |  | Megaco text H.248 |
| 2945 | Yes |  |  | Megaco binary (ASN.1) H.248 |
| 2947 | Yes |  |  | gpsd, GPS daemon |
| 2948–2949 | Yes |  |  | WAP push Multimedia Messaging Service(MMS) |
| 2967 | Yes |  |  | Symantec System Center agent (SSC-AGENT) |
| 2989 | Yes |  |  | Zarkov Intelligent Agent Communication |
| 3000 | Unofficial |  |  | Ruby on Rails development default |
| 3000 | Unofficial |  |  | Bun |
| 3000 | Unofficial |  |  | Meteor development default |
| 3000 | Unofficial |  |  | Resilio Sync, spun from BitTorrent Sync |
| 3000 | Unofficial |  |  | Create React App, script to create single-page React applications |
| 3000 | Unofficial |  |  | Gogs and Gitea(self-hosted Git service) |
| 3000 | Unofficial |  |  | Grafana |
| 3001 | Yes | No |  | Honeywell Prowatch |
| 3004 | Unofficial |  |  | iSync |
| 3010 | Yes |  |  | KWS Connector |
| 3020 | Yes |  |  | Common Internet File System(CIFS). See also port 445 for Server Message Block(SMB), a dialect of CIFS |
| 3050 | Yes |  |  | gds-db (Interbase/ Firebird databases) |
| 3052 | Yes |  |  | APC PowerChute Network |
| 3074 | Yes |  |  | Xbox LIVE and Games for Windows – Live |
| 3101 | Unofficial |  |  | BlackBerry Enterprise Server communication protocol |
| 3128 | Unofficial | No |  | Squid caching web proxy |
| 3225 | Yes |  |  | Fibre Channel over IP(FCIP) |
| 3233 | Yes |  |  | WhiskerControl research control protocol |
| 3260 | Yes |  |  | iSCSI |
| 3268 | Yes |  |  | msft-gc, Microsoft Global Catalog (LDAP service which contains data from Active Directory forests) |
| 3269 | Yes |  |  | msft-gc-ssl, Microsoft Global Catalog over SSL(similar to port 3268, LDAP over SSL) |
| 3283 | Yes |  |  | Net Assistant, a predecessor to Apple Remote Desktop |
| 3283 | Unofficial |  |  | Apple Remote Desktop 2.0 or later |
| 3290 | Unofficial |  |  | Virtual Air Traffic Simulation(VATSIM) network voice communication |
| 3305 | Yes |  |  | Odette File Transfer Protocol(OFTP) |
| 3306 | Yes | Assigned |  | MySQL database system |
| 3323 | Unofficial |  |  | DECE GEODI Server |
| 3332 | Unofficial |  |  | Thundercloud DataPath Overlay Control |
| 3333 | Unofficial |  |  | Eggdrop, an IRC bot default port |
| 3333 | Unofficial |  |  | Network Caller ID server |
| 3333 | Unofficial |  |  | CruiseControl.rb |
| 3333 | Unofficial |  |  | OpenOCD (gdbserver) |
| 3344 | Unofficial |  |  | Repetier-Server |
| 3351 | Unofficial |  |  | Pervasive PSQL |
| 3386 | Yes |  |  | GTP' 3GPP GSM/ UMTS CDR logging protocol |
| 3389 | Yes |  |  | Microsoft Terminal Server(RDP) officially registered as Windows Based Terminal (WBT) |
| 3396 | Yes |  |  | Novell NDPS Printer Agent |
| 3412 | Yes |  |  | xmlBlaster |
| 3423 | Yes |  |  | Xware xTrm Communication Protocol |
| 3424 | Yes |  |  | Xware xTrm Communication Protocol over SSL |
| 3435 | Yes |  |  | Pacom Security User Port |
| 3455 | Yes |  |  | Resource Reservation Protocol(RSVP) |
| 3478 | Yes |  |  | STUN, a protocol for NAT traversal |
| 3478 | Yes |  |  | TURN, a protocol for NAT traversal (extension to STUN) |
| 3478 | Yes |  |  | STUN Behavior Discovery. See also port 5349 |
| 3478–3481 | Unofficial |  |  | Microsoft Teams |
| 3479 | Unofficial |  |  | PlayStation Network |
| 3480 | Unofficial |  |  | PlayStation Network |
| 3483 | Yes |  |  | Slim Devices discovery protocol |
| 3483 | Yes |  |  | Slim Devices SlimProto protocol |
| 3493 | Yes |  |  | Network UPS Tools(NUT) |
| 3503 | Yes |  |  | MPLS LSP-echo Port |
| 3516 | Yes |  |  | Smartcard Port |
| 3527 | Yes |  |  | Microsoft Message Queuing |
| 3535 | Unofficial |  |  | SMTP alternate |
| 3544 | Yes |  |  | Teredo tunneling |
| 3551 | Yes |  |  | Apcupsd Information Port |
| 3601 | Yes |  |  | SAP Message Server Port |
| 3632 | Yes | Assigned |  | Distcc, distributed compiler |
| 3645 | Yes |  |  | Cyc |
| 3655 | Yes |  |  | Advanced Systems Concepts, Inc. ActiveBatch Exec Agent |
| 3659 | Yes |  |  | Apple SASL, used by macOS Server Password Server |
| 3659 | Unofficial |  |  | Battlefield 4 |
| 3667 | Yes |  |  | Information Exchange |
| 3671 | Yes |  |  | KNXnet/IP(EIBnet/IP) |
| 3689 | Yes | Assigned |  | Digital Audio Access Protocol(DAAP), used by Apple's iTunes and AirPlay |
| 3690 | Yes |  |  | Subversion (SVN) version control system |
| 3702 | Yes |  |  | Web Services Dynamic Discovery(WS-Discovery), used by various components of Windows Vista and later |
| 3721 | Unofficial |  |  | ES File Explorer FTP server |
| 3724 | Yes |  |  | Some Blizzard games |
| 3724 | Unofficial |  |  | Club Penguin Disney online game for kids |
| 3725 | Yes |  |  | Netia NA-ER Port |
| 3749 | Yes |  |  | CimTrak registered port |
| 3768 | Yes |  |  | RBLcheckd server daemon |
| 3784 | Yes |  |  | Bidirectional Forwarding Detection (BFD)for IPv4 and IPv6 (Single Hop) (RFC 5881) |
| 3785 | Unofficial |  |  | VoIP program used by Ventrilo |
| 3799 | Yes |  |  | RADIUS change of authorization |
| 3804 | Yes |  |  | Harman Professional HiQnet protocol |
| 3825 | Unofficial |  |  | RedSeal Networks client/server connection |
| 3826 | Yes |  |  | WarMUX game server |
| 3826 | Unofficial |  |  | RedSeal Networks client/server connection |
| 3835 | Unofficial |  |  | RedSeal Networks client/server connection |
| 3830 | Yes |  |  | System Management Agent, developed and used by Cerner to monitor and manage solutions |
| 3856 | Unofficial |  |  | ERP Server Application used by F10 Software |
| 3880 | Yes |  |  | IGRS |
| 3868 | Yes | Yes |  | Diameter base protocol (RFC 3588) |
| 3872 | Yes |  |  | Oracle Enterprise Manager Remote Agent |
| 3900 | Yes |  |  | udt_os, IBM UniData UDT OS |
| 3911 | Yes | Yes |  | prnstatus, Printer Status Port |
| 3960 | Unofficial |  |  | Warframe online interaction |
| 3962 | Unofficial |  |  | Warframe online interaction |
| 3978 | Unofficial |  |  | OpenTTD game (masterserver and content service) |
| 3978 | Unofficial |  |  | Palo Alto Networks' Panorama management of firewalls and log collectors & pre-PAN-OS 8.0 Panorama-to-managed devices software updates |
| 3979 | Unofficial |  |  | OpenTTD game |
| 3999 | Yes |  |  | Norman distributed scanning service |
| 4000 | Unofficial |  |  | Diablo II game |
| 4001 | Unofficial |  |  | Microsoft Ants game |
| 4001 | Unofficial |  |  | CoreOS etcd client communication |
| 4001 | Unofficial |  |  | InterPlanetary File System swarm node |
| 4018 | Yes |  |  | Protocol information and warnings |
| 4035 | Unofficial |  |  | IBM Rational Developer for System z Remote System Explorer Daemon |
| 4045 | Unofficial |  |  | Solaris lockd NFS lock daemon/manager |
| 4050 | Unofficial |  |  | Mud Master Chat protocol (MMCP) – Peer-to-peer communications between MUD clients |
| 4061 | Yes |  |  | Ice Location Service |
| 4069 | Yes |  |  | Minger Email Address Verification Protocol |
| 4070 | Unofficial |  |  | Amazon Echo Dot (Amazon Alexa) streaming connection with Spotify |
| 4089 | Yes |  |  | OpenCORE Remote Control Service |
| 4090 | Yes |  |  | Kerio |
| 4093 | Yes |  |  | PxPlus Client server interface ProvideX |
| 4096 | Yes |  |  | Ascom Timeplex Bridge Relay Element (BRE) |
| 4105 | Yes |  |  | Shofar (ShofarNexus) |
| 4111 | Yes | Assigned |  | Xgrid |
| 4116 | Yes |  |  | Smartcard-TLS |
| 4123 | Assigned | Yes |  | Z-Wave Protocol |
| 4125 | Unofficial |  |  | Microsoft Remote Web Workplace administration |
| 4172 | Yes |  |  | Teradici PCoIP |
| 4190 | Yes |  |  | ManageSieve |
| 4195 | Yes |  |  | AWS protocol for cloud remoting solution |
| 4197 | Yes |  |  | Harman International's HControl protocol for control and monitoring of Audio, Video, Lighting and Control equipment |
| 4198 | Unofficial |  |  | Couch Potato Android app |
| 4200 | Unofficial |  |  | Angular app |
| 4201 | Unofficial |  |  | TinyMUD and various derivatives |
| 4213 | Unofficial |  |  | DuckDB UI default port |
| 4222 | Unofficial |  |  | NATS server default port |
| 4226 | Unofficial |  |  | Aleph One, a computer game |
| 4242 | Unofficial |  |  | Orthanc– DICOM server |
| 4242 | Unofficial |  |  | Quassel distributed IRC client |
| 4243 | Unofficial |  |  | Docker implementations, redistributions, and setups default |
| 4243 | Unofficial |  |  | CrashPlan |
| 4244 | Unofficial |  |  | Viber |
| 4303 | Yes |  |  | Simple Railroad Command Protocol (SRCP) |
| 4307 | Yes |  |  | TrueConf Client – TrueConf Server media data exchange |
| 4321 | Yes |  |  | Referral Whois (RWhois) Protocol |
| 4420 | Yes |  |  | NVM Express over Fabrics storage access |
| 4433 | Unofficial |  |  | SaltoSystems – DTLS Based Communication for NCoder |
| 4444 | Unofficial |  |  | Oracle WebCenter Content: Content Server—Intradoc Socket port. (formerly known as Oracle Universal Content Management) |
| 4444 | Unofficial |  |  | Metasploit's default listener port |
| 4444 | Unofficial |  |  | Xvfb X server virtual frame buffer service |
| 4444 | Unofficial |  |  | OpenOCD (Telnet) |
| 4444–4445 | Unofficial |  |  | I2P HTTP/S proxy |
| 4455 | Unofficial |  |  | OBS Studio built-in WebSocket plugin default port |
| 4460 | Yes | Assigned |  | Network Time Security Key Establishment (NTS) |
| 4486 | Yes |  |  | Integrated Client Message Service (ICMS) |
| 4488 | Yes | Assigned |  | Apple Wide Area Connectivity Service, used by Back to My Mac |
| 4500 | Assigned | Yes |  | IPSec NAT Traversal (RFC 3947, RFC 4306) |
| 4502–4534 | Yes |  |  | Microsoft Silverlight connectable ports under non-elevated trust |
| 4505–4506 | Unofficial |  |  | Salt master |
| 4534 | Unofficial |  |  | Armagetron Advanced server default |
| 4560 | Unofficial |  |  | default Log4j socketappender port |
| 4567 | Unofficial |  |  | Sinatra default server port in development mode (HTTP) |
| 4569 | Yes |  |  | Inter-Asterisk eXchange(IAX2) |
| 4604 | Yes |  |  | Identity Registration Protocol |
| 4605 | Yes |  |  | Direct End to End Secure Chat Protocol |
| 4610–4640 | Unofficial |  |  | QualiSystems TestShell Suite Services |
| 4662 | Yes |  |  | OrbitNet Message Service |
| 4662 | Unofficial |  |  | Default for older versions of eMule |
| 4664 | Unofficial |  |  | Google Desktop Search |
| 4672 | Unofficial |  |  | Default for older versions of eMule |
| 4711 | Unofficial |  |  | eMule optional web interface |
| 4713 | Unofficial |  |  | PulseAudio sound server |
| 4723 | Unofficial |  |  | Appium open source automation tool |
| 4724 | Unofficial |  |  | Default bootstrap port to use on device to talk to Appium |
| 4728 | Yes |  |  | Computer Associates Desktop and Server Management (DMP)/Port Multiplexer |
| 4730 | Yes |  |  | Gearman's job server |
| 4739 | Yes |  |  | IP Flow Information Export |
| 4747 | Unofficial |  |  | Apprentice |
| 4753 | Yes |  |  | SIMON (service and discovery) |
| 4789 | Yes |  |  | Virtual eXtensible Local Area Network (VXLAN) |
| 4791 | Yes |  |  | IP Routable RocE(RoCEv2) |
| 4840 | Yes |  |  | OPC UA Connection Protocol (TCP) and OPC UA Multicast Datagram Protocol (UDP) for OPC Unified Architecture from OPC Foundation |
| 4843 | Yes |  |  | OPC UA TCP Protocol over TLS/SSL for OPC Unified Architecture from OPC Foundation |
| 4847 | Yes |  |  | Web Fresh Communication, Quadrion Software & Odorless Entertainment |
| 4848 | Unofficial |  |  | Java GlassFish Application Server administration default |
| 4894 | Yes |  |  | LysKOM Protocol A |
| 4900 | Unofficial |  |  | HFSQL (Hyperfile SQL) Mantra Server from PC SOFT |
| 4944 | No | Unofficial |  | DrayTek DSL Status Monitoring |
| 4949 | Yes |  |  | Munin Resource Monitoring Tool |
| 4950 | Yes |  |  | Cylon Controls UC32 Communications Port |
| 5000 | Unofficial |  |  | UPnP—Windows network device interoperability |
| 5000 | Unofficial |  |  | VTun, VPN Software |
| 5000 | Unofficial |  |  | ASP.NET Core— Development Webserver |
| 5000 | Unofficial |  |  | FlightGear multiplayer |
| 5000 | Unofficial |  |  | Synology Inc. Management Console, File Station, Audio Station |
| 5000 | Unofficial |  |  | Flask Development Webserver |
| 5000 | Unofficial |  |  | Heroku console access |
| 5000 | Unofficial |  |  | Docker Registry |
| 5000 | Unofficial |  |  | AT&T U-verse public, educational, and government access(PEG) streaming over HTTP |
| 5000 | Unofficial |  |  | High-Speed SECS Message Services |
| 5000 | Unofficial |  |  | 3CX Phone System Management Console/Web Client (HTTP) |
| 5000 | Unofficial |  |  | RidgeRun GStreamer Daemon (GSTD) |
| 5000 | Unofficial |  |  | Apple's AirPlay Receiver |
| 5000 | Unofficial |  |  | AWS Elastic Beanstalk Proxy server |
| 5000–5500 | No | Unofficial |  | League of Legends, a multiplayer online battle arena video game |
| 5001 | Unofficial |  |  | Slingbox and Slingplayer |
| 5001 | Unofficial |  |  | Iperf(Tool for measuring TCP and UDP bandwidth performance) |
| 5001 | Unofficial |  |  | Synology Inc. Secured Management Console, File Station, Audio Station |
| 5001 | Unofficial |  |  | 3CX Phone System Management Console/Web Client (HTTPS) |
| 5001 | Unofficial |  |  | InterPlanetary File System RPC API |
| 5002 | Unofficial |  |  | ASSA ARX access control system |
| 5003 | Yes | Assigned |  | FileMaker– name binding and transport |
| 5004 | Yes | Yes |  | Real-time Transport Protocol media data (RTP) (RFC 3551, RFC 4571) |
| 5005 | Yes | Yes |  | Real-time Transport Protocol control protocol(RTCP) (RFC 3551, RFC 4571) |
| 5007 | Unofficial |  |  | Palo Alto Networks – User-ID agent |
| 5010 | Yes |  |  | Registered to: TelePath (the IBM FlowMark workflow-management system messaging platform)The TCP port is now used for: IBM WebSphere MQ Workflow |
| 5011 | Yes |  |  | TelePath (the IBM FlowMark workflow-management system messaging platform) |
| 5022 | Unofficial |  |  | MSSQL Server Replication and Database mirroring endpoints |
| 5025 | Yes |  |  | scpi-raw Standard Commands for Programmable Instruments |
| 5029 | Unofficial |  |  | Sonic Robo Blast 2 and Sonic Robo Blast 2 Kart servers |
| 5031 | Unofficial |  |  | AVM CAPI-over-TCP (ISDN over Ethernet tunneling) |
| 5037 | Unofficial |  |  | Android ADB server |
| 5044 | Yes |  |  | Standard port in Filebeats/Logstash implementation of Lumberjack protocol |
| 5048 | Yes |  |  | Texai Message Service |
| 5050 | Unofficial |  |  | Yahoo! Messenger |
| 5051 | Yes |  |  | ita-agent Symantec Intruder Alert |
| 5060 | Yes |  |  | Session Initiation Protocol(SIP) |
| 5061 | Yes |  |  | Session Initiation Protocol(SIP) over TLS |
| 5062 | Yes |  |  | Localisation access |
| 5064 | Yes |  |  | EPICS Channel Access server |
| 5065 | Assigned | Yes |  | EPICS Channel Access repeater beacon |
| 5070 | Unofficial | No |  | Binary Floor Control Protocol(BFCP) |
| 5075 | Yes | No |  | EPICS PV Access Data |
| 5076 | No | Yes |  | EPICS PV Access Searches |
| 5080 | Unofficial |  |  | NEC Phone System SV8100 and SV9100 MLC phones: default iSIP port |
| 5084 | Yes |  |  | EPCglobal Low Level Reader Protocol (LLRP) |
| 5085 | Yes |  |  | EPCglobal Low Level Reader Protocol (LLRP) over TLS |
| 5090 | Unofficial |  |  | 3CX Phone System 3CX Tunnel Protocol, 3CX App API, 3CX Session Border Controller |
| 5093 | Yes |  |  | Thales Sentinel (was SafeNet, Gemalto), Sentinel LM / Sentinel RMS, client-to-server |
| 5099 | Yes |  |  | Thales Sentinel (was SafeNet, Gemalto), Sentinel LM / Sentinel RMS, server-to-server |
| 5104 | Unofficial |  |  | IBM Tivoli Framework NetCOOL/Impact HTTP Service |
| 5121 | Unofficial |  |  | Neverwinter Nights |
| 5150 | Yes |  |  | ATMP Ascend Tunnel Management Protocol |
| 5151 | Yes |  |  | ESRI SDE Instance |
| 5151 | Yes |  |  | ESRI SDE Remote Start |
| 5154 | Yes |  |  | BZFlag |
| 5172 | Yes |  |  | PC over IP Endpoint Management |
| 5173 | Unofficial |  |  | Vite |
| 5190 | Yes |  |  | AOL Instant Messenger protocol. The chat app is defunct as of 15 December 2017 |
| 5198 | Unofficial |  |  | EchoLink VoIP Amateur Radio Software (Voice) |
| 5199 | Unofficial |  |  | EchoLink VoIP Amateur Radio Software (Voice) |
| 5200 | Unofficial |  |  | EchoLink VoIP Amateur Radio Software (Information) |
| 5201 | Unofficial |  |  | Iperf3(Tool for measuring TCP and UDP bandwidth performance) |
| 5222 | Yes | Reserved |  | Extensible Messaging and Presence Protocol(XMPP) client connection |
| 5223 | Unofficial |  |  | Apple Push Notification Service |
| 5223 | Unofficial |  |  | Extensible Messaging and Presence Protocol (XMPP) client connection over SSL |
| 5228 | Yes |  |  | HP Virtual Room Service |
| 5228 | Unofficial |  |  | Google Play, Android Cloud to Device Messaging Service, Google Cloud Messaging |
| 5231 | Yes |  |  | Remote Control of Scan Software for Cruse Scanners |
| 5232 | Yes |  |  | Cruse Scanning System Service |
| 5232 | Unofficial |  |  | Silicon Graphics Distributed Graphics Library daemon (dgld) |
| 5235–5236 | Unofficial |  |  | Firebase Cloud Messaging |
| 5242 | Unofficial |  |  | Viber |
| 5243 | Unofficial |  |  | Viber |
| 5246 | Yes |  |  | Control And Provisioning of Wireless Access Points (CAPWAP) CAPWAP control |
| 5247 | Yes |  |  | Control And Provisioning of Wireless Access Points (CAPWAP) CAPWAP data |
| 5269 | Yes |  |  | Extensible Messaging and Presence Protocol (XMPP) server-to-server connection |
| 5280 | Yes |  |  | Extensible Messaging and Presence Protocol (XMPP) |
| 5281 | Unofficial |  |  | Extensible Messaging and Presence Protocol (XMPP) |
| 5298 | Yes |  |  | Extensible Messaging and Presence Protocol (XMPP) |
| 5310 | Assigned | Yes |  | Outlaws, a 1997 first-person shooter video game |
| 5318 | Yes | Reserved |  | Certificate Management over CMS |
| 5349 | Yes |  |  | STUN over TLS/ DTLS, a protocol for NAT traversal |
| 5349 | Yes |  |  | TURN over TLS/DTLS, a protocol for NAT traversal |
| 5349 | Yes | Reserved |  | STUN Behavior Discovery over TLS. See also port 3478 |
| 5351 | Reserved | Yes |  | NAT Port Mapping Protocol and Port Control Protocol—client-requested configuration for connections through network address translators and firewalls |
| 5353 | Assigned | Yes |  | Multicast DNS(mDNS) |
| 5355 | Yes |  |  | Link-Local Multicast Name Resolution(LLMNR), allows hosts to perform name resolution for hosts on the same local link(only provided by Windows Vista and Server 2008) |
| 5357 | Unofficial |  |  | Web Services for Devices(WSDAPI) (starting from Windows Vista, Windows 7 and Server 2008) |
| 5358 | Unofficial |  |  | WSDAPI Applications to Use a Secure Channel (only provided by Windows Vista, Windows 7 and Server 2008) |
| 5394 | Unofficial |  |  | Kega Fusion, a Sega multi-console emulator |
| 5402 | Yes |  |  | Multicast File Transfer Protocol(MFTP) |
| 5405 | Yes |  |  | NetSupport Manager |
| 5412 | Yes |  |  | IBM Rational Synergy (Telelogic Synergy) (Continuus CM) Message Router |
| 5413 | Yes |  |  | Wonderware SuiteLink service |
| 5417 | Yes |  |  | SNS Agent |
| 5421 | Yes |  |  | NetSupport Manager |
| 5432 | Yes | Assigned |  | PostgreSQL database system |
| 5433 | Unofficial |  |  | Bouwsoft file/webserver |
| 5445 | Unofficial |  |  | Cisco Unified Video Advantage |
| 5450 | Unofficial |  |  | OSIsoft PI Server Client Access |
| 5457 | Unofficial |  |  | OSIsoft PI Asset Framework Client Access |
| 5458 | Unofficial |  |  | OSIsoft PI Notifications Client Access |
| 5480 | Unofficial |  |  | VMware VAMI (Virtual Appliance Management Infrastructure) — used for initial setup of various administration settings on Virtual Appliances designed using the VAMI architecture |
| 5481 | Unofficial |  |  | Schneider Electric's ClearSCADA (SCADA implementation for Windows) — used for client-to-server communication |
| 5495 | Unofficial |  |  | IBM Cognos TM1 Admin server |
| 5498 | Unofficial |  |  | Hotline tracker server connection |
| 5499 | Unofficial |  |  | Hotline tracker server discovery |
| 5500 | Unofficial |  |  | Hotline control connection |
| 5500 | Unofficial |  |  | VNC Remote Framebuffer (RFB) protocol— for incoming listening viewer |
| 5501 | Unofficial |  |  | Hotline file transfer connection |
| 5517 | Unofficial |  |  | Setiqueue Proxy server client for SETI@Home project |
| 5520 | Unofficial |  |  | Hytale multiplayer server |
| 5550 | Unofficial |  |  | Hewlett-Packard Data Protector |
| 5554 | Unofficial |  |  | Fastboot default wireless port |
| 5555 | Unofficial |  |  | Oracle WebCenter Content: Inbound Refinery—Intradoc Socket port. (formerly known as Oracle Universal Content Management). Port though often changed during installation |
| 5555 | Unofficial |  |  | Freeciv versions up to 2.0, Hewlett-Packard Data Protector, McAfee EndPoint Encryption Database Server, SAP, Default for Microsoft Dynamics CRM 4.0, Softether VPN default port |
| 5555 | Unofficial |  |  | Wireless adb(Android Debug Bridge) control of an Android device over the network |
| 5556 | Yes |  |  | Freeciv, Oracle WebLogic Server Node Manager |
| 5568 | Yes |  |  | Session Data Transport (SDT), a part of Architecture for Control Networks(ACN) |
| 5601 | Unofficial |  |  | Kibana |
| 5631 | Yes |  |  | pcANYWHEREdata, Symantec pcAnywhere(version 7.52 and later) data |
| 5632 | Yes |  |  | pcANYWHEREstat, Symantec pcAnywhere (version 7.52 and later) status |
| 5656 | Unofficial |  |  | IBM Lotus Sametime p2p file transfer |
| 5666 | Unofficial |  |  | NRPE(Nagios) |
| 5667 | Unofficial |  |  | NSCA (Nagios) |
| 5670 | Yes |  |  | FILEMQ ZeroMQ File Message Queuing Protocol |
| 5670 | Yes |  |  | ZRE-DISC ZeroMQ Realtime Exchange Protocol (Discovery) |
| 5671 | Yes | Assigned |  | Advanced Message Queuing Protocol(AMQP) over TLS |
| 5672 | Yes | Assigned |  | Advanced Message Queuing Protocol (AMQP) |
| 5678 | Unofficial | No |  | n8n |
| 5678 | No | Yes |  | MikroTik Neighbor Discovery Protocol |
| 5683 | Yes |  |  | Constrained Application Protocol(CoAP) |
| 5684 | Yes |  |  | Constrained Application Protocol Secure (CoAPs) |
| 5693 | Unofficial |  |  | Nagios Cross Platform Agent (NCPA) |
| 5701 | Unofficial |  |  | Hazelcast default communication port |
| 5718 | Unofficial |  |  | Microsoft DPM Data Channel (with the agent coordinator) |
| 5719 | Unofficial |  |  | Microsoft DPM Data Channel (with the protection agent) |
| 5722 | Yes |  |  | Microsoft RPC, DFSR (SYSVOL) Replication Service |
| 5723 | Unofficial |  |  | System Center Operations Manager |
| 5724 | Unofficial |  |  | Operations Manager Console |
| 5741 | Yes |  |  | IDA Discover Port 1 |
| 5742 | Yes |  |  | IDA Discover Port 2 |
| 5800 | Unofficial |  |  | VNC Remote Framebuffer (RFB) protocol over HTTP |
| 5800 | Unofficial |  |  | ProjectWise Server |
| 5900 | Yes |  |  | Remote Framebuffer (RFB) protocol |
| 5900 | Unofficial |  |  | VNC Remote Framebuffer (RFB) protocol |
| 5905 | Unofficial |  |  | Windows service "C:\Program Files\Intel\Intel(R) Online Connect Access\IntelTechnologyAccessService.exe" that listens on 127.0.0.1 |
| 5931 | Yes |  |  | AMMYY admin Remote Control |
| 5938 | Unofficial |  |  | TeamViewer remote desktop protocol |
| 5984 | Yes |  |  | CouchDB database server |
| 5985 | Yes |  |  | Windows PowerShell Default psSession Port Windows Remote Management Service(WinRM-HTTP) |
| 5986 | Yes |  |  | Windows PowerShell Default psSession Port Windows Remote Management Service(WinRM-HTTPS) |
| 5988–5989 | Yes |  |  | CIM-XML (DMTF Protocol) |
| 6000–6063 | Yes |  |  | X11—used between an X client and server over the network |
| 6005 | Unofficial |  |  | Default for BMC Software Control-M/Server—Socket used for communication between Control-M processes—though often changed during installation |
| 6005 | Unofficial |  |  | Default for Camfrog chat & cam client |
| 6009 | Unofficial |  |  | JD Edwards EnterpriseOne ERP system JDENet messaging client listener |
| 6024–6025 | Unofficial |  |  | Tigermeeting Android client discovery |
| 6026 | Unofficial |  |  | Tigermeeting client/server communication |
| 6030–6031 | Unofficial |  |  | Tigermeeting Admin user discovery |
| 6032 | Unofficial |  |  | Tigermeeting API for cloud management – TigerDriver |
| 6050 | Unofficial |  |  | Arcserve backup |
| 6051 | Unofficial |  |  | Arcserve backup |
| 6081 | Yes |  |  | Generic Network Virtualization Encapsulation(Geneve) |
| 6086 | Yes |  |  | Peer Distributed Transfer Protocol(PDTP), FTP like file server in a P2P network |
| 6100 | Unofficial |  |  | Vizrt System |
| 6100 | Unofficial |  |  | Ventrilo authentication for version 3 |
| 6101 | Unofficial |  |  | Backup Exec Agent Browser |
| 6110 | Yes |  |  | softcm, HP Softbench CM |
| 6111 | Yes |  |  | spc, HP Softbench Sub-Process Control |
| 6112 | Yes |  |  | dtspcd, execute commands and launch applications remotely |
| 6112 | Unofficial |  |  | Blizzard's Battle.net gaming service and some games, ArenaNet gaming service, Relic gaming service |
| 6112 | Unofficial |  |  | Club Penguin Disney online game for kids |
| 6113 | Unofficial |  |  | Club Penguin Disney online game for kids, Used by some Blizzard games |
| 6121–6122 | Unofficial |  |  | Lacewing networking extensions used in Clickteam Fusion |
| 6136 | Unofficial |  |  | ObjectDB database server |
| 6159 | Yes |  |  | ARINC 840 EFB Application Control Interface |
| 6160 | Unofficial |  |  | Veeam Installer Service |
| 6161 | Unofficial |  |  | Veeam vPower NFS Service |
| 6162 | Unofficial |  |  | Veeam Data Mover |
| 6163 | Unofficial |  |  | Veeam Hyper-V Integration Service |
| 6164 | Unofficial |  |  | Veeam WAN Accelerator |
| 6165 | Unofficial |  |  | Veeam WAN Accelerator Data Transfer |
| 6167 | Unofficial |  |  | Veeam Log Shipping Service |
| 6170 | Unofficial |  |  | Veeam Mount Server |
| 6200 | Unofficial |  |  | Oracle WebCenter Content Portable: Content Server (With Native UI) and Inbound Refinery |
| 6201 | Assigned |  |  | Thermo-Calc Software AB: Management of service nodes in a processing grid for thermodynamic calculations |
| 6201 | Unofficial |  |  | Oracle WebCenter Content Portable: Admin |
| 6225 | Unofficial |  |  | Oracle WebCenter Content Portable: Content Server Web UI |
| 6227 | Unofficial |  |  | Oracle WebCenter Content Portable: JavaDB |
| 6240 | Unofficial |  |  | Oracle WebCenter Content Portable: Capture |
| 6244 | Unofficial |  |  | Oracle WebCenter Content Portable: Content Server—Intradoc Socket port |
| 6255 | Unofficial |  |  | Oracle WebCenter Content Portable: Inbound Refinery—Intradoc Socket port |
| 6257 | Unofficial |  |  | WinMX(see also 6699) |
| 6260 | Unofficial |  |  | planet M.U.L.E |
| 6262 | Unofficial |  |  | Sybase Advantage Database Server |
| 6343 | Yes |  |  | SFlow, sFlow traffic monitoring |
| 6346 | Yes |  |  | gnutella-svc, gnutella (FrostWire, Limewire, Shareaza, etc.) |
| 6347 | Yes |  |  | gnutella-rtr, Gnutella alternate |
| 6350 | Yes |  |  | App Discovery and Access Protocol |
| 6379 | Yes |  |  | Redis key-value data store |
| 6389 | Unofficial |  |  | EMC CLARiiON |
| 6432 | Yes |  |  | PgBouncer—A connection pooler for PostgreSQL |
| 6436 | Unofficial |  |  | Leap Motion Websocket Server TLS |
| 6437 | Unofficial |  |  | Leap Motion Websocket Server |
| 6443 | Unofficial |  |  | Kubernetes API server |
| 6444 | Yes |  |  | Sun Grid Engine Qmaster Service |
| 6445 | Yes |  |  | Sun Grid Engine Execution Service |
| 6454 | Unofficial |  |  | Art-Net protocol |
| 6463–6472 | Unofficial |  |  | Discord RPC |
| 6464 | Yes |  |  | Port assignment for medical device communication in accordance to IEEE 11073-20701 |
| 6513 | Yes |  |  | NETCONF over TLS |
| 6514 | Yes |  |  | Syslog over TLS |
| 6515 | Yes |  |  | Elipse RPC Protocol (REC) |
| 6516 | Unofficial |  |  | Windows Admin Center |
| 6543 | Unofficial |  |  | Pylons project#Pyramid Default Pylons Pyramid web service port |
| 6556 | Unofficial |  |  | Check MK Agent |
| 6566 | Yes |  |  | SANE(Scanner Access Now Easy)—SANE network scanner daemon |
| 6560–6561 | Unofficial |  |  | Speech-Dispatcher daemon |
| 6567 | Unofficial |  |  | Mindustry multiplayer server |
| 6571 | Unofficial |  |  | Windows Live FolderShare client |
| 6600 | Yes |  |  | Microsoft Hyper-V Live |
| 6600 | Unofficial |  |  | Music Player Daemon(MPD) |
| 6601 | Yes |  |  | Microsoft Forefront Threat Management Gateway |
| 6602 | Yes |  |  | Microsoft Windows WSS Communication |
| 6610 | Yes |  |  | Bencher API |
| 6619 | Yes |  |  | odette-ftps, Odette File Transfer Protocol(OFTP) over TLS/ SSL |
| 6622 | Yes |  |  | Multicast FTP |
| 6626 | Yes |  |  | Semaphore Messenger |
| 6653 | Yes | Assigned |  | OpenFlow |
| 6660–6664 | Unofficial |  |  | Internet Relay Chat(IRC) |
| 6665–6669 | Yes |  |  | Internet Relay Chat (IRC) |
| 6679 | Yes |  |  | Osorno Automation Protocol (OSAUT) |
| 6679 | Unofficial |  |  | Internet Relay Chat (IRC) SSL(Secure Internet Relay Chat)—often used |
| 6690 | Unofficial |  |  | Synology Cloud station |
| 6697 | Yes |  |  | IRC SSL (Secure Internet Relay Chat)—often used |
| 6699 | Unofficial |  |  | WinMX(see also 6257) |
| 6715 | Unofficial |  |  | AberMUD and derivatives default port |
| 6771 | Unofficial |  |  | BitTorrent Local Peer Discovery |
| 6783–6785 | Unofficial |  |  | Splashtop Remote server broadcast |
| 6789 | Unofficial |  |  | Ubiquiti UniFi Network server mobile speed test |
| 6801 | Yes |  |  | ACNET Control System Protocol |
| 6881–6887 | Unofficial |  |  | BitTorrent beginning of range of ports used most often |
| 6888 | Yes |  |  | MUSE |
| 6888 | Unofficial |  |  | BitTorrent continuation of range of ports used most often |
| 6889–6900 | Unofficial |  |  | BitTorrent continuation of range of ports used most often |
| 6891–6900 | Unofficial |  |  | Windows Live Messenger(File transfer) |
| 6901 | Unofficial |  |  | Windows Live Messenger (Voice) |
| 6901 | Unofficial |  |  | BitTorrent continuation of range of ports used most often |
| 6902–6968 | Unofficial |  |  | BitTorrent continuation of range of ports used most often |
| 6924 | Yes |  |  | split-ping, ping with RX/TX latency/loss split |
| 6935 | Yes |  |  | EthoScan Service |
| 6936 | Yes |  |  | XenSource Management Service |
| 6969 | Yes |  |  | acmsoda |
| 6969 | Unofficial |  |  | BitTorrent tracker |
| 6970–6999 | Unofficial |  |  | BitTorrent end of range of ports used most often |
| 6970–6999 | Unofficial |  |  | QuickTime Streaming Server |
| 6980 | Unofficial |  |  | Voicemeeter VBAN network audio protocol |
| 7000 | Unofficial |  |  | Default for Vuze's built-in HTTPS Bittorrent tracker |
| 7000 | Unofficial |  |  | Avira Server Management Console |
| 7000 | Unofficial |  |  | Default for MAGICS remote license server |
| 7000 | Yes |  |  | IRC SSL (Secure Internet Relay Chat)—often used |
| 7001 | Unofficial |  |  | Avira Server Management Console |
| 7001 | Unofficial |  |  | Default for BEA WebLogic Server's HTTP server, though often changed during installation |
| 7001 | Unofficial |  |  | Default for Network Optix as well as their whilelabel branded systems, providing service both on http and deployed client for video surveillance system |
| 7002 | Unofficial |  |  | Default for BEA WebLogic Server's HTTPS server, though often changed during installation |
| 7005 | Unofficial |  |  | Default for BMC Software Control-M/Server and Control-M/Agent for Agent-to-Server, though often changed during installation |
| 7006 | Unofficial |  |  | Default for BMC Software Control-M/Server and Control-M/Agent for Server-to-Agent, though often changed during installation |
| 7010 | Unofficial |  |  | Default for Cisco AON AMC (AON Management Console) |
| 7010 | Unofficial |  |  | Default for MAGICS remote license server |
| 7022 | Unofficial |  |  | MSSQL Server Replication and Database mirroring endpoints |
| 7023 | Yes |  |  | T2-NMCS Protocol for SatCom Modems |
| 7025 | Unofficial |  |  | Zimbra LMTP [mailbox]—local mail delivery |
| 7047 | Unofficial |  |  | Zimbra conversion server |
| 7070 | Unofficial |  |  | Real Time Streaming Protocol(RTSP), used by QuickTime Streaming Server. TCP is used by default, UDP is used as an alternate |
| 7077 | Yes |  |  | Development-Network Authentification-Protocol |
| 7133 | Unofficial |  |  | Enemy Territory: Quake Wars |
| 7144 | Unofficial |  |  | Peercast |
| 7145 | Unofficial |  |  | Peercast |
| 7171 | Unofficial |  |  | Tibia |
| 7262 | Yes |  |  | CNAP (Calypso Network Access Protocol) |
| 7272 | Yes |  |  | WatchMe – WatchMe Monitoring |
| 7306 | Unofficial |  |  | Zimbra mysql [mailbox] |
| 7307 | Unofficial |  |  | Zimbra mysql [logger] |
| 7312 | Unofficial |  |  | Sibelius License Server |
| 7396 | Unofficial |  |  | Web control interface for Folding@home v7.3.6 and later |
| 7400 | Yes |  |  | RTPS (Real Time Publish Subscribe) DDS Discovery |
| 7401 | Yes |  |  | RTPS (Real Time Publish Subscribe) DDS User-Traffic |
| 7402 | Yes |  |  | RTPS (Real Time Publish Subscribe) DDS Meta-Traffic |
| 7471 | Unofficial |  |  | Stateless Transport Tunneling (STT) |
| 7473 | Yes |  |  | Rise: The Vieneo Province |
| 7474 | Yes |  |  | Neo4J Server webadmin |
| 7478 | Yes |  |  | Default port used by Open iT Server |
| 7542 | Yes |  |  | Saratoga file transfer protocol |
| 7547 | Yes |  |  | CPE WAN Management Protocol (CWMP) Technical Report 069 |
| 7575 | Unofficial |  |  | Populous: The Beginning server |
| 7624 | Yes |  |  | Instrument Neutral Distributed Interface |
| 7631 | Yes |  |  | ERLPhase |
| 7634 | Unofficial |  |  | hddtemp—Utility to monitor hard drive temperature |
| 7652–7654 | Unofficial |  |  | I2P anonymizing overlay network |
| 7655 | Unofficial |  |  | I2P SAM Bridge Socket API |
| 7656–7660 | Unofficial |  |  | I2P anonymizing overlay network |
| 7659 | Unofficial |  |  | Polypheny User Interface (database system) |
| 7670 | Unofficial |  |  | BrettspielWelt BSW Boardgame Portal |
| 7680 | Unofficial |  |  | Delivery Optimization for Windows 10 |
| 7687 | Yes |  |  | Bolt database connection |
| 7707–7708 | Unofficial |  |  | Killing Floor |
| 7717 | Unofficial |  |  | Killing Floor |
| 7745 | Unofficial |  |  | HomeBox |
| 7777 | Unofficial |  |  | iChat server file transfer proxy |
| 7777 | Unofficial |  |  | Oracle Cluster File System 2 |
| 7777 | Unofficial |  |  | Windows backdoor program tini.exe default |
| 7777 | Unofficial |  |  | Just Cause 2: Multiplayer Mod Server |
| 7777 | Unofficial |  |  | Terraria default server |
| 7777 | Unofficial | Unofficial |  | Super Foosball multiplayer gameplay port |
| 7777 | Unofficial |  |  | San Andreas Multiplayer (SA-MP) default port server |
| 7777 | Unofficial |  |  | SCP: Secret Laboratory Multiplayer Server |
| 7777–7788 | Yes |  |  | Steam common default game server ports (Ark, L4D2, etc.) |
| 7777–7788 | Unofficial |  |  | Unreal Tournament series default server |
| 7831 | Unofficial |  |  | Default used by Smartlaunch Internet Cafe Administration software |
| 7880 | Yes |  |  | PowerSchool Gradebook Server |
| 7890 | Unofficial |  |  | Default that will be used by the iControl Internet Cafe Suite Administration software |
| 7915 | Unofficial |  |  | Default for YSFlight server |
| 7935 | Unofficial |  |  | Fixed port used for Adobe Flash Debug Player to communicate with a debugger (Flash IDE, Flex Builder or fdb) |
| 7946 | Unofficial |  |  | Docker Swarm communication among nodes |
| 7979 | Unofficial |  |  | Used by SilverBluff Studios for communication between servers and clients |
| 7990 | Unofficial |  |  | Atlassian Bitbucket(default port) |
| 8000 | Unofficial |  |  | Deno |
| 8000 | Unofficial |  |  | Commonly used for Internet radio streams such as SHOUTcast, Icecast and iTunes Radio |
| 8000 | Unofficial |  |  | DynamoDB Local |
| 8000 | Unofficial |  |  | Django Development Webserver |
| 8000 | Unofficial |  |  | Python 3 http.server |
| 8005 | Unofficial |  |  | Tomcat remote shutdown |
| 8005 | Unofficial |  |  | PLATO ASCII protocol (RFC 600) |
| 8005 | Unofficial |  |  | Windows SCCM HTTP listener service |
| 8006 | Unofficial |  |  | Quest AppAssure 5 API |
| 8006 | Unofficial | No |  | Proxmox Virtual Environment admin web interface |
| 8007 | Unofficial |  |  | Quest AppAssure 5 Engine |
| 8007 | Yes |  |  | Proxmox Backup Server admin web interface |
| 8008 | Unofficial |  |  | Alternative port for HTTP. See also ports 80 and 8080 |
| 8008 | Unofficial |  |  | IBM HTTP Server administration default |
| 8008 | Unofficial |  |  | iCal, a calendar application by Apple |
| 8008 | Unofficial | No |  | Matrix homeserver federation over HTTP |
| 8009 | Unofficial |  |  | Apache JServ Protocol(`ajp13`) |
| 8010 | Unofficial | No |  | Buildbot web status page |
| 8042 | Unofficial |  |  | Orthanc– REST API over HTTP |
| 8061 | Yes | Reserved |  | Nikatron Device Protocol (nikatron-dev) |
| 8069 | Unofficial |  |  | OpenERP 5.0 XML-RPC protocol |
| 8070 | Unofficial |  |  | OpenERP 5.0 NET-RPC protocol |
| 8074 | Yes |  |  | Gadu-Gadu |
| 8075 | Unofficial |  |  | Killing Floor web administration interface |
| 8080 | Yes |  |  | Alternative port for HTTP. See also ports 80 and 8008 |
| 8080 | Unofficial |  |  | Apache Tomcat |
| 8080 | Unofficial |  |  | Atlassian JIRA applications |
| 8081 | Yes |  |  | Sun Proxy Admin Service |
| 8088 | Unofficial |  |  | Asterisk management access via HTTP |
| 8088 | Unofficial |  |  | YARN ResourceManager Web UI |
| 8089 | Unofficial | No |  | Splunk daemon management |
| 8089 | Unofficial |  |  | Fritz!Box automatic TR-069 configuration |
| 8090 | Unofficial |  |  | Atlassian Confluence |
| 8090 | Unofficial |  |  | Coral Content Distribution Network (legacy; 80 and 8080 now supported) |
| 8090 | Unofficial |  |  | Matrix identity server |
| 8091 | Unofficial |  |  | CouchBase web administration |
| 8092 | Unofficial |  |  | CouchBase API |
| 8093 | Unofficial |  |  | GitLab Runner session server |
| 8096 | Unofficial |  |  | Emby and Jellyfin HTTP port |
| 8100 | Unofficial |  |  | SaltoSystems – Pro Access Space Service |
| 8100 | Unofficial |  |  | BlueMap, a 3D Minecraft web viewer and mapping tool |
| 8102 | Unofficial |  |  | SaltoSystems – Used for LocalIO-Bridge for USB-Devices |
| 8111 | Unofficial |  |  | JOSM Remote Control |
| 8112 | Unofficial |  |  | PAC Pacifica Coin |
| 8116 | Unofficial |  |  | Check Point Cluster Control Protocol |
| 8118 | Yes |  |  | Privoxy—advertisement-filtering Web proxy |
| 8123 | Unofficial |  |  | Polipo Web proxy |
| 8123 | Unofficial |  |  | Home Assistant Home automation |
| 8123 | Unofficial |  |  | Minecraft Dynmap plugin/mod |
| 8125 | Unofficial |  |  | StatsD server |
| 8139 | Unofficial |  |  | Puppet (software) Client agent |
| 8140 | Yes |  |  | Puppet (software) Master server |
| 8172 | Unofficial |  |  | Microsoft Remote Administration for IIS Manager |
| 8181–8186 | Unofficial |  |  | FRITZ!Box services |
| 8182 | Unofficial |  |  | NexusM Media Server HTTP port |
| 8184 | Unofficial |  |  | NCSA Brown Dog Data Access Proxy |
| 8188 | Unofficial |  |  | ComfyUI Web Interface |
| 8194–8195 | Yes |  |  | Bloomberg Terminal |
| 8200 | Unofficial |  |  | GoToMyPC |
| 8200 | Unofficial |  |  | MiniDLNA media server Web Interface |
| 8200 | Unofficial |  |  | Elastic APM Server |
| 8222 | Unofficial |  |  | VMware VI Web Access via HTTP |
| 8236 | Unofficial |  |  | jRCS listener for Rocket Software jBASE Remote Connectivity Server |
| 8243 | Yes |  |  | HTTPS listener for Apache Synapse |
| 8245 | Unofficial |  |  | Dynamic DNS for at least No-IP and DynDNS |
| 8280 | Yes |  |  | HTTP listener for Apache Synapse |
| 8281 | Unofficial |  |  | HTTP Listener for Gatecraft Plugin |
| 8291 | Unofficial |  |  | WinBox: Mikrotik RouterOS GUI Configurator |
| 8303 | Unofficial |  |  | Teeworlds Server |
| 8322 | Assigned |  |  | Garmin Marine |
| 8332 | Unofficial |  |  | Bitcoin JSON-RPC server |
| 8333 | Unofficial |  |  | Bitcoin |
| 8333 | Unofficial |  |  | VMware VI Web Access via HTTPS |
| 8334 | Unofficial |  |  | Filestash server (default) |
| 8335 | Unofficial |  |  | DBCalm Open |
| 8337 | Unofficial |  |  | VisualSVN Distributed File System Service (VDFS) |
| 8384 | Unofficial |  |  | Syncthing web GUI |
| 8388 | Unofficial |  |  | Shadowsocks proxy server |
| 8400 | Yes |  |  | Commvault Communications Service (GxCVD, found in all client computers) |
| 8401 | Yes |  |  | Commvault Server Event Manager (GxEvMgrS, available in CommServe) |
| 8403 | Yes |  |  | Commvault Firewall (GxFWD, tunnel port for HTTP/HTTPS) |
| 8443 | Unofficial |  |  | SW Soft Plesk Control Panel |
| 8443 | Unofficial |  |  | Apache Tomcat SSL |
| 8443 | Unofficial |  |  | Promise WebPAM SSL |
| 8443 | Unofficial |  |  | iCal over SSL |
| 8443 | Unofficial |  |  | MineOs WebUi |
| 8444 | Unofficial |  |  | Bitmessage |
| 8444 | Unofficial |  |  | Chia |
| 8448 | Yes |  |  | Matrix homeserver federation over HTTPS |
| 8484 | Unofficial |  |  | MapleStory Login Server |
| 8500 | Unofficial |  |  | Adobe ColdFusion built-in web server |
| 8501 | Unofficial |  |  | Streamlit Open-source Python framework for machine learning and data science |
| 8530 | Unofficial |  |  | Windows Server Update Services over HTTP, when using the default role installation settings in Windows Server 2012 and later versions |
| 8531 | Unofficial |  |  | Windows Server Update Services over HTTPS, when using the default role installation settings in Windows Server 2012 and later versions |
| 8555 | Unofficial |  |  | Symantec DLP OCR Engine |
| 8555 | Unofficial |  |  | Chia JSON-RPC server |
| 8580 | Unofficial |  |  | Freegate, an Internet anonymizer and proxy tool |
| 8601 | Unofficial |  |  | Wavestore VMS protocol |
| 8611–8614 | Yes |  |  | Canon BubbleJet Network Protocol |
| 8629 | Unofficial |  |  | Tibero database |
| 8642 | Unofficial |  |  | Lotus Notes Traveler auto synchronization for Windows Mobile and Nokia devices |
| 8691 | Unofficial |  |  | Ultra Fractal, a fractal generation and rendering software application– distributed calculations over networked computers |
| 8728 | Unofficial |  |  | MikroTik RouterOS API |
| 8729 | Unofficial |  |  | MikroTik RouterOS API-SSL |
| 8765 | Unofficial | No |  | Default port of a local GUN relay peer that the Internet Archive and others use as a decentralized mirror for censorship resistance |
| 8767 | Unofficial |  |  | Voice channel of TeamSpeak 2, a proprietary Voice over IP protocol targeted at gamers |
| 8787 | Unofficial |  |  | Cloudflare Workers development default |
| 8834 | Unofficial |  |  | Nessus, a vulnerability scanner– remote XML-RPC web server |
| 8840 | Unofficial |  |  | Opera Unite, an extensible framework for web applications |
| 8880 | Yes |  |  | Alternate port of CDDB(Compact Disc Database) protocol, used to look up audio CD (compact disc) information over the Internet. See also port 888 |
| 8880 | Unofficial |  |  | IBM WebSphere Application Server SOAP connector |
| 8883 | Yes |  |  | Secure MQTT(MQTT over TLS) |
| 8887 | Unofficial |  |  | HyperVM over HTTP |
| 8888 | Unofficial |  |  | HyperVM over HTTPS |
| 8888 | Unofficial | No |  | Freenet web UI (localhost only) |
| 8888 | Unofficial |  |  | Default for IPython / Jupyter notebook dashboards |
| 8888 | Unofficial |  |  | MAMP |
| 8889 | Unofficial |  |  | MAMP |
| 8920 | Unofficial |  |  | Jellyfin HTTPS port |
| 8983 | Unofficial |  |  | Apache Solr |
| 8997 | Unofficial |  |  | Alternate port for I2P Monotone Proxy |
| 8998 | Unofficial |  |  | I2P Monotone Proxy |
| 8999 | Unofficial |  |  | Alternate port for I2P Monotone Proxy |
| 9000 | Unofficial |  |  | SonarQube Web Server |
| 9000 | Unofficial |  |  | ClickHouse default port |
| 9000 | Unofficial |  |  | DBGp |
| 9000 | Unofficial |  |  | SqueezeCenter web server & streaming |
| 9000 | Unofficial |  |  | UDPCast |
| 9000 | Unofficial |  |  | Play Framework web server |
| 9000 | Unofficial |  |  | Hadoop NameNode default port |
| 9000 | Unofficial |  |  | PHP-FPM default port |
| 9000 | Unofficial |  |  | qBittorrent's embedded torrent tracker default port |
| 9000 | Unofficial |  |  | Emidate |
| 9001 | Yes |  |  | ETL Service Manager |
| 9001 | Unofficial |  |  | Microsoft SharePoint authoring environment |
| 9001 | Unofficial |  |  | cisco-xremote router configuration |
| 9001 | Unofficial |  |  | Tor network default (ORPort) |
| 9001 | Unofficial |  |  | DBGp Proxy |
| 9001 | Unofficial |  |  | HSQLDB default port |
| 9001 | Unofficial |  |  | Emidate |
| 9002 | Unofficial |  |  | Newforma Server comms |
| 9002 | Unofficial |  |  | Emidate |
| 9003 | Unofficial |  |  | Xdebug default client port |
| 9006 | Unofficial |  |  | Tomcat in standalone mode |
| 9008 | Unofficial |  |  | Zerto VRA encrypted communications listener |
| 9030 | Unofficial |  |  | Tor network default (DirPort) |
| 9042 | Unofficial |  |  | Apache Cassandra native protocol clients |
| 9043 | Unofficial |  |  | WebSphere Application Server Administration Console secure |
| 9050–9051 | Unofficial |  |  | Tor(SOCKS-5 proxy) |
| 9060 | Unofficial |  |  | WebSphere Application Server Administration Console |
| 9080 | Yes |  |  | glrpc, Groove Collaboration software GLRPC |
| 9080 | Unofficial |  |  | WebSphere Application Server HTTP Transport (port 1) default |
| 9080 | Unofficial |  |  | Remote Potato by FatAttitude, Windows Media Center addon |
| 9080 | Unofficial |  |  | ServerWMC, Windows Media Center addon |
| 9081 | Unofficial |  |  | Zerto ZVM to ZVM communication |
| 9090 | Unofficial |  |  | Cockpit |
| 9090 | Unofficial |  |  | Prometheus metrics server |
| 9090 | Unofficial |  |  | Openfire Administration console |
| 9090 | Unofficial |  |  | SqueezeCenter control (CLI) |
| 9090 | Unofficial |  |  | Cherokee Admin panel |
| 9091 | Unofficial |  |  | Openfire Administration console (SSL secured) |
| 9091 | Unofficial |  |  | Transmission (BitTorrent client) Web interface |
| 9092 | Unofficial |  |  | H2 (DBMS) Database server |
| 9092 | Unofficial |  |  | Apache Kafka A Distributed Streaming Platform |
| 9095 | Unofficial |  |  | Networker Web user interface server |
| 9100 | Yes | Assigned |  | PDL Data Stream, used for printing to certain network printers |
| 9101 | Yes |  |  | Bacula Director |
| 9102 | Yes |  |  | Bacula File Daemon |
| 9103 | Yes |  |  | Bacula Storage Daemon |
| 9116 | Unofficial |  |  | SNMP-exporter (Prometheus) |
| 9119 | Yes |  |  | MXit Instant Messenger |
| 9150 | Unofficial |  |  | Tor browser |
| 9191 | Unofficial |  |  | Sierra Wireless Airlink |
| 9199 | Unofficial |  |  | Avtex LLC—qStats |
| 9200 | Unofficial |  |  | Elasticsearch—default Elasticsearch port |
| 9217 | Unofficial |  |  | iPass Platform Service |
| 9229 | Unofficial |  |  | NodeJS debugging default port (localhost) |
| 9293 | Unofficial |  |  | Sony PlayStation RemotePlay |
| 9295 | Unofficial |  |  | Sony PlayStation Remote Play Session creation communication port |
| 9296 | Unofficial |  |  | Sony PlayStation Remote Play |
| 9297 | Unofficial |  |  | Sony PlayStation Remote Play Video stream |
| 9300 | Unofficial |  |  | IBM Cognos BI |
| 9303 | Unofficial |  |  | D-Link Shareport Share storage and MFP printers |
| 9306 | Yes |  |  | Sphinx Native API |
| 9309 | Unofficial |  |  | Sony PlayStation Vita Host Collaboration WiFi Data Transfer |
| 9312 | Yes |  |  | Sphinx SphinxQL |
| 9332 | Unofficial |  |  | Litecoin JSON-RPC server |
| 9333 | Unofficial |  |  | Litecoin |
| 9339 | Unofficial |  |  | Used by all Supercell games such as Brawl Stars and Clash of Clans, mobile freemium strategy video games |
| 9389 | Yes |  |  | adws, Microsoft AD DS Web Services, Powershell uses this port |
| 9392 | Unofficial | No |  | OpenVAS Greenbone Security Assistant web interface |
| 9418 | Yes |  |  | git, Git pack transfer service |
| 9419 | Unofficial |  |  | MooseFS distributed file system – master control port |
| 9420 | Unofficial |  |  | MooseFS distributed file system – master command port |
| 9421 | Unofficial |  |  | MooseFS distributed file system – master client port |
| 9422 | Unofficial |  |  | MooseFS distributed file system – Chunkservers |
| 9425 | Unofficial |  |  | MooseFS distributed file system – CGI server |
| 9443 | Unofficial |  |  | VMware Websense Triton console (HTTPS port used for accessing and administrating a vCenter Server via the Web Management Interface) |
| 9443 | Unofficial |  |  | NCSA Brown Dog Data Tilling Service |
| 9535 | Yes |  |  | mngsuite, LANDesk Management Suite Remote Control |
| 9536 | Yes |  |  | laes-bf, IP Fabrics Surveillance buffering function |
| 9600 | No | Unofficial |  | Factory Interface Network Service(FINS), a network protocol used by Omron programmable logic controllers |
| 9669 | Unofficial | No |  | VGG Image Search Engine VISE |
| 9675 | Unofficial |  |  | Spiceworks Desktop, IT Helpdesk Software |
| 9676 | Unofficial |  |  | Spiceworks Desktop, IT Helpdesk Software |
| 9695 | Yes |  |  | Content centric networking(CCN, CCNx) |
| 9735 | Unofficial |  |  | Bitcoin Lightning Network |
| 9761 | Unofficial |  |  | Roboteq Motor controller |
| 9785 | Unofficial |  |  | Viber |
| 9800 | Yes |  |  | WebDAV Source |
| 9800 | Unofficial |  |  | WebCT e-learning portal |
| 9875 | Unofficial |  |  | Club Penguin Disney online game for kids |
| 9876 | Unofficial |  |  | V Rising Dedicated server |
| 9877 | Unofficial |  |  | V Rising Dedicated server |
| 9898 | Unofficial |  |  | Tripwire—File Integrity Monitoring Software |
| 9899 | Yes |  |  | SCTP tunneling (port number used in SCTP packets encapsulated in UDP, RFC 6951) |
| 9901 | Unofficial |  |  | Banana for Apache Solr |
| 9911 | Unofficial |  |  | Curecoin |
| 9981 | Unofficial |  |  | Tvheadend HTTP server (web interface) |
| 9982 | Unofficial |  |  | Tvheadend HTSP server (Streaming protocol) |
| 9987 | Unofficial | No |  | TeamSpeak 3 server default (voice) port (for the conflicting service see the IANA list) |
| 9993 | Unofficial |  |  | ZeroTier Default port for ZeroTier |
| 9997 | Unofficial |  |  | Splunk port for communication between the forwarders and indexers |
| 9999 | Unofficial |  |  | Urchin Web Analytics |
| 9999 | Unofficial |  |  | Dash (cryptocurrency) |
| 10000 | Yes |  |  | Network Data Management Protocol (NDMP) Control stream for network backup and restore |
| 10000 | Unofficial |  |  | BackupExec |
| 10000 | Unofficial |  |  | Webmin, Web-based Unix/Linux system administration tool (default port) |
| 10000–20000 | No | Unofficial |  | Used on VoIP networks for receiving and transmitting voice telephony traffic which includes Google Voice via the OBiTalk ATA devices as well as on the MagicJack and Vonage ATA network devices |
| 10001 | Unofficial |  |  | Ubiquiti UniFi access points broadcast to 255.255.255.255:10001 (UDP) to locate the controller(s) |
| 10009 | Unofficial |  |  | Crossfire, a multiplayer online First Person Shooter |
| 10011 | Unofficial | No |  | TeamSpeak 3 ServerQuery |
| 10022 | Unofficial | No |  | TeamSpeak 3 ServerQuery over SSH |
| 10024 | Unofficial |  |  | Zimbra smtp [mta]—to amavis from postfix |
| 10025 | Unofficial |  |  | Zimbra smtp [mta]—back to postfix from amavis |
| 10042 | Unofficial |  |  | Mathoid server |
| 10050 | Yes |  |  | Zabbix agent |
| 10051 | Yes |  |  | Zabbix trapper |
| 10101 | Unofficial |  |  | arx Compressed file transfer protocol |
| 10110 | Yes |  |  | NMEA 0183 Navigational Data. Transport of NMEA 0183 sentences over TCP or UDP |
| 10172 | Unofficial |  |  | Intuit Quickbooks client |
| 10200 | Unofficial |  |  | FRISK Software International's fpscand virus scanning daemon for Unix platforms |
| 10200 | Unofficial |  |  | FRISK Software International's f-protd virus scanning daemon for Unix platforms |
| 10200 | Unofficial |  |  | Wyoming protocol (Text-to-Speech) |
| 10201–10204 | Unofficial |  |  | FRISK Software International's f-protd virus scanning daemon for Unix platforms |
| 10212 | Yes |  |  | GE Intelligent Platforms Proficy HMI/SCADA – CIMPLICITY WebView |
| 10308 | Unofficial |  |  | Digital Combat Simulator Dedicated Server |
| 10346 | No |  |  | TEKWorx Limited – interfaceIT board protocol |
| 10468 | Unofficial |  |  | Flyer – discovery protocol |
| 10480 | Unofficial |  |  | SWAT 4 Dedicated Server |
| 10505 | Unofficial |  |  | BlueStacks (android simulator) broadcast |
| 10514 | Unofficial |  |  | TLS-enabled Rsyslog (default by convention) |
| 10578 | Unofficial | No |  | Skyrim Together multiplayer server for The Elder Scrolls V: Skyrim mod |
| 10800 | Unofficial |  |  | Touhou versus games (Immaterial and Missing Power, Phantasmagoria of Flower View, Scarlet Weather Rhapsody, Hisoutensoku, Hopeless Masquerade and Urban Legend in Limbo) |
| 10801 | Unofficial |  |  | Bag With Friends multiplayer server for the Peaks of Yore mod |
| 10823 | Unofficial |  |  | Farming Simulator 2025 |
| 10891 | Unofficial |  |  | Jungle Disk (this port is opened by the Jungle Disk Monitor service on the localhost) |
| 10933 | Yes | No |  | Octopus Deploy Tentacle deployment agent |
| 11000 | No | Unofficial |  | University of Utah CS3500 Software Software Practice |
| 11100 | No | Unofficial |  | Risk of Rain multiplayer server |
| 11111 | Unofficial |  |  | RiCcI, Remote Configuration Interface (Redhat Linux) |
| 11112 | Yes |  |  | ACR/ NEMA Digital Imaging and Communications in Medicine(DICOM) |
| 11211 | Unofficial |  |  | memcached |
| 11214 | Unofficial |  |  | memcached incoming SSL proxy |
| 11215 | Unofficial |  |  | memcached internal outgoing SSL proxy |
| 11235 | Yes |  |  | XCOMPUTE numerical systems messaging (Xplicit Computing) |
| 11311 | Unofficial |  |  | Robot Operating System master |
| 11371 | Yes |  |  | OpenPGP HTTP key server |
| 11434 | Unofficial |  |  | Ollama to run LLM locally |
| 11753 | Unofficial |  |  | OpenRCT2 multiplayer |
| 12000 | Unofficial |  |  | CubeForm, Multiplayer SandBox Game |
| 12012 | Unofficial |  |  | Audition Online Dance Battle, Korea Server—Status/Version Check |
| 12013 | Unofficial |  |  | Audition Online Dance Battle, Korea Server |
| 12035 | Unofficial |  |  | Second Life, used for server UDP in-bound |
| 12043 | Unofficial |  |  | Second Life, used for LSL HTTPS in-bound |
| 12046 | Unofficial |  |  | Second Life, used for LSL HTTP in-bound |
| 12201 | Unofficial |  |  | Graylog Extended Log Format (GELF) |
| 12222 | Yes |  |  | Light Weight Access Point Protocol (LWAPP) LWAPP data (RFC 5412) |
| 12223 | Yes |  |  | Light Weight Access Point Protocol (LWAPP) LWAPP control (RFC 5412) |
| 12307 | Unofficial |  |  | Makerbot UDP Broadcast (client to printer) (JSON-RPC) |
| 12308 | Unofficial |  |  | Makerbot UDP Broadcast (printer to client) (JSON-RPC) |
| 12345 | Unofficial |  |  | Cube World |
| 12345 | Unofficial |  |  | Little Fighter 2 |
| 12345 | Unofficial |  |  | NetBus remote administration tool (often Trojan horse) |
| 12443 | Unofficial |  |  | IBM HMC web browser management access over HTTPS instead of default port 443 |
| 12489 | Unofficial |  |  | NSClient/NSClient++/NC_Net (Nagios) |
| 12975 | Unofficial |  |  | LogMeIn Hamachi(VPN tunnel software; also port 32976)—used to connect to Mediation Server (bibi.hamachi.cc); will attempt to use SSL(TCP port 443) if both 12975 & 32976 fail to connect |
| 13000–13050 | Unofficial |  |  | Second Life, used for server UDP in-bound |
| 13008 | Unofficial |  |  | Crossfire, a multiplayer online First Person Shooter |
| 13075 | Yes |  |  | Default for BMC Software Control-M/Enterprise Manager Corba communication, though often changed during installation |
| 13400 | Yes |  |  | ISO 13400 Road vehicles — Diagnostic communication over Internet Protocol (DoIP) |
| 13720 | Yes |  |  | Symantec NetBackup—bprd (formerly VERITAS) |
| 13721 | Yes |  |  | Symantec NetBackup—bpdbm (formerly VERITAS) |
| 13724 | Yes |  |  | Symantec Network Utility—vnetd (formerly VERITAS) |
| 13782 | Yes |  |  | Symantec NetBackup—bpcd (formerly VERITAS) |
| 13783 | Yes |  |  | Symantec VOPIED protocol (formerly VERITAS) |
| 13785 | Yes |  |  | Symantec NetBackup Database—nbdb (formerly VERITAS) |
| 13786 | Yes |  |  | Symantec nomdb (formerly VERITAS) |
| 14550 | Unofficial |  |  | MAVLink Ground Station Port |
| 14567 | Unofficial |  |  | Battlefield 1942 and mods |
| 14652 | Unofficial |  |  | Repgen DoxBox reporting tool |
| 14800 | Unofficial |  |  | Age of Wonders III p2p port |
| 15000 | Unofficial |  |  | psyBNC |
| 15000 | Unofficial |  |  | Wesnoth |
| 15000 | Unofficial |  |  | Kaspersky Network Agent |
| 15000 | Unofficial |  |  | Teltonika networks remote management system (RMS) |
| 15009 | Unofficial |  |  | Teltonika networks remote management system (RMS) |
| 15010 | Unofficial |  |  | Teltonika networks remote management system (RMS) |
| 15441 | Unofficial |  |  | ZeroNet fileserver |
| 15567 | Unofficial |  |  | Battlefield Vietnam and mods |
| 15345 | Yes |  |  | XPilot Contact |
| 15672 | Unofficial | No |  | RabbitMQ management plugin |
| 16000 | Unofficial |  |  | Oracle WebCenter Content: Imaging (formerly known as Oracle Universal Content Management). Port though often changed during installation |
| 16000 | Unofficial |  |  | shroudBNC |
| 16080 | Unofficial |  |  | macOS Server Web (HTTP) service with performance cache |
| 16200 | Unofficial |  |  | Oracle WebCenter Content: Content Server (formerly known as Oracle Universal Content Management). Port though often changed during installation |
| 16225 | Unofficial |  |  | Oracle WebCenter Content: Content Server Web UI. Port though often changed during installation |
| 16250 | Unofficial |  |  | Oracle WebCenter Content: Inbound Refinery (formerly known as Oracle Universal Content Management). Port though often changed during installation |
| 16261 | Unofficial |  |  | Project Zomboid multiplayer. Additional sequential ports used for each player connecting to server |
| 16300 | Unofficial |  |  | Oracle WebCenter Content: Records Management (formerly known as Oracle Universal Records Management). Port though often changed during installation |
| 16379 | Unofficial |  |  | Redis Cluster bus |
| 16384 | Unofficial |  |  | CISCO Default RTP MIN |
| 16384–16403 | Unofficial |  |  | Real-time Transport Protocol(RTP), RTP Control Protocol(RTCP), used by Apple's iChat for audio and video |
| 16384–16387 | Unofficial |  |  | Real-time Transport Protocol (RTP), RTP Control Protocol (RTCP), used by Apple's FaceTime and Game Center |
| 16393–16402 | Unofficial |  |  | Real-time Transport Protocol (RTP), RTP Control Protocol (RTCP), used by Apple's FaceTime and Game Center |
| 16403–16472 | Unofficial |  |  | Real-time Transport Protocol (RTP), RTP Control Protocol (RTCP), used by Apple's Game Center |
| 16400 | Unofficial |  |  | Oracle WebCenter Content: Capture (formerly known as Oracle Document Capture). Port though often changed during installation |
| 16567 | Unofficial |  |  | Battlefield 2 and mods |
| 17000 | Unofficial |  |  | M17 – Digital RF voice and data protocol with Internet (UDP) gateways (reflectors) |
| 17011 | Unofficial |  |  | Worms multiplayer |
| 17224 | Yes |  |  | Train Realtime Data Protocol (TRDP) Process Data, network protocol used in train communication |
| 17225 | Yes |  |  | Train Realtime Data Protocol (TRDP) Message Data, network protocol used in train communication |
| 17333 | Unofficial |  |  | CS Server (CSMS), default binary protocol port |
| 17472 | Unofficial |  |  | Tanium Communication Port |
| 17474 | Unofficial |  |  | DMXControl 3 Network Discovery |
| 17475 | Unofficial |  |  | DMXControl 3 Network Broker |
| 17476 | Unofficial |  |  | DMXControl 3 Network Broker TLS |
| 17500 | Yes |  |  | Dropbox LanSync Protocol (db-lsp); used to synchronize file catalogs between Dropbox clients on a local network |
| 18080 | Unofficial | No |  | Monero P2P network communications |
| 18081 | Unofficial | No |  | Monero incoming RPC calls |
| 18091 | Unofficial |  |  | memcached Internal REST HTTPS for SSL |
| 18092 | Unofficial |  |  | memcached Internal CAPI HTTPS for SSL |
| 18104 | Yes |  |  | RAD PDF Service |
| 18200 | Unofficial |  |  | Audition Online Dance Battle, AsiaSoft Thailand Server status/version check |
| 18201 | Unofficial |  |  | Audition Online Dance Battle, AsiaSoft Thailand Server |
| 18206 | Unofficial |  |  | Audition Online Dance Battle, AsiaSoft Thailand Server FAM database |
| 18300 | Unofficial |  |  | Audition Online Dance Battle, AsiaSoft SEA Server status/version check |
| 18301 | Unofficial |  |  | Audition Online Dance Battle, AsiaSoft SEA Server |
| 18306 | Unofficial |  |  | Audition Online Dance Battle, AsiaSoft SEA Server FAM database |
| 18333 | Unofficial |  |  | Bitcoin testnet |
| 18400 | Unofficial |  |  | Audition Online Dance Battle, KAIZEN Brazil Server status/version check |
| 18401 | Unofficial |  |  | Audition Online Dance Battle, KAIZEN Brazil Server |
| 18505 | Unofficial |  |  | Audition Online Dance Battle R4p3 Server, Nexon Server status/version check |
| 18506 | Unofficial |  |  | Audition Online Dance Battle, Nexon Server |
| 18605 | Unofficial |  |  | X-BEAT status/version check |
| 18606 | Unofficial |  |  | X-BEAT |
| 18676 | Unofficial |  |  | YouView |
| 18769 | Yes |  |  | iQue Protocol |
| 18789 | Unofficial |  |  | OpenClaw Gateway |
| 19000 | Unofficial |  |  | Audition Online Dance Battle, G10/alaplaya Server status/version check |
| 19000 | Unofficial |  |  | JACK sound server |
| 19001 | Unofficial |  |  | Audition Online Dance Battle, G10/alaplaya Server |
| 19132 | Unofficial |  |  | Minecraft: Bedrock Edition multiplayer server |
| 19133 | Unofficial |  |  | Minecraft: Bedrock Edition IPv6 multiplayer server |
| 19150 | Unofficial |  |  | Gkrellm Server |
| 19226 | Unofficial |  |  | Panda Software AdminSecure Communication Agent |
| 19294 | Unofficial |  |  | Google Talk Voice and Video connections |
| 19295 | Unofficial |  |  | Google Talk Voice and Video connections |
| 19302 | Unofficial |  |  | Google Talk Voice and Video connections |
| 19531 | Unofficial | No |  | systemd-journal-gatewayd |
| 19532 | Unofficial | No |  | systemd-journal-remote |
| 19788 | No | Yes |  | Mesh Link Establishment protocol for IEEE 802.15.4 radio mesh networks |
| 19771 | Unofficial |  |  | Softros LAN Messenger uses TCP and UDP ports for collecting user lists and sending messages |
| 19812 | Yes | No |  | 4D database SQL Communication |
| 19813 | Yes |  |  | 4D database Client Server Communication |
| 19814 | Yes |  |  | 4D database DB4D Communication |
| 19818 | Unofficial | Unofficial |  | Vereign mesh network. Client-to-client data transfer over secure direct tunnel. It uses TCP and UDP |
| 19880 | Unofficial |  |  | Softros LAN Messenger uses TCP port for file transfers |
| 19999 | Yes |  |  | Distributed Network Protocol—Secure (DNP—Secure), a secure version of the protocol used in SCADA systems between communicating RTU's and IED's |
| 20000 | Yes |  |  | Distributed Network Protocol (DNP), a protocol used in SCADA systems between communicating RTU's and IED's |
| 20000 | Yes |  |  | OpenWebNet, communications protocol used in Bticino products |
| 20000 | Unofficial |  |  | Usermin, Web-based Unix/Linux user administration tool (default port) |
| 20000 | Unofficial |  |  | Used on VoIP networks for receiving and transmitting voice telephony traffic which includes Google Voice via the OBiTalk ATA devices as well as on the MagicJack and Vonage ATA network devices |
| 20560 | Unofficial |  |  | Killing Floor |
| 20580 | Unofficial | Unofficial |  | Walljam device communications |
| 20581 | Unofficial | Unofficial |  | Walljam device communications |
| 20595 | Unofficial |  |  | 0 A.D. Empires Ascendant |
| 20808 | Unofficial |  |  | Ableton Link |
| 21025 | Unofficial |  |  | Starbound Server (default), Starbound |
| 21064 | Unofficial |  |  | Default Ingres DBMS server |
| 22000 | Unofficial |  |  | Syncthing(default) |
| 22067 | Unofficial |  |  | Syncthing Relay Server(strelaysrv) |
| 22070 | Unofficial |  |  | Syncthing Relay Server (strelaysrv) – Status service |
| 22136 | Unofficial |  |  | FLIR Systems Camera Resource Protocol |
| 22222 | Unofficial |  |  | Davis Instruments, WeatherLink IP |
| 22347 | Yes |  |  | WibuKey, WIBU-SYSTEMS AG Copy protection |
| 22350 | Yes |  |  | CodeMeter, WIBU-SYSTEMS AG Copy protection |
| 22351 | Yes |  |  | CodeMeter-CmWAN, WIBU-SYSTEMS AG Copy protection |
| 23073 | Unofficial |  |  | Soldat Dedicated Server |
| 23399 | Unofficial |  |  | Skype default protocol |
| 23513 | Unofficial |  |  | Duke Nukem 3D source ports |
| 24441 | Unofficial |  |  | Pyzor spam detection network |
| 24444 | Unofficial |  |  | NetBeans integrated development environment |
| 24454 | Unofficial |  |  | Minecraft(Java Edition) Simple Voice Chat mod voice server |
| 24465 | Yes |  |  | Tonido Directory Server for Tonido which is a Personal Web App and P2P platform |
| 24554 | Yes |  |  | BINKP, Fidonet mail transfers over TCP/IP |
| 24576 | Unofficial |  |  | MINT Protocol used for Motorola, Zebra, and Extreme Networks wireless |
| 24800 | Unofficial |  |  | Synergy: keyboard/mouse sharing software |
| 24842 | Unofficial |  |  | StepMania: Online: Dance Dance Revolution Simulator |
| 25565 | Unofficial |  |  | Minecraft(Java Edition) multiplayer server |
| 25565 | Unofficial |  |  | Minecraft (Java Edition) multiplayer server query |
| 25575 | Unofficial |  |  | Minecraft (Java Edition) multiplayer server RCON |
| 25585 | Unofficial |  |  | Minecraft (Java Edition) multiplayer server management |
| 25734–25735 | Unofficial |  |  | SolidWorks SolidNetworkLicense Manager |
| 25826 | Unofficial |  |  | collectd default port |
| 26000 | Yes |  |  | id Software's Quake server |
| 26000 | Unofficial |  |  | EVE Online, iVentoy webGUI (see Ventoy) |
| 26000 | Unofficial |  |  | Xonotic, an open-source arena shooter |
| 26822 | Unofficial |  |  | MSI MysticLight |
| 26900–26901 | Unofficial |  |  | EVE Online |
| 26909–26911 | Unofficial |  |  | Action Tanks Online |
| 27000 | Unofficial |  |  | PowerBuilder SySAM license server |
| 27000–27006 | Unofficial |  |  | id Software's QuakeWorld master server |
| 27000–27009 | Yes |  |  | FlexNet Publisher's License server (from the range of default ports) |
| 27000–27015 | No | Unofficial |  | Steam(game client traffic) |
| 27015 | No | Unofficial |  | GoldSrc, Source engine and Source 2 engine dedicated server port |
| 27015–27018 | Unofficial |  |  | Unturned, a survival game |
| 27015–27030 | No | Unofficial |  | Steam (matchmaking and HLTV) |
| 27015–27030 | Unofficial |  |  | Steam (downloads) |
| 27016 | Unofficial |  |  | Magicka and Space Engineers server port |
| 27017 | Unofficial | No |  | MongoDB daemon process (`mongod`) and routing service (`mongos`) |
| 27031–27035 | No | Unofficial |  | Steam (In-Home Streaming) |
| 27036 | Unofficial |  |  | Steam (In-Home Streaming) |
| 27100 | Unofficial |  |  | Screen Play Games controller |
| 27374 | Unofficial |  |  | Sub7 default |
| 27500–27900 | Unofficial |  |  | id Software's QuakeWorld |
| 27888 | Unofficial |  |  | Kaillera server |
| 27901–27910 | Unofficial |  |  | id Software's Quake II master server |
| 27950 | Unofficial |  |  | OpenArena outgoing |
| 27960–27969 | Unofficial |  |  | Activision's Enemy Territory and id Software's Quake III Arena, Quake III and Quake Live and some ioquake3 derived games, such as Urban Terror (OpenArena incoming) |
| 28000 | Yes |  |  | Siemens Digital Industries Software license server |
| 28001 | Unofficial |  |  | Starsiege: Tribes |
| 28015 | Unofficial |  |  | Rust (video game) |
| 28016 | Unofficial |  |  | Rust (video game) RCON |
| 28200 | Assigned |  |  | VoxelStorm game server |
| 28260 | Unofficial |  |  | Palo Alto Networks' Panorama HA-1 backup unencrypted sync port |
| 28443 | Unofficial |  |  | Palo Alto Networks' Panorama-to-managed devices software updates, PAN-OS 8.0 and later |
| 28769 | Unofficial |  |  | Palo Alto Networks' Panorama HA unencrypted sync port |
| 28770 | Unofficial |  |  | Palo Alto Networks' Panorama HA-1 backup sync port |
| 28770–28771 | Unofficial |  |  | AssaultCube Reloaded, a video game based upon a modification of AssaultCube |
| 28785–28786 | Unofficial |  |  | Cube 2: Sauerbraten |
| 28852 | Unofficial |  |  | Killing Floor |
| 28910 | Unofficial |  |  | Nintendo Wi-Fi Connection |
| 28960 | Unofficial |  |  | Call of Duty; Call of Duty: United Offensive; Call of Duty 2; Call of Duty 4: Modern Warfare Call of Duty: World at War(PC platform) |
| 29000 | Yes |  |  | Siemens Digital Industries Software license server |
| 29070 | Unofficial |  |  | Jedi Knight: Jedi Academy by Ravensoft |
| 29900–29901 | Unofficial |  |  | Nintendo Wi-Fi Connection |
| 29920 | Unofficial |  |  | Nintendo Wi-Fi Connection |
| 30000 | Unofficial |  |  | XLink Kai P2P |
| 30000 | Unofficial |  |  | Luanti server default port |
| 30000 | Unofficial |  |  | Foundry Virtual Tabletop server default port |
| 30003 | Yes | Yes |  | Amicon FPSU-IP Remote Administration |
| 30004 | Yes | Yes |  | Amicon FPSU-IP VPN |
| 30033 | Unofficial | No |  | TeamSpeak 3 File Transfer |
| 30120 | Unofficial |  |  | FiveM(Default Port) GTA V multiplayer |
| 30564 | Unofficial |  |  | Multiplicity: keyboard/mouse/clipboard sharing software |
| 30814 | Unofficial |  |  | BeamMP: Unofficial BeamNG.drive multiplayer mod. Default server port |
| 31337 | Unofficial |  |  | Back Orifice and Back Orifice 2000 remote administration tools |
| 31337 | Unofficial |  |  | ncat, a netcat alternative |
| 31416 | Unofficial |  |  | BOINC RPC |
| 31438 | Unofficial |  |  | Rocket U2 |
| 31457 | Yes |  |  | TetriNET |
| 32137 | Unofficial |  |  | Immunet Protect(UDP in version 2.0, TCP since version 3.0) |
| 32400 | Yes |  |  | Plex Media Server |
| 32749 | Unofficial |  |  | Gridcoin |
| 32764 | Unofficial |  |  | A backdoor found on certain Linksys, Netgear and other wireless DSL modems/combination routers |
| 32887 | Unofficial |  |  | Ace of Spades, a multiplayer FPS video game |
| 32976 | Unofficial |  |  | LogMeIn Hamachi, a VPN application; also TCP port 12975 and SSL(TCP 443) |
| 33434 | Yes |  |  | traceroute |
| 33848 | Unofficial |  |  | Jenkins, a continuous integration(CI) tool |
| 34000 | Unofficial |  |  | Infestation: Survivor Stories(formerly known as The War Z), a multiplayer zombie video game |
| 34197 | No | Unofficial |  | Factorio, a multiplayer survival and factory-building game |
| 35357 | Yes |  |  | OpenStack Identity(Keystone) administration |
| 36330 | Unofficial |  |  | Folding@home Control Port |
| 37008 | Unofficial |  |  | TZSP intrusion detection |
| 38412 | Yes |  |  | NG Application Protocol (NGAP) for communication between a gNB and AMF in 5G core networks |
| 40000 | Yes |  |  | SafetyNET p– a real-time Industrial Ethernet protocol |
| 41121 | Yes | Reserved |  | Tentacle Server – Pandora FMS |
| 41230 | Assigned | Yes |  | Z-Wave Protocol over DTLS |
| 41794 | Yes |  |  | Crestron Control Port – Crestron Electronics |
| 41795 | Yes |  |  | Crestron Terminal Port – Crestron Electronics |
| 41796 | Yes | No |  | Crestron Secure Control Port – Crestron Electronics |
| 41797 | Yes | No |  | Crestron Secure Terminal Port – Crestron Electronics |
| 42081–42090 | Yes |  |  | Zippin –Zippin Store |
| 42420 | Unofficial |  |  | Vintage Story multiplayer server |
| 42590–42595 | Yes |  |  | Glue – MakePro X |
| 42999 | Yes |  |  | Curiosity |
| 43110 | Unofficial |  |  | ZeroNet web UI default port |
| 43594–43595 | Unofficial |  |  | RuneScape |
| 44123 | Assigned | Unofficial |  | Z-Wave Secure Tunnel |
| 44405 | Unofficial |  |  | Mu Online Connect Server |
| 44818 | Yes |  |  | EtherNet/IP explicit messaging |
| 47808–47823 | Yes |  |  | BACnet Building Automation and Control Networks (4780810 = BAC016 to 4782310 = BACF16) |
| 48556 | Yes |  |  | drive.web AC/DC Drive Automation and Control Networks |
| 48656 | Unofficial |  |  | Brainy LAB Control Server |
| 48657 | Unofficial |  |  | Brainy LAB Control Server |
| 49151 | Reserved |  |  | "IANA Reserved" |

---

## Dynamic, private or ephemeral ports (49152–65535)

| Port | TCP | UDP | Observations | Description |
|------|-----|-----|--------------|-------------|
| 49152–65535 | Unofficial | No |  | Certificate Management over CMS and Xsan Filesystem Access |
| 49160 | Unofficial |  |  | Palo Alto Networks' Panorama |
| 50160 | Unofficial |  |  | S-CONNECT protocol – data exchange (TCP) and manual device pairing (UDP) |
| 50161 | Unofficial |  |  | S-CONNECT protocol – automatic device pairing |
| 51413 | Unofficial |  |  | Transmission (BitTorrent client) |
| 51515 | Unofficial |  |  | Kopia server |
| 51820 | No | Unofficial |  | WireGuard protocol |
| 52380 | No | Unofficial |  | Sony VISCA Network Setting Protocol |
| 52381 | No | Unofficial |  | Sony VISCA over IP Protocol |
| 53317 | Unofficial |  |  | LocalSend |
| 59100 | Unofficial |  |  | AudioRelay |
| 60000–61000 | No | Unofficial |  | Range from which Mosh– a remote-terminal application similar to SSH– typically assigns ports for ongoing sessions between Mosh servers and Mosh clients |
| 61616 | Unofficial |  |  | ActiveMQ Classic |
| 61616–61631 | compressible |  |  | Ports with efficient compression in 6LoWPAN header compression |
| 62078 | Unofficial |  |  | Apple's lockdownd protocol – used for communicating with iPhones and iPads |
| 64738 | Unofficial |  |  | Mumble |

---

## External links

- [List of TCP and UDP port numbers — Wikipedia](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers)
- [IANA Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
- [RFC 6335 — Internet Assigned Numbers Authority (IANA) Procedures for the Management of the Service Name and Transport Protocol Port Number Registry](https://www.rfc-editor.org/rfc/rfc6335)
