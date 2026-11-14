# Network Infrastructure Design & Deployment Lab

A virtual branch-office network project covering the full deployment lifecycle: VLAN/IP design, switch and wireless configuration, staging, testing, troubleshooting, and as-built documentation.

> **Status:** In progress. Sections marked *(pending)* are filled in as each phase is completed.

> **Note:** This is a simulated environment built in Cisco Packet Tracer. No physical equipment was used. All device names, IP addresses, serial numbers, and asset tags are fictional.

![Logical topology](Diagrams/logical-topology.svg)

## Overview

This project simulates the rollout of a new 80-person branch office with six departments (Executive, HR, Accounting, Operations, Sales, and IT). I took the role of the deployment technician responsible for planning, staging, configuring, testing, and documenting the site's network infrastructure against a defined set of naming, labeling, security, and documentation standards.

The goal is to practice the work of a real infrastructure deployment, not just a working configuration: pre-deployment planning, standardized configs, evidence-based testing, troubleshooting, and a handoff package another technician could use to support the site.

## Skills demonstrated

- Ethernet, TCP/IP, switching, VLANs, IP addressing, and subnetting
- 802.1Q trunking, LACP/EtherChannel uplinks, inter-VLAN routing, and OSPF dynamic routing
- Switch baseline hardening: SSH-only management, port security, DHCP snooping, BPDU guard, unused-port shutdown, native VLAN change
- Wireless deployment with SSIDs mapped to VLANs
- Staging workflow: inventory, labeling, config templates, and checklists
- Configuration as code: Jinja2 templates and variables kept in Git
- Rack, patch panel, cabling, and UPS planning
- Test planning and evidence collection
- Structured troubleshooting and root-cause documentation
- Project planning, vendor and contractor coordination, and technical documentation

## Tools

| Purpose | Tool |
|---|---|
| Network simulation | Cisco Packet Tracer |
| Diagrams | draw.io (diagrams.net) |
| Inventory, port map, test matrix, BOM | Excel / Google Sheets |
| Config templating | Python, Jinja2 |
| Version control and documentation | Git, GitHub, Markdown |

## Network design

Addressing is allocated with variable length subnet mask from two pools: `192.168.0.0/16` for hosts (summarized as `192.168.0.0/22`) and `10.10.0.0/24` for network devices. Each subnet is sized from its department's headcount plus 25% growth and a gateway address. The method, DHCP conventions, routing design, per-switch port plan, and inter-VLAN policy are in [`01-planning/addressing-plan.md`](01-planning/addressing-plan.md).

**Topology:** one edge router, one Layer 3 core switch, three access switches (Executive/HR/Accounting, Operations/Sales, and IT/servers), and two wireless APs. Each access switch connects to the core with a two-link LACP port channel. The core and edge router exchange routes with OSPF (area 0) over a point-to-point transit link. Native VLAN 999 is unused and not routed.

**Host VLANs (192.168.0.0/16)**

| VLAN | Name | Users / hosts | Subnet | Usable |
|---|---|---|---|---|
| 10 | EXEC | 8 users | 192.168.2.192/28 | 14 |
| 20 | HR | 10 users | 192.168.2.208/28 | 14 |
| 30 | ACCT | 12 users | 192.168.2.64/27 | 30 |
| 40 | OPS | 14 users | 192.168.2.96/27 | 30 |
| 50 | SALES | 20 users | 192.168.2.128/27 | 30 |
| 60 | IT | 16 users | 192.168.2.0/26 | 62 |
| 70 | VOICE | 80 devices | 192.168.1.0/25 | 126 |
| 80 | STAFF-WIFI | 80 users | 192.168.0.0/24 | 254 |
| 90 | GUEST | 80 devices | 192.168.1.128/25 | 126 |
| 100 | PRINTERS-IOT | 18 devices | 192.168.2.160/27 | 30 |
| 110 | SERVERS | 4 devices | 192.168.2.224/29 | 6 |

**Network device addressing (10.10.0.0/24)**

