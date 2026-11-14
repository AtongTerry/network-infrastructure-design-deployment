# Addressing and Routing Plan

Two address pools, each carved with VLSM (largest subnet first, no overlaps, no gaps between blocks):

| Pool | Used for | Allocated | Summary route | Reserved for growth |
|---|---|---|---|---|
| `192.168.0.0/16` | Hosts (departments, voice, Wi-Fi, printers, servers) | `192.168.0.0` to `192.168.3.31` | `192.168.0.0/22` | `192.168.3.32` onward |
| `10.10.0.0/24` | Network devices (management and transit) | `10.10.0.0` to `10.10.0.47` | `10.10.0.0/24` | `10.10.0.48` onward |

Both buildings draw from the same two pools. Building 1 was allocated first and Building 2 was appended after it, so no Building 1 subnet moved: Logistics takes `192.168.3.0/27`, the inter-building link takes `10.10.0.36/30`, and Building 2 management takes `10.10.0.40/29`.

The WAN handoff (`203.0.113.0/30`) uses the 203.0.113.0/24 documentation range as a placeholder. Routes between the two pools are learned with OSPF (see Routing design).

## Sizing method

1. Hosts needed = users x devices per user, or a fixed device count for shared VLANs.
2. Add 25% growth, rounded up.
3. Add one address for the gateway (a core switch SVI in Building 1, a router subinterface in Building 2).
4. Pick the smallest prefix whose usable host count covers the total.

Headcount: Executive 8, HR 10, Accounting 12, Operations 14, Sales 20, IT 16 = **80 employees**.

| VLAN | Name | Users | Hosts needed | +25% growth | + gateway | Prefix | Usable | Spare |
|---|---|---|---|---|---|---|---|---|
| 10 | EXEC | 8 | 8 | 10 | 11 | /28 | 14 | 3 |
| 20 | HR | 10 | 10 | 13 | 14 | /28 | 14 | 0 |
| 30 | ACCT | 12 | 12 | 15 | 16 | /27 | 30 | 14 |
| 40 | OPS | 14 | 14 | 18 | 19 | /27 | 30 | 11 |
| 50 | SALES | 20 | 20 | 25 | 26 | /27 | 30 | 4 |
| 60 | IT | 16 | 32 | 40 | 41 | /26 | 62 | 21 |
| 70 | VOICE | n/a | 80 | 100 | 101 | /25 | 126 | 25 |
| 80 | STAFF-WIFI | 80 | 160 | 200 | 201 | /24 | 254 | 53 |
| 90 | GUEST | n/a | 80 | 100 | 101 | /25 | 126 | 25 |
| 100 | PRINTERS-IOT | n/a | 18 | 23 | 24 | /27 | 30 | 6 |
| 110 | SERVERS | n/a | 4 | 5 | 6 | /29 | 6 | 0 |
| 99 | MGMT | n/a | 6 | 20 | 21 | /27 | 30 | 9 |
| 120 | LOGISTICS | 20 | 20 | 25 | 26 | /27 | 30 | 4 |
| 99 | MGMT-B2 | n/a | 2 | 3 | 4 | /29 | 6 | 2 |

Notes:
- Zero spare addresses: HR, SERVERS. They fit exactly. Move to the next larger prefix if they grow past the planned size.
- **IT** counts two devices per person (workstation plus a test or lab machine).
- **Staff Wi-Fi** counts two devices per person (laptop and phone). It is one shared VLAN. Per-department Wi-Fi would need 802.1X with RADIUS dynamic VLAN assignment, listed as a possible improvement.
- **Voice, Guest, and Printers/IoT** scale with the 80-person headcount. **Servers** stay at 4.
- **LOGISTICS** is the only department in Building 2: 20 users, one wired workstation each. **MGMT-B2** holds the Building 2 router subinterface and access switch, with room for a few more devices.
- **MGMT** is sized for expansion (extra switches, more APs, more UPS units), not just today's six devices.

## Subnets

