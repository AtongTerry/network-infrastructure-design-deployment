# Wireless Design Note

## Summary
Two access points in Building 1 provide wireless: one for staff, one for guests. Each SSID maps to its own VLAN, and all addressing comes from the central DHCP server on BLD1-CORE-01.

| AP | SSID | VLAN | Subnet | Switch port | Port mode |
|---|---|---|---|---|---|
| BLD1-AP-01 | BLD1-Staff | 80 (STAFF-WIFI) | 192.168.0.0/24 | BLD1-ACC-01 Fa0/24 | access, VLAN 80 |
| BLD1-AP-02 | BLD1-Guest | 90 (GUEST) | 192.168.1.128/25 | BLD1-ACC-05 Fa0/24 | access, VLAN 90 |

Planned AP management addresses (documented only, because the Packet Tracer AP-PT has no management IP): 10.10.0.21 (AP-01) and 10.10.0.22 (AP-02) on VLAN 99.

## Design decision: one SSID per AP
A production AP carries several SSIDs and tags each one onto a VLAN over a trunk port. The Packet Tracer AP-PT cannot tag VLANs, so the lab uses one AP per SSID, each on an access port in its VLAN. The VLAN separation, DHCP and policy behave the same, and the access-port choice is the only simplification.

On real hardware: a single AP, a trunk port allowing VLANs 80, 90 and 99, and two SSIDs mapped to VLANs 80 and 90.

## Security controls
- **Isolation by VLAN:** staff and guest traffic never share a broadcast domain.
- **Guest ACL (GUEST-IN, applied inbound on the VLAN 90 SVI):** permits DHCP and DNS, then denies the whole 192.168.0.0/16, 10.0.0.0/8 and 172.16.0.0/12 ranges, so guests cannot reach servers, staff, printers or management. All other traffic (internet) is allowed.
- **Guest DNS:** guests receive 1.1.1.1 rather than the internal DNS server.
- **Staff Wi-Fi** uses WPA2-PSK. Passphrases are kept out of the repo.
- **Management:** APs sit outside the user VLANs; the plan places them on MGMT (VLAN 99).

## DHCP
Central DHCP on BLD1-CORE-01 serves pools STAFF-WIFI and GUEST. The APs are layer 2 only, so no relay is needed in Building 1.

## Test results
| Test | Expected | Result |
|---|---|---|
| Staff laptop joins BLD1-Staff and gets a 192.168.0.x address | Pass | Pass |
| Guest laptop joins BLD1-Guest and gets a 192.168.1.129+ address | Pass | Pass |
| Guest laptop pings SERVERS (192.168.2.226) | Blocked | Blocked (request times out) |
| Guest laptop pings 8.8.8.8 | Allowed by ACL | Pass (after fixing the WAN link, see Troubleshooting) |

## Lessons learned
- DHCP snooping on port-channel uplinks dropped the core's DHCP replies in Packet Tracer, so it is documented for real hardware and left off in the lab.
- AP-PT limits drove the one-SSID-per-AP design.
