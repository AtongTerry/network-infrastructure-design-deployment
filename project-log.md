# Project Log

## 2026-11-12
- Repo structure, README, and logical topology diagram added.

## 2026-11-13
- Scaled to 80 employees; re-sized every subnet with VLSM (192.168.0.0/16 hosts, 10.10.0.0/24 network devices).
- Added third access switch, per-switch port plan, and detailed topology diagram.
- Chose Cisco IOS CLI + Jinja2 templates as the configuration approach.
- Switched to dynamic routing: OSPF area 0 between the core switch and a new edge router (BR01-RTR-01); redrew diagram with device symbols.
- Added server addressing table, ACL examples, routing verification, and glossary (Planning/glossary.md).
- Updated the step-by-step guide to match: VLSM sizing, OSPF, per-device configs, routing tests, glossary.

## 2026-11-13 (later)
- Added Building 2: one router (BLD2-RTR-01) and one access switch serving one department (Logistics, 20 users, 192.168.3.0/27).
- Renamed Building 1 devices from BR01-* to BLD1-*.
- Added a routed inter-building link (10.10.0.36/30) running OSPF area 0 with MD5 auth; Building 2 reaches the internet through NAT on BLD1-RTR-01.
- Building 2 uses router-on-a-stick (802.1Q subinterfaces), DHCP on the router, and a LOGISTICS-IN ACL.
- Updated the addressing plan, routing design and tests, CSV, glossary, README, and topology diagram.

## 2026-11-15
- Packet Tracer has no 48-port switch, so the two 48-port access switches were split into 24-port switches. Building 1 now has five access switches: ACC-01 (Executive, HR, AP-01), ACC-02 (Accounting), ACC-03 (IT, Servers, UPS), ACC-04 (Operations), ACC-05 (Sales, AP-02).
- Printers/IoT (18 devices) are spread across ACC-01, 02, 04 and 05. New port channels Po4 and Po5 on core Gi1/0/7-10; new management addresses 10.10.0.14 and 10.10.0.15.
- Updated the addressing plan, CSV, README, glossary, and topology diagram.
- Matched the design to the Packet Tracer models: ISR4331 routers (Gi0/0/0-2), 3560-24PS L3 core (Fa0/1-24, Gi0/1-2), 2960-24TT access switches (Fa0/x hosts, Gi0/1-2 uplinks).
- The core has only two Gigabit ports, so the five port channels use core Fast Ethernet ports (Fa0/1-10) and the access switches' Gi0/1-2 uplinks; the core-to-edge-router link moved to core Gi0/1 (Gi0/0/1 on the router).
- Added `switchport trunk encapsulation dot1q` on the core trunks (required on the 3560) and `no shutdown` on all router interfaces.
- BLD2-ACC-01 now uses Fa0/1-20 for hosts and Gi0/1 as the trunk to the router.