| VLAN | Name | Network | Mask | Gateway | Host range | Broadcast |
|---|---|---|---|---|---|---|
| 10 | EXEC | 192.168.2.192/28 | 255.255.255.240 | 192.168.2.193 | 192.168.2.194 - 192.168.2.206 | 192.168.2.207 |
| 20 | HR | 192.168.2.208/28 | 255.255.255.240 | 192.168.2.209 | 192.168.2.210 - 192.168.2.222 | 192.168.2.223 |
| 30 | ACCT | 192.168.2.64/27 | 255.255.255.224 | 192.168.2.65 | 192.168.2.66 - 192.168.2.94 | 192.168.2.95 |
| 40 | OPS | 192.168.2.96/27 | 255.255.255.224 | 192.168.2.97 | 192.168.2.98 - 192.168.2.126 | 192.168.2.127 |
| 50 | SALES | 192.168.2.128/27 | 255.255.255.224 | 192.168.2.129 | 192.168.2.130 - 192.168.2.158 | 192.168.2.159 |
| 60 | IT | 192.168.2.0/26 | 255.255.255.192 | 192.168.2.1 | 192.168.2.2 - 192.168.2.62 | 192.168.2.63 |
| 70 | VOICE | 192.168.1.0/25 | 255.255.255.128 | 192.168.1.1 | 192.168.1.2 - 192.168.1.126 | 192.168.1.127 |
| 80 | STAFF-WIFI | 192.168.0.0/24 | 255.255.255.0 | 192.168.0.1 | 192.168.0.2 - 192.168.0.254 | 192.168.0.255 |
| 90 | GUEST | 192.168.1.128/25 | 255.255.255.128 | 192.168.1.129 | 192.168.1.130 - 192.168.1.254 | 192.168.1.255 |
| 100 | PRINTERS-IOT | 192.168.2.160/27 | 255.255.255.224 | 192.168.2.161 | 192.168.2.162 - 192.168.2.190 | 192.168.2.191 |
| 110 | SERVERS | 192.168.2.224/29 | 255.255.255.248 | 192.168.2.225 | 192.168.2.226 - 192.168.2.230 | 192.168.2.231 |
| 99 | MGMT | 10.10.0.0/27 | 255.255.255.224 | 10.10.0.1 | 10.10.0.2 - 10.10.0.30 | 10.10.0.31 |
| 120 | LOGISTICS | 192.168.3.0/27 | 255.255.255.224 | 192.168.3.1 | 192.168.3.2 - 192.168.3.30 | 192.168.3.31 |
| 99 | MGMT-B2 | 10.10.0.40/29 | 255.255.255.248 | 10.10.0.41 | 10.10.0.42 - 10.10.0.46 | 10.10.0.47 |
| n/a | TRANSIT | 10.10.0.32/30 | 255.255.255.252 | n/a | 10.10.0.33 - 10.10.0.34 | 10.10.0.35 |
| n/a | TRANSIT-B2 | 10.10.0.36/30 | 255.255.255.252 | n/a | 10.10.0.37 - 10.10.0.38 | 10.10.0.39 |
| n/a | WAN | 203.0.113.0/30 | 255.255.255.252 | n/a | 203.0.113.1 - 203.0.113.2 | 203.0.113.3 |

Conventions:
- The gateway is the first usable address, hosted on a core switch SVI (Building 1) or a router subinterface (Building 2).
- DHCP pools run from the first host after the gateway to the last usable address. SERVERS and MGMT are static only. Building 1 DHCP is served by the core, Building 2 DHCP by BLD2-RTR-01.
- Transit networks are routed /30 links (edge router to core, and between the two buildings). They have no VLAN.
- Native VLAN 999 is unused, unrouted, and set on every trunk.

## Network device addresses (10.10.0.0/24)

