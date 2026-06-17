# Nugget Nesting

## Original

```mermaid
graph TD
    Root[Root Node] --> Child1[Child Node 1]
    Root --> Child2[Child Node 2]
    Child1 --> Grandchild1[Grandchild 1]
    Child1 --> Grandchild2[Grandchild 2]
```

## Simplest Systems

An ARP Scan gives you IP Addresses and MAC Addresses, so all you can infer is that a host/device is on the network.

```mermaid
graph TD
    Host[Host] -->|contains| IPAddress[IP Address]

```

## Some Systems

An ARP Scan gives you IP Addresses and MAC Addresses, so all you can infer is that a system is on the network.

```mermaid
graph TD
    System[System] --> Networking[Networking]
    Networking --> IPAddress[IP Address]
    Networking --> MACAddress[MAC Address]
```

A Port Scan gives you open ports, so you can infer that a system is running a service, and this can be done for UDP and TCP.


```mermaid
graph TD
    System[System] --> Networking[Networking]
    Networking --> IPAddress[IP Address]
    Networking --> MACAddress[MAC Address]
	IPAddress --> Protocol[Protocol]
	Protocol --> Port[Port]
```

## NMAP Scanning

```mermaid
graph TD

    Host

    Host -->|contains| IPAddress

    IPAddress -->|contains| Protocol

    Protocol -->|contains| Port

    Port -->|has| State

    Port -->|uses| Service

    Service -->|has| ServiceName
    Service -->|has| Product
    Service -->|has| Version
    Service -->|has| ExtraInfo
```




## External Scanning Service Model

```mermaid
graph TD

    Host

    Host -->|contains| OperatingSystem

    Host -->|contains| Applications

    Applications -->|contains| Service

    Service -->|listens on| Port


    Service -->|has| ServiceName
    Service -->|has| Product

    Host -->|contains| Networking

    Networking -->|contains| IPAddress

    IPAddress -->|contains| Protocol

    Protocol -->|contains| Port

    Port -->|has| State
```