| Segment | Subnet | Usable | Purpose |
|---|---|---|---|
| VLAN 99 MGMT | 10.10.0.0/27 | 30 | Switch, AP, and UPS management (gateway 10.10.0.1) |
| Transit | 10.10.0.32/30 | 2 | Edge router (10.10.0.33) to core (10.10.0.34), routed link running OSPF |
| WAN | 203.0.113.0/30 | 2 | ISP handoff (placeholder documentation range), router 203.0.113.2 |

**Devices**

| Device | Role | Management / transit IP |
|---|---|---|
| BR01-RTR-01 | Edge router: NAT, OSPF, default route to ISP | 10.10.0.33 (transit), 203.0.113.2 (WAN) |
| BR01-CORE-01 | Layer 3 core switch: DHCP, SVIs, inter-VLAN routing, OSPF | 10.10.0.1 (VLAN 99), 10.10.0.34 (transit) |
| BR01-ACC-01 | Access switch (Executive, HR, Accounting, Printers/IoT) | 10.10.0.11 |
| BR01-ACC-02 | Access switch (Operations, Sales, Printers/IoT) | 10.10.0.12 |
| BR01-ACC-03 | Access switch (IT, Servers, UPS) | 10.10.0.13 |
| BR01-AP-01 / AP-02 | Wireless APs (Staff and Guest SSIDs) | 10.10.0.21 / 10.10.0.22 |
| BR01-UPS-01 | UPS network card | 10.10.0.25 |

**Standards**

- Device naming: `SITE-ROLE-NN` (for example `BR01-ACC-01`)
- Cable and port labels: `SITE-IDF#-PP#-PORT` (for example `BR01-IDF1-PP1-14`)
- Patch cable colors assigned by function
- Security baseline applied to every device from one config template

## Technologies and configuration approach

- **Platform:** Cisco Packet Tracer using Cisco IOS-style CLI. The same design can be rebuilt in GNS3 or EVE-NG with real IOS images.
- **Routing:** OSPFv2, single area (area 0), between the core switch and the edge router. Point-to-point network type, MD5 authentication, passive interfaces on every user-facing SVI, and a default route originated by the edge router. Inter-VLAN routing happens on the core through SVIs.
- **How devices are configured:** the Cisco IOS command line, first over console, then over SSH on the management VLAN. Configs are written as Jinja2 templates with per-device variables stored in the repo, rendered per device by a short Python script, applied during staging, then verified with `show` commands and committed.
- **Automation (optional, later):** Netmiko or Ansible (`cisco.ios` collection) can push the rendered configs to GNS3 or EVE-NG devices. Packet Tracer devices cannot be driven from the host, so configs are pasted there.
- **Protocols and features:** 802.1Q VLAN trunking, LACP port channels, Rapid PVST+, OSPF, DHCP on the core, inter-VLAN ACLs, NAT/PAT, SSH v2, port security, DHCP snooping, BPDU guard, NTP, and syslog.

## Repository structure

```
network-infrastructure-design-deployment/
├── README.md
├── project-log.md           Dated notes on what was done each session
├── .gitignore
├── 01-planning/
│   ├── requirements.md
│   ├── addressing-plan.md      Addressing, OSPF routing design, switch port plan, ACL policy
│   ├── glossary.md
│   ├── ip-vlan-plan.xlsx
│   ├── ip-vlan-plan.csv
│   └── standards.md
├── 02-pre-deployment/
│   ├── site-survey.md
│   ├── bill-of-materials.xlsx
│   ├── inventory.xlsx
│   ├── inventory.csv
│   ├── ups-sizing.md
│   ├── project-plan.xlsx
│   ├── staging-checklist.md
│   └── installation-checklist.md
├── 03-configs/
│   ├── network-infrastructure-design-deployment.pkt
│   ├── templates/           Jinja2 templates (base, access switch, core)
│   ├── variables/           Per-device variables (YAML or CSV)
│   ├── render_configs.py    Renders one config per device
│   ├── BR01-CORE-01.txt
│   ├── BR01-ACC-01.txt
│   ├── BR01-ACC-02.txt
│   ├── BR01-ACC-03.txt
│   └── wireless-design-note.md
├── 04-testing/
│   ├── test-matrix.xlsx
│   └── evidence/
├── 05-troubleshooting/
│   ├── 01-wrong-access-vlan.md
│   ├── 02-trunk-allowed-vlan-mismatch.md
│   └── ...
├── 06-coordination/
│   ├── contractor-scope-email.md
│   ├── facilities-request.md
│   ├── vendor-rma-email.md
│   ├── cutover-notice.md
│   └── status-update-template.md
├── 07-handoff/
│   ├── as-built-notes.md
│   ├── config-backups/
│   └── closeout-checklist.md
└── diagrams/
    ├── logical-topology.svg
    ├── logical-topology.drawio
    ├── rack-elevation.png
    └── patch-panel-map.png
```