| Device | Interface | Address |
|---|---|---|
| BLD1-CORE-01 | VLAN 99 SVI (MGMT gateway) | 10.10.0.1/27 |
| BLD1-ACC-01 | VLAN 99 SVI | 10.10.0.11/27 |
| BLD1-ACC-02 | VLAN 99 SVI | 10.10.0.12/27 |
| BLD1-ACC-03 | VLAN 99 SVI | 10.10.0.13/27 |
| BLD1-AP-01 | Management | 10.10.0.21/27 |
| BLD1-AP-02 | Management | 10.10.0.22/27 |
| BLD1-UPS-01 | Network card | 10.10.0.25/27 |
| BLD1-RTR-01 | Gi0/1 inside (transit) | 10.10.0.33/30 |
| BLD1-CORE-01 | Gi1/0/24 routed port (transit) | 10.10.0.34/30 |
| BLD1-RTR-01 | Gi0/0 WAN | 203.0.113.2/30 (ISP 203.0.113.1) |
| BLD1-RTR-01 | Gi0/2 inter-building link | 10.10.0.37/30 |
| BLD2-RTR-01 | Gi0/0 inter-building link | 10.10.0.38/30 |
| BLD2-RTR-01 | Gi0/1.99 (Building 2 MGMT gateway) | 10.10.0.41/29 |
| BLD2-RTR-01 | Gi0/1.120 (LOGISTICS gateway) | 192.168.3.1/27 |
| BLD2-ACC-01 | VLAN 99 SVI | 10.10.0.42/29 |

Each Building 1 access switch also needs `ip default-gateway 10.10.0.1`. BLD2-ACC-01 uses `ip default-gateway 10.10.0.41`, the Building 2 router.

## Server addresses (192.168.2.224/29)

All servers use static addresses. The gateway is 192.168.2.225 (VLAN 110 SVI). Staff and department DHCP pools hand out 192.168.2.226 as the DNS server. Guests get a public resolver (`1.1.1.1`) so they never need to reach the server VLAN. Domain name: `campus.lab`.

| Host | Address | Role |
|---|---|---|
| BLD1-SRV-01 | 192.168.2.226/29 | Domain controller, DNS (DHCP is served by the core) |
| BLD1-SRV-02 | 192.168.2.227/29 | File server |
| BLD1-SRV-03 | 192.168.2.228/29 | Print server |
| BLD1-SRV-04 | 192.168.2.229/29 | Backup and syslog server |

## Routing design (OSPF)

Dynamic routing runs across three routing devices with **OSPFv2, single area (area 0)**: the Building 1 core switch (BLD1-CORE-01), the Building 1 edge router (BLD1-RTR-01), and the Building 2 router (BLD2-RTR-01). The edge router sits in the middle, with one adjacency to the core and one to Building 2. Single-area OSPF is enough for three routing devices. If Building 2 grew into a full site, make it its own area and turn BLD1-RTR-01 into the area border router.

| Item | Setting |
|---|---|
| Process / area | OSPF process 1, area 0 on all three devices |
| Router IDs | Core `10.10.0.1`, BLD1 edge router `10.10.0.33`, BLD2 router `10.10.0.38` (set manually, no loopbacks needed) |
| Adjacencies | Core to edge router over `10.10.0.32/30`, edge router to BLD2 router over `10.10.0.36/30` (the inter-building link) |
| Network type | `point-to-point` on both transit links (no DR/BDR election, faster convergence) |
| Authentication | MD5 on both transit links (key stored as a placeholder in the repo) |
| Passive interfaces | `passive-interface default` on all three devices. Only the transit interfaces are active, so no OSPF hellos reach user, guest, or printer VLANs |
| Core advertises | `192.168.0.0/22` (all Building 1 host SVIs) and `10.10.0.0/26` (management and transit) |
| Edge router advertises | Both transit networks (`10.10.0.32/29` covers them) and a default route (`default-information originate`) |
| BLD2 router advertises | `192.168.3.0/27` (Logistics), `10.10.0.40/29` (Building 2 management), and the inter-building link |
| Default route | Edge router has `ip route 0.0.0.0 0.0.0.0 203.0.113.1` to the ISP. The core and the BLD2 router learn the default through OSPF as an external route (`O*E2`), so neither has a static default |
| NAT | Only the edge router does PAT (`ip nat inside source list NAT-INSIDE interface Gi0/0 overload`). It translates `192.168.0.0/22`, which already includes Logistics (`192.168.3.0/27`), so Building 2 needs no NAT of its own |

### Core (BLD1-CORE-01)

