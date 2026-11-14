# Project Log

## 2026-11-12
- Repo structure, README, and logical topology diagram added.

## 2026-11-13
- Scaled to 80 employees; re-sized every subnet with VLSM (192.168.0.0/16 hosts, 10.10.0.0/24 network devices).
- Added third access switch, per-switch port plan, and detailed topology diagram.
- Chose Cisco IOS CLI + Jinja2 templates as the configuration approach.
- Switched to dynamic routing: OSPF area 0 between the core switch and a new edge router (BR01-RTR-01); redrew diagram with device symbols.
- Added server addressing table, ACL examples, routing verification, and glossary (01-planning/glossary.md).
- Updated the step-by-step guide to match: VLSM sizing, OSPF, per-device configs, routing tests, glossary.