File names are suggestions. Match them to what you actually produce and keep this tree current.

## Project phases

| Phase | Focus | Folder | Status |
|---|---|---|---|
| 0 | Repo and tool setup | root | Complete |
| 1 | Requirements, IP/VLAN plan, standards, logical diagram | `01-planning/` | In progress |
| 2 | Site survey, BOM, inventory, rack elevation, UPS sizing, project plan, checklists | `02-pre-deployment/` | Pending |
| 3 | Build the virtual topology | `03-configs/` | Pending |
| 4 | Config template and device staging | `03-configs/` | Pending |
| 5 | Wireless configuration | `03-configs/` | Pending |
| 6 | Testing | `04-testing/` | Pending |
| 7 | Troubleshooting log | `05-troubleshooting/` | Pending |
| 8 | Coordination documents | `06-coordination/` | Pending |
| 9 | Handoff package | `07-handoff/` | Pending |
| 10 | Final README, release, and publish | root | Pending |

## Testing summary *(pending)*

Results are added after Phase 6, for example: "XX of XX tests passed on the first run; YY required fixes (see the troubleshooting log)."

## Troubleshooting highlights *(pending)*

| # | Symptom | Root cause | Fix |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## How to reproduce *(pending)*

1. Install Cisco Packet Tracer.
2. Open `03-configs/network-infrastructure-design-deployment.pkt`.
3. Review the IP/VLAN plan in `01-planning/` and the port map in `diagrams/`.
4. To rebuild from scratch, apply `03-configs/base-template.txt` to each device, replacing the `{{PLACEHOLDERS}}` with that device's values.
5. Run the checks in `04-testing/test-matrix.xlsx` and compare against the evidence folder.

All credentials in this repository are placeholders.

## Possible improvements

- Generate device configs from a variables spreadsheet with Python and Jinja2
- Add a second core switch and edge router with HSRP/VRRP for first-hop redundancy
- Add centralized logging and SNMP monitoring
- Rebuild the topology in GNS3 or EVE-NG with real switch images
- Add 802.1X port authentication

## Glossary

Key terms used in this project. The full list is in [`01-planning/glossary.md`](01-planning/glossary.md).

| Term | Meaning |
|---|---|
| **BR01** | Branch 01, the site code at the start of every device name |
| **VLAN** | A separate broadcast domain on shared switches, one per department |
| **SVI** | Switched Virtual Interface: a virtual Layer 3 interface that acts as a VLAN's gateway |
| **VLSM** | Subnetting where each subnet gets the prefix its host count needs |
| **Trunk (802.1Q)** | A link that carries several VLANs, each frame tagged |
| **LACP** | Bundles several links into one logical port channel with failover |
| **OSPF** | The dynamic routing protocol used between the core and the edge router |
| **Passive interface** | An interface that advertises its network but sends no routing messages |
| **PAT** | NAT overload: many private hosts share one public address |
| **ACL** | A permit/deny rule list that filters traffic |
| **Staging** | Configuring, labeling, and testing equipment before deployment |

## Author

**Terry Atong Taku**
[www.linkedin.com/in/terry-taku]

---

*Learning project built in a simulated environment for portfolio purposes.*