```
ip routing
!
interface GigabitEthernet1/0/24
 description TRANSIT-TO-BLD1-RTR-01
 no switchport
 ip address 10.10.0.34 255.255.255.252
 ip ospf network point-to-point
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 {{OSPF_KEY}}
!
router ospf 1
 router-id 10.10.0.1
 passive-interface default
 no passive-interface GigabitEthernet1/0/24
 network 192.168.0.0 0.0.3.255 area 0
 network 10.10.0.0 0.0.0.63 area 0
```

### Edge router (BLD1-RTR-01)

```
interface GigabitEthernet0/0
 description WAN-TO-ISP
 ip address 203.0.113.2 255.255.255.252
 ip nat outside
!
interface GigabitEthernet0/1
 description TRANSIT-TO-BLD1-CORE-01
 ip address 10.10.0.33 255.255.255.252
 ip nat inside
 ip ospf network point-to-point
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 {{OSPF_KEY}}
!
interface GigabitEthernet0/2
 description INTER-BUILDING-TO-BLD2-RTR-01
 ip address 10.10.0.37 255.255.255.252
 ip nat inside
 ip ospf network point-to-point
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 {{OSPF_KEY}}
 no shutdown
!
ip route 0.0.0.0 0.0.0.0 203.0.113.1
!
ip access-list standard NAT-INSIDE
 permit 192.168.0.0 0.0.3.255
!
ip nat inside source list NAT-INSIDE interface GigabitEthernet0/0 overload
!
router ospf 1
 router-id 10.10.0.33
 passive-interface default
 no passive-interface GigabitEthernet0/1
 no passive-interface GigabitEthernet0/2
 network 10.10.0.32 0.0.0.7 area 0
 default-information originate
```

### Building 2 router (BLD2-RTR-01)

One physical port trunks to the switch and carries two 802.1Q subinterfaces (router-on-a-stick). The router is also the DHCP server and the default gateway for Building 2.

```
hostname BLD2-RTR-01
!
interface GigabitEthernet0/0
 description INTER-BUILDING-TO-BLD1-RTR-01
 ip address 10.10.0.38 255.255.255.252
 ip ospf network point-to-point
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 {{OSPF_KEY}}
 no shutdown
!
interface GigabitEthernet0/1
 description TRUNK-TO-BLD2-ACC-01
 no ip address
 no shutdown
!
interface GigabitEthernet0/1.99
 description MGMT gateway
 encapsulation dot1Q 99
 ip address 10.10.0.41 255.255.255.248
!
interface GigabitEthernet0/1.120
 description LOGISTICS gateway
 encapsulation dot1Q 120
 ip address 192.168.3.1 255.255.255.224
 ip access-group LOGISTICS-IN in
!
ip dhcp excluded-address 192.168.3.1
ip dhcp pool LOGISTICS
 network 192.168.3.0 255.255.255.224
 default-router 192.168.3.1
 dns-server 192.168.2.226
 domain-name campus.lab
!
ip access-list extended LOGISTICS-IN
 permit udp any eq bootpc any eq bootps
 deny ip any 192.168.2.208 0.0.0.15
 deny ip any 192.168.2.64 0.0.0.31
 deny ip any 10.10.0.0 0.0.0.63
 permit ip any any
!
router ospf 1
 router-id 10.10.0.38
 passive-interface default
 no passive-interface GigabitEthernet0/0
 network 10.10.0.36 0.0.0.3 area 0
 network 10.10.0.40 0.0.0.7 area 0
 network 192.168.3.0 0.0.0.31 area 0
```

`LOGISTICS-IN` keeps Logistics away from HR, Accounting, and management at the first hop. The core's `PROTECT-HR-ACCT` and `PROTECT-MGMT` ACLs enforce the same rules a second time at the destination.

### Verification

