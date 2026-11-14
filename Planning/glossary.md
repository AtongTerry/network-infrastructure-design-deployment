# Glossary

Plain-language definitions of the terms used in this project, with the lab's own values as examples.

## Naming

| Term | Meaning |
|---|---|
| **BR01** | Branch 01, the site code that starts every device name. A second site would be BR02. |
| **SITE-ROLE-NN** | The device naming standard. `BR01-ACC-02` is site BR01, access switch, number 02. |
| **RTR / CORE / ACC / AP / UPS** | Role codes: edge router, core switch, access switch, wireless access point, battery backup. |
| **IDF** | Intermediate Distribution Frame: a network closet. This lab has one (IDF1). |

## Addressing

| Term | Meaning |
|---|---|
| **IP address** | A device's network address, for example `192.168.2.193`. |
| **Subnet** | A block of addresses that share a network prefix, for example `192.168.2.192/28`. |
| **Prefix length (/28)** | How many leading bits identify the network. `/28` leaves 4 host bits, so 16 addresses (14 usable). |
| **Subnet mask** | The same idea written as dotted numbers. `/28` is `255.255.255.240`. |
| **Wildcard mask** | The inverse of the mask, used in OSPF and ACL statements. `/28` is `0.0.0.15`. |
| **Usable hosts** | Addresses in a subnet minus the network address and the broadcast address. |
| **Gateway (default gateway)** | The router address hosts send off-subnet traffic to. Here it is the first usable address of each subnet, on a core SVI. |
| **VLSM** | Variable Length Subnet Masking. Each subnet gets the prefix its host count needs, instead of one size for all. |
| **Summary route** | One route that covers many subnets. All host subnets fit in `192.168.0.0/22`. |
| **Growth allowance** | Extra addresses added to a subnet's size so it survives new hires. This lab uses 25%. |
| **Transit network** | A small routed link between two devices (a /30 with 2 usable addresses). Here: `10.10.0.32/30`. |
| **Documentation range** | Addresses reserved for examples (`203.0.113.0/24`). Used as a placeholder WAN. |
| **Static address** | An address typed in by hand. Used for servers and network devices. |

## Switching

| Term | Meaning |
|---|---|
| **Layer 2 / Layer 3** | Layer 2 switches forward by MAC address inside one VLAN. Layer 3 devices route between networks by IP address. |
| **VLAN** | Virtual LAN. A separate broadcast domain on shared switches, one per department here. |
| **Access port** | A switch port that carries one VLAN, for a PC or printer. |
| **Trunk (802.1Q)** | A link that carries several VLANs, each frame tagged with its VLAN number. |
| **Native VLAN** | The VLAN a trunk carries untagged. Set to unused VLAN 999 on every trunk for safety. |
| **Voice VLAN** | A second VLAN on an access port so the IP phone (VLAN 70) and the PC behind it stay separate. |
| **SVI** | Switched Virtual Interface. A virtual Layer 3 interface for a VLAN, which acts as that VLAN's gateway. |
| **LACP / port channel** | Bundles several physical links into one logical link with failover. Po1 to Po3 here. |
| **Spanning Tree (STP, Rapid PVST+)** | Prevents switching loops by blocking redundant paths. The core is the root bridge. |
| **Root bridge** | The switch STP builds its tree around. Set to the core with a low priority. |
| **PortFast** | Lets an access port start forwarding immediately. Only used on end-device ports. |
| **BPDU Guard** | Shuts a PortFast port if it receives spanning-tree messages, which stops someone plugging in a switch. |
| **Port security** | Limits how many MAC addresses may use a port. |
| **DHCP snooping** | Blocks rogue DHCP servers by trusting DHCP replies only from uplinks. |
| **PoE** | Power over Ethernet. Powers phones and APs through the data cable. |
| **MAC address** | The hardware address of a network card. |
| **Broadcast domain** | The set of devices that receive each other's broadcasts. One per VLAN. |

