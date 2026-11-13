# Network Infrastructure Design & Deployment Lab

A virtual branch-office network project covering the full deployment lifecycle: VLAN/IP design, switch and wireless configuration, staging, testing, troubleshooting, and as-built documentation.

> **Status:** In progress. Sections marked *(pending)* are filled in as each phase is completed.

> **Note:** This is a simulated environment built in Cisco Packet Tracer. No physical equipment was used. All device names, IP addresses, serial numbers, and asset tags are fictional.

![Logical topology](diagrams/logical-topology.svg)

## Overview

This project simulates the rollout of a new 40-person branch office. I took the role of the deployment technician responsible for planning, staging, configuring, testing, and documenting the site's network infrastructure against a defined set of naming, labeling, security, and documentation standards.

The goal is to practice the work of a real infrastructure deployment, not just a working configuration: pre-deployment planning, standardized configs, evidence-based testing, troubleshooting, and a handoff package another technician could use to support the site.

## Skills demonstrated

- Ethernet, TCP/IP, switching, VLANs, IP addressing, and subnetting
- 802.1Q trunking, LACP/EtherChannel uplinks, and inter-VLAN routing
- Switch baseline hardening: SSH-only management, port security, DHCP snooping, BPDU guard, unused-port shutdown, native VLAN change
- Wireless deployment with SSIDs mapped to VLANs
- Staging workflow: inventory, labeling, config templates, and checklists
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
| Version control and documentation | Git, GitHub, Markdown |

## Network design

**Topology:** one firewall/router, one core (Layer 3) switch, two access switches, and one wireless AP. Access-to-core links are LACP port channels. Native VLAN 999 is unused and not routed.

| VLAN | Name | Subnet | Purpose |
|---|---|---|---|
| 10 | USERS | 10.50.10.0/24 | Staff workstations |
| 20 | VOICE | 10.50.20.0/24 | IP phones |
| 30 | SERVERS | 10.50.30.0/26 | Local servers |
| 40 | PRINTERS-IOT | 10.50.40.0/26 | Printers and badge readers |
| 50 | GUEST | 10.50.50.0/24 | Guest Wi-Fi (isolated) |
| 99 | MGMT | 10.50.99.0/26 | Switch and AP management |
| 999 | NATIVE-BLACKHOLE | none | Unused native VLAN |
| n/a | TRANSIT | 10.50.0.0/30 | Core to firewall link |

**Devices**

| Device | Role | Management IP |
|---|---|---|
| BR01-FW-01 | Firewall / router | 10.50.0.1 (transit) |
| BR01-CORE-01 | Core / distribution switch | 10.50.99.2 |
| BR01-ACC-01 | Access switch | 10.50.99.11 |
| BR01-ACC-02 | Access switch | 10.50.99.12 |
| BR01-AP-01 | Wireless AP | 10.50.99.21 |

Update these tables if your final addressing changes.

**Standards**

- Device naming: `SITE-ROLE-NN` (for example `BR01-ACC-01`)
- Cable and port labels: `SITE-IDF#-PP#-PORT` (for example `BR01-IDF1-PP1-14`)
- Patch cable colors assigned by function
- Security baseline applied to every device from one config template

## Repository structure

```
network-infrastructure-design-deployment/
├── README.md
├── project-log.md           Dated notes on what was done each session
├── .gitignore
├── 01-planning/
│   ├── requirements.md
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
│   ├── base-template.txt
│   ├── BR01-CORE-01.txt
│   ├── BR01-ACC-01.txt
│   ├── BR01-ACC-02.txt
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
- Add a second firewall and uplink for redundancy
- Add centralized logging and SNMP monitoring
- Rebuild the topology in GNS3 or EVE-NG with real switch images
- Add 802.1X port authentication

## Author

**[Your Name]**
[LinkedIn URL]

---

*Learning project built in a simulated environment for portfolio purposes.*