| Check | Command | Expected |
|---|---|---|
| Neighbors up | `show ip ospf neighbor` (edge router) | Two neighbors in `FULL` state: core `10.10.0.1` and BLD2 router `10.10.0.38` |
| Neighbor up | `show ip ospf neighbor` (core, BLD2 router) | One neighbor in `FULL` state each |
| Learned routes | `show ip route ospf` (edge router) | Every Building 1 host subnet, `10.10.0.0/27`, and `192.168.3.0/27` via `10.10.0.38` |
| Building 2 routes | `show ip route ospf` (BLD2 router) | `O*E2` default via `10.10.0.37`, plus every Building 1 host subnet via `10.10.0.37` |
| Core sees Building 2 | `show ip route 192.168.3.0` (core) | `O` route via `10.10.0.33` |
| Default route | `show ip route 0.0.0.0` (core) | `O*E2` via `10.10.0.33` |
| Interface settings | `show ip ospf interface brief` | Transit interfaces in area 0, network type point-to-point |
| Passive interfaces | `show ip protocols` | All SVIs (core) and `Gi0/1.99`, `Gi0/1.120` (BLD2 router) listed as passive |
| Authentication | `show ip ospf interface Gi0/2` (edge router) | Message digest authentication enabled |
| DHCP | `show ip dhcp binding` (BLD2 router) | Logistics PCs hold `192.168.3.0/27` leases, gateway `192.168.3.1` |
| End to end, internal | Logistics PC pings the file server `192.168.2.226` | Success across both transit links |
| End to end, internet | Logistics PC pings an outside address | Success. `show ip nat translations` on the edge router shows the Logistics address translated |
| Policy | Logistics PC pings an HR PC and `10.10.0.1` | Fails (ACLs working as designed) |

### Routing tests to record

1. Remove the `network` statement for one VLAN on the core. That subnet disappears from the edge router's and the BLD2 router's tables and return traffic fails.
2. Break authentication (wrong key on one side of the inter-building link). The neighbor drops, and `debug ip ospf adj` shows the mismatch. Building 2 loses all routes except its connected networks.
3. Shut the inter-building interface on the edge router. Confirm the BLD2 router loses the default route and every Building 1 route, Logistics still reaches its own gateway, and everything returns when the link comes back.
4. Remove `ip nat inside` from `Gi0/2` on the edge router. Logistics reaches Building 1 servers but not the internet, because traffic leaves untranslated with a private source address. Restore it and confirm the translation appears.
5. Remove `network 192.168.3.0 0.0.0.31 area 0` on the BLD2 router. Building 1 loses the Logistics route and replies stop.
6. Shut the transit interface between the core and the edge router. Confirm the default route leaves the core's table, then restore it and watch the neighbor rebuild.

Possible later upgrades: a second inter-building link (with OSPF cost to prefer one path) so Building 2 survives a cable cut, a second core switch and edge router with HSRP or VRRP, and a local ISP link in Building 2.

## Switch port plan

Port names follow Catalyst 9000-style numbering (`Gi1/0/x` access, `Gi1/1/x` uplinks). Rename them to match the model or simulator image you use.

### BLD1-CORE-01 (24-port)

| Ports | Connects |
|---|---|
| `Gi1/0/1-2` | Po1 to BLD1-ACC-01 (`Gi1/1/1-2`) |
| `Gi1/0/3-4` | Po2 to BLD1-ACC-02 (`Gi1/1/1-2`) |
| `Gi1/0/5-6` | Po3 to BLD1-ACC-03 (`Gi1/1/1-2`) |
| `Gi1/0/24` | Routed port to BLD1-RTR-01 `Gi0/1`, 10.10.0.34/30, OSPF area 0 |
| All SVIs | Default gateways for every VLAN (see Subnets), passive in OSPF |

### BLD1-ACC-01 (48-port, Mgmt 10.10.0.11)

Uplink `Po1`: `Gi1/1/1-2` to core `Gi1/0/1-2`, LACP trunk, native VLAN 999, allowed VLANs 10,20,30,70,80,90,99,100. Voice VLAN 70 on `Gi1/0/1-30`.

| Ports | VLAN | Connects |
|---|---|---|
| `Gi1/0/1-8` | 10 EXEC | 8 users |
| `Gi1/0/9-18` | 20 HR | 10 users |
| `Gi1/0/19-30` | 30 ACCT | 12 users |
| `Gi1/0/31-39` | 100 PRINTERS-IOT | 9 printers/IoT |
| `Gi1/0/40-47` | n/a | Unused: shutdown, VLAN 999 |
| `Gi1/0/48` | n/a | AP-01 trunk (native 99, allow 80,90,99) |

