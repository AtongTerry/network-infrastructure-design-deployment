# Troubleshooting Log

Issues found while building and testing the lab. Each entry follows the same format: symptom, diagnosis, root cause, fix, verification, lesson.

## Index
| # | Issue | Device(s) | Status |
|---|---|---|---|
| 1 | DHCP failed on VLAN 10 only | ACC-01..05, core | Resolved |
| 2 | Building 1 hosts got no DHCP address while Building 2 did | Core, access switches | Resolved |
| 3 | No default route in the network, 8.8.8.8 unreachable | BLD1-RTR-01, ISP-RTR | Resolved |
| 4 | `crypto key generate rsa modulus 2048` rejected | All IOS devices | Resolved (workaround) |
| 5 | `ip dhcp snooping trust` rejected on a Port-channel | Access switches | Resolved |
| 6 | `deny ip any any log` rejected | Core, BLD2-RTR-01 | Resolved |
| 7 | AP-PT cannot tag a VLAN per SSID | BLD1-AP-01/02 | Resolved (design change) |

---

## 1. DHCP failed on VLAN 10 only
- **Symptom:** After DHCP snooping was disabled on most access switches, hosts on every VLAN got addresses except VLAN 10 (EXEC) on BLD1-ACC-01.
- **Diagnosis:** A static address on a VLAN 10 PC could ping the Logistics PC, so routing and the trunk were fine. In Simulation mode the DHCP discover from the VLAN 10 PC reached the core and the DHCP reply never made it back. `show ip dhcp pool EXEC` showed the pool healthy, so exhaustion was ruled out, and `show run | include excluded` showed no bad excluded range.
- **Root cause:** DHCP snooping was still enabled on BLD1-ACC-01. It cannot trust a Port-channel in Packet Tracer, and trust on the physical member ports had no effect, so snooping dropped the core's DHCP replies as untrusted server traffic.
- **Fix:** Removed the snooping commands from ACC-01 (and the other Building 1 switches). The commands are kept in the config as comments for real hardware.
- **Verification:** A PC on VLAN 10 received a 192.168.2.19x address and `show ip dhcp binding` on the core listed the lease.
- **Lesson:** When one VLAN fails and the rest work, compare the switch configuration for that VLAN's path before blaming the pool. Early guesses (pool exhaustion) cost time; Simulation mode pointed at the real cause.

## 2. Building 1 hosts got no DHCP address while Building 2 did
- **Symptom:** Logistics PCs in Building 2 leased addresses from the core, but Building 1 hosts did not.
- **Diagnosis:** The Building 2 PCs only worked because of the relay (`ip helper-address 10.10.0.1`). That showed the core's pools were working, so the Building 1 problem was on the access side (see issue 1).
- **Root cause:** Same as issue 1 (snooping on the Port-channel uplinks). The design itself, one central DHCP server on the core with a relay in Building 2, was correct.
- **Fix:** One central DHCP server on BLD1-CORE-01 with a LOGISTICS pool and the helper address on BLD2-RTR-01's `.120` subinterface. Snooping was removed from the Building 1 switches.
- **Verification:** Hosts on every VLAN in both buildings receive addresses from the core.
- **Lesson:** Design DHCP once, centrally, and use `ip helper-address` on every routed gateway that is not on the DHCP server. A second DHCP server would have added a second thing to maintain.

## 3. No default route, 8.8.8.8 unreachable
- **Symptom:** Staff and guest laptops got "destination unreachable" pinging 8.8.8.8. The core's routing table showed no gateway of last resort.
- **Diagnosis:** `show ip ospf neighbor` on the core showed the neighbor in FULL state and the core had Building 2 routes, so OSPF itself was fine. `show ip int brief` on BLD1-RTR-01 showed Gi0/0/0 `down/down`, even after `no shutdown`.
- **Root cause:** The WAN link between BLD1-RTR-01 and ISP-RTR was physically down in Packet Tracer. With Gi0/0/0 down, the static default route was never installed, so `default-information originate` had nothing to advertise.
- **Fix:** Deleted the cable on Gi0/0/0 and re-added it. The interface came up, the static route installed, and the core learned `O*E2 0.0.0.0/0`.
- **Verification:** The core's route table shows `O*E2 0.0.0.0/0`, and staff and guest laptops ping 8.8.8.8.
- **Lesson:** If `default-information originate` is configured but no default route shows up in OSPF, check that the WAN interface is up before looking at OSPF.

## 4. `crypto key generate rsa modulus 2048` rejected
- **Symptom:** `% Invalid input detected` on the modulus keyword.
- **Root cause:** This Packet Tracer IOS version does not accept the `modulus` keyword.
- **Fix:** Run `crypto key generate rsa` and enter 2048 when prompted. The key step is documented as a manual step rather than included in the pasted configs.
- **Lesson:** Pasted configs must be tested against the simulator's IOS, not just against real IOS syntax.

## 5. `ip dhcp snooping trust` rejected on a Port-channel
- **Symptom:** `% Invalid input detected` when trusting `Port-channel1`.
- **Root cause:** Packet Tracer does not accept trust on a Port-channel. Applying it to the physical member ports was accepted but did not take effect (see issue 1).
- **Fix:** Snooping is documented for real hardware and disabled in the lab on Building 1. It remains active on BLD2-ACC-01, which has a single uplink (Gi0/1) that can be trusted directly.
- **Lesson:** On real switches, trust goes on the Port-channel interface. Where the simulator cannot do that, document the real-world configuration and say why the lab differs.

## 6. `deny ip any any log` rejected
- **Symptom:** `% Invalid input detected` on the `log` keyword in the extended ACLs.
- **Fix:** Removed `log`. The final `deny ip any any` entries are kept.
- **Lesson:** Logging for denied traffic is a real-hardware improvement to note in the hardening section.

## 7. AP-PT cannot tag a VLAN per SSID
- **Symptom:** The standalone Access Point-PT has no per-SSID VLAN setting, so one AP cannot put staff and guest users in different VLANs.
- **Fix:** One AP per SSID, each on an access port in its VLAN: BLD1-AP-01 (BLD1-Staff, VLAN 80, ACC-01 Fa0/24) and BLD1-AP-02 (BLD1-Guest, VLAN 90, ACC-05 Fa0/24). See `wireless-design-note.md`.
- **Lesson:** Production design is one AP with two SSIDs on a trunk. The lab design keeps the same VLAN separation within the simulator's limits.