## Routing

| Term | Meaning |
|---|---|
| **Inter-VLAN routing** | Moving traffic between VLANs. Done on the core switch through SVIs. |
| **Static route** | A route typed in by hand. The edge router has one default route to the ISP. |
| **Dynamic routing** | Routers learn routes from each other automatically with a routing protocol. |
| **OSPF** | Open Shortest Path First, a dynamic routing protocol. Used between the core and the edge router. |
| **Area 0** | OSPF's backbone area. This lab has a single area. |
| **Router ID** | A unique name for an OSPF router, written like an IP address. Set manually (`10.10.0.1` core, `10.10.0.33` edge). |
| **Adjacency / neighbor** | Two OSPF routers that have formed a relationship and exchange routes. `FULL` means it is working. |
| **Point-to-point network type** | An OSPF setting for a link with exactly two routers. No election, faster convergence. |
| **Passive interface** | An interface that advertises its network but sends no OSPF messages. All user-facing SVIs are passive. |
| **`network` statement** | The OSPF command that picks which interfaces run OSPF and which networks are advertised. |
| **MD5 authentication** | A shared key that proves OSPF messages come from a trusted neighbor. |
| **`default-information originate`** | Makes the edge router tell the core about its default route. |
| **O\*E2** | How the core's routing table shows a default route learned from OSPF as an external route. |
| **Default route (0.0.0.0/0)** | The "send everything else here" route, pointing toward the internet. |
| **NAT / PAT** | Network Address Translation. PAT (overload) lets many private hosts share one public address. |
| **HSRP / VRRP** | Protocols that give two routers one shared gateway address for redundancy. A possible future upgrade. |

## Security and management

| Term | Meaning |
|---|---|
| **ACL** | Access Control List. A list of permit and deny rules that filters traffic. |
| **SSH** | Secure Shell. Encrypted remote login to devices, used instead of Telnet. |
| **Console** | The direct cable connection used for first-time setup. |
| **Banner** | A login warning message ("Authorized access only"). |
| **NTP** | Network Time Protocol. Keeps device clocks in sync so logs line up. |
| **Syslog** | Sends device log messages to a central server (the backup/syslog server here). |
| **Hardening / security baseline** | The standard set of security settings every device gets. |
| **DHCP** | Hands out IP addresses automatically. The core serves it for each VLAN. |
| **DNS** | Translates names to IP addresses. Runs on BR01-SRV-01. |
| **Rogue DHCP server** | An unauthorized device handing out addresses. DHCP snooping blocks it. |

## Deployment and documentation

| Term | Meaning |
|---|---|
| **Staging** | Configuring, labeling, and testing equipment before it goes to the site. |
| **BOM** | Bill of Materials. The list of every item to buy, with quantities. |
| **RMA** | Return Merchandise Authorization. The vendor process for replacing defective equipment. |
| **Cutover** | The planned moment the new network replaces the old one and goes live. |
| **Rollback plan** | The steps to return to the old setup if the cutover fails. |
| **Rack elevation** | A front-view diagram showing what sits in each rack slot. |
| **Patch panel** | A panel of ports where building cabling ends, connected to switches with short patch cables. |
| **Structured cabling** | The permanent cabling in walls and ceilings, run to a patch panel. |
| **UPS** | Uninterruptible Power Supply. A battery that keeps equipment running during a power loss. |
| **VA / watts** | UPS capacity ratings. Choose a UPS whose watt rating covers the load plus headroom. |
| **As-built diagram** | The final diagram showing what was actually installed. |
| **Closeout checklist** | The sign-off list that proves the project is finished and documented. |
| **Configuration as code** | Keeping device configs as templates and variables in Git, so every device is consistent and changes are tracked. |
| **Jinja2** | A Python templating language used to render one config per device from a template. |
| **Evidence** | Screenshots or command output that prove a test passed. |