### BLD1-ACC-02 (48-port, Mgmt 10.10.0.12)

Uplink `Po2`: `Gi1/1/1-2` to core `Gi1/0/3-4`, LACP trunk, native VLAN 999, allowed VLANs 40,50,70,80,90,99,100. Voice VLAN 70 on `Gi1/0/1-34`.

| Ports | VLAN | Connects |
|---|---|---|
| `Gi1/0/1-14` | 40 OPS | 14 users |
| `Gi1/0/15-34` | 50 SALES | 20 users |
| `Gi1/0/35-43` | 100 PRINTERS-IOT | 9 printers/IoT |
| `Gi1/0/44-47` | n/a | Unused: shutdown, VLAN 999 |
| `Gi1/0/48` | n/a | AP-02 trunk (native 99, allow 80,90,99) |

### BLD1-ACC-03 (24-port, Mgmt 10.10.0.13)

Uplink `Po3`: `Gi1/1/1-2` to core `Gi1/0/5-6`, LACP trunk, native VLAN 999, allowed VLANs 60,70,99,110. Voice VLAN 70 on `Gi1/0/1-16`.

| Ports | VLAN | Connects |
|---|---|---|
| `Gi1/0/1-16` | 60 IT | 16 users |
| `Gi1/0/17-20` | 110 SERVERS | 4 servers |
| `Gi1/0/21-23` | n/a | Unused: shutdown, VLAN 999 |
| `Gi1/0/24` | 99 MGMT | UPS-01 (static 10.10.0.25) |

### BLD2-RTR-01 (router, 2 interfaces plus subinterfaces)

| Interface | Connects |
|---|---|
| `Gi0/0` | Inter-building link to BLD1-RTR-01 `Gi0/2`, 10.10.0.38/30, OSPF area 0 |
| `Gi0/1` | 802.1Q trunk to BLD2-ACC-01 `Gi1/0/24`, no IP address on the physical port |
| `Gi0/1.99` | VLAN 99 management subinterface, gateway 10.10.0.41/29 |
| `Gi0/1.120` | VLAN 120 LOGISTICS subinterface, gateway 192.168.3.1/27, DHCP server |

### BLD2-ACC-01 (24-port, Mgmt 10.10.0.42)

Uplink: `Gi1/0/24` to BLD2-RTR-01 `Gi0/1`, 802.1Q trunk, native VLAN 999, allowed VLANs 99,120. No voice VLAN (data only).

| Ports | VLAN | Connects |
|---|---|---|
| `Gi1/0/1-20` | 120 LOGISTICS | 20 users |
| `Gi1/0/21-23` | n/a | Unused: shutdown, VLAN 999 |
| `Gi1/0/24` | n/a | Trunk to BLD2-RTR-01 (native 999, allow 99,120) |

## Inter-VLAN policy (enforced with ACLs on the core)

| Source | Destination | Policy |
|---|---|---|
| Executive, Sales, Operations | SERVERS | Permit required services (DNS, DHCP, file, print) |
| Any VLAN except IT and Executive | HR and ACCT | Deny (sensitive data) |
| HR, ACCT | SERVERS | Permit required services |
| IT | All VLANs and MGMT | Permit (administration) |
| Everyone except IT | MGMT | Deny |
| STAFF-WIFI | SERVERS, internet | Permit. Deny to HR and ACCT |
| GUEST | Internet only | Deny all private ranges (`192.168.0.0/16`, `10.0.0.0/8`, `172.16.0.0/12`) |
| LOGISTICS (Building 2) | SERVERS, internet | Permit. Crosses the inter-building link; NAT on BLD1-RTR-01 |
| LOGISTICS (Building 2) | HR, ACCT, MGMT | Deny. Enforced twice: `LOGISTICS-IN` on BLD2-RTR-01 and the core ACLs |
| Department VLANs | PRINTERS-IOT | Permit print ports only |
| PRINTERS-IOT, VOICE | Other VLANs | Deny. Allow replies and voice servers only |
