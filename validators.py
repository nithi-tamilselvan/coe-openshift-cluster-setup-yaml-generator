import ipaddress
import re
from collections import Counter


class ValidationError(Exception):
    pass


# -------------------------
# MAC Validation
# -------------------------
def validate_mac_format(mac):
    pattern = r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$"
    if not re.match(pattern, mac):
        raise ValidationError(f"Invalid MAC address format: {mac}")


def validate_duplicate_macs(nodes):
    macs = [node["mac"] for node in nodes]

    duplicates = [mac for mac, count in Counter(macs).items() if count > 1]

    if duplicates:
        raise ValidationError(f"Duplicate MAC addresses detected: {duplicates}")


# -------------------------
# IP Validation Helpers
# -------------------------
def collect_all_ips(nodes):
    """Collect IPv4/IPv6 from mgmt + storage networks"""
    ips = []

    for node in nodes:
        hostname = node.get("hostname", "UNKNOWN")

        # Mgmt IPs
        mgmt = node.get("mgmtnetworkIPs", {})
        if mgmt.get("ipv4"):
            ips.append(mgmt["ipv4"])
        if mgmt.get("ipv6"):
            ips.append(mgmt["ipv6"])

        # Storage IPs
        storage = node.get("storageIPs", {})
        for vlan, ip in storage.items():
            if ip:
                ips.append(ip)

    return ips


def validate_duplicate_ips(nodes):
    ips = collect_all_ips(nodes)

    print("\nDEBUG → Collected IPs:")
    for ip in ips:
        print(ip)

    duplicates = [ip for ip, count in Counter(ips).items() if count > 1]

    if duplicates:
        raise ValidationError(
            f"Duplicate IP addresses detected: {duplicates}"
        )


import ipaddress

def validate_ip_format(nodes):
    for node in nodes:
        hostname = node.get("hostname", "UNKNOWN")

        # ---- Management IPs ----
        mgmt = node.get("mgmtnetworkIPs", {})

        ipv4 = mgmt.get("ipv4")
        if ipv4:
            try:
                ipaddress.IPv4Address(ipv4)
            except ipaddress.AddressValueError:
                raise ValidationError(f"[{hostname}] Invalid IPv4: {ipv4}")

        ipv6 = mgmt.get("ipv6")
        if ipv6:
            try:
                ipaddress.IPv6Address(ipv6)
            except ipaddress.AddressValueError:
                raise ValidationError(f"[{hostname}] Invalid IPv6: {ipv6}")

        # ---- Storage VLAN IPs ----
        storage = node.get("storageIPs", {})

        for vlan, ip in storage.items():
            if not ip:
                continue  # Skip empty values safely

            try:
                ipaddress.IPv4Address(ip)
            except ipaddress.AddressValueError:
                raise ValidationError(
                    f"[{hostname}] Invalid Storage IP (VLAN {vlan}): {ip}"
                )


# -------------------------
# Master Count Validation
# -------------------------
def validate_master_count(nodes):
    masters = [n for n in nodes if n["role"] == "master"]

    if len(masters) < 3:
        raise ValidationError("Minimum 3 master nodes required")

    if len(masters) % 2 == 0:
        raise ValidationError("Master node count must be odd")


# -------------------------
# CIDR Validation
# -------------------------
def validate_cidr_overlap(networks):
    cidrs = [ipaddress.ip_network(c) for c in networks]

    for i in range(len(cidrs)):
        for j in range(i + 1, len(cidrs)):
            if cidrs[i].overlaps(cidrs[j]):
                raise ValidationError(
                    f"CIDR overlap detected: {cidrs[i]} ↔ {cidrs[j]}"
                )


# -------------------------
# VIP Validation
# -------------------------
def validate_vip_in_machine_network(vips, machine_networks):
    machine_nets = [ipaddress.ip_network(net) for net in machine_networks]

    for vip in vips:
        ip_obj = ipaddress.ip_address(vip)

        if not any(ip_obj in net for net in machine_nets):
            raise ValidationError(
                f"VIP {vip} NOT inside machineNetwork {machine_networks}"
            )


# -------------------------
# Node-Level Validation
# -------------------------
def validate_nodes(nodes):
    validate_ip_format(nodes)
    validate_duplicate_ips(nodes)
    validate_master_count(nodes)
    validate_duplicate_macs(nodes)

    for node in nodes:
        validate_mac_format(node["mac"])


# -------------------------
# Cluster-Level Validation
# -------------------------
def validate_cluster(networking, nodes):
    print("Running validations...")

    validate_nodes(nodes)

    cidrs_to_check = [
        networking["machineNetworkIPv4"],
        networking["clusterNetworkIPv4"],
        networking["serviceNetworkIPv4"],
    ]

    if networking.get("machineNetworkIPv6"):
        cidrs_to_check.append(networking["machineNetworkIPv6"])
    if networking.get("clusterNetworkIPv6"):
        cidrs_to_check.append(networking["clusterNetworkIPv6"])
    if networking.get("serviceNetworkIPv6"):
        cidrs_to_check.append(networking["serviceNetworkIPv6"])

    validate_cidr_overlap(cidrs_to_check)

    vips = [
        networking["apiVIPv4"],
        networking["ingressVIPv4"],
    ]

    if networking.get("apiVIPv6"):
        vips.append(networking["apiVIPv6"])
    if networking.get("ingressVIPv6"):
        vips.append(networking["ingressVIPv6"])

    machine_networks = [networking["machineNetworkIPv4"]]

    if networking.get("machineNetworkIPv6"):
        machine_networks.append(networking["machineNetworkIPv6"])

    validate_vip_in_machine_network(vips, machine_networks)

    print("All validations passed ✅")