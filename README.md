# OpenShift YAML Generator

Automates generation of:

- `install-config.yaml`
- `agent-config.yaml`

from cluster-level-environment-specific JSON inputs.

Designed for **OpenShift Agent-Based Installation** with support for:

✅ Dual-stack (IPv4 + IPv6)  
✅ Multiple environments (DEV / QA / PROD)  
✅ Strong validations  

---

## 📂 Project Structure

    dellcoe-openshift-yaml-generator/
        │
        ├── cluster-datasource/
        │ ├── pde.json
        │ └── ncw.json
        │
        ├── jinja2-templates/
        │ ├── install-config.yaml.j2
        │ └── agent-config.yaml.j2
        │
        ├── generated-yaml-output/
        │ └── (auto-generated)
        │
        ├── render_yaml.py
        ├── validators.py
        ├── requirements.txt
        └── README.md

---

## ⚙️ Requirements

Install dependencies:

  ```bash
  python -m venv myenv
  myenv\Scripts\activate.bat

  pip install -r requirements.txt
  ```

---

## 🚀 Usage

Run generator with environment JSON:

```bash
python render_yaml.py cluster-datasource/pde.json
```

Output:
    
```bash
generated-yaml-output/datacenter-install-config.yaml
generated-yaml-output/datacenter-agent-config.yaml

Example :
generated-yaml-output\pde-agent-config.yaml
generated-yaml-output\pde-install-config.yaml
```

---

##  Input JSON Format - cluster-datasource\pde.json

    {
    "cluster": {
        "name": "ctc-pde-hub-c1",
        "baseDomain": "corp.chartercom.com"
    },
    "networking": {
        "machineNetworkIPv4": "10.24.34.0/24",
        "machineNetworkIPv6": "2001:1998:3b01:201::/64",
        "clusterNetworkIPv4": "10.128.0.0/16",
        "clusterNetworkHostPrefixIPv4": 23,
        "clusterNetworkIPv6": "fd01::/48",
        "clusterNetworkHostPrefixIPv6": 64,
        "serviceNetworkIPv4": "172.30.0.0/16",
        "serviceNetworkIPv6": "fd02::/112",
        "apiVIPv4": "10.24.34.11",
        "apiVIPv6": "2001:1998:3b01:201::11",
        "ingressVIPv4": "10.24.34.12",
        "ingressVIPv6": "2001:1998:3b01:201::12",
        "gatewayIPv4": "10.24.34.1",
        "gatewayIPv6": "2001:1998:3b01:201::1",
        "vlanId": 201,
        "mtu": 9000,
        "dnsServers": [
            "142.136.252.87",
            "142.136.253.87"
        ],
        "ntpSources": [
            "142.136.130.195",
            "bluentp.inf.charter.com",
            "2001:1998:3003:2::1"
        ]
    },
    "nodes": [
        {
            "hostname": "CTCLRDAZ01HC001",
            "role": "master",
            "mac": "AA:BB:CC:DD:EE:01",
            "mgmtnetworkIPs": {
                "ipv4": "10.24.34.10",
                "ipv6": "2001:1998:3b01:201::13"
            },
            "storageIPs": {
                "503": "10.3.121.13",
                "504": "10.3.123.13"
            },
            "rootDeviceHints": {
                "deviceName": "/dev/sda",
                "serialNumber": "",
                "vendor": "Dell",
                "minSizeGigabytes": "",
                "wwn": "",
                "rotational": false
            }
        },
        {
            "hostname": "CTCLRDAZ01HC002",
            "role": "master",
            "mac": "AA:BB:CC:DD:EE:02",
            "mgmtnetworkIPs": {
                "ipv4": "10.24.34.14",
                "ipv6": "2001:1998:3b01:201::14"
            },
            "storageIPs": {
                "503": "10.3.121.14",
                "504": "10.3.123.14"
            },
            "rootDeviceHints": {
                "deviceName": "/dev/sda",
                "serialNumber": "",
                "vendor": "Dell",
                "minSizeGigabytes": "",
                "wwn": "",
                "rotational": false
            }       
        },
        {
            "hostname": "CTCLRDAZ01HC003",
            "role": "master",
            "mac": "AA:BB:CC:DD:EE:03",
            "mgmtnetworkIPs": {
                "ipv4": "10.24.34.15",
                "ipv6": "2001:1998:3b01:201::15"
            },
            "storageIPs": {
                "503": "10.3.121.15",
                "504": "10.3.123.15"
            },
            "rootDeviceHints": {
                "deviceName": "/dev/sda",
                "serialNumber": "",
                "vendor": "Dell",
                "minSizeGigabytes": "",
                "wwn": "",
                "rotational": false
            }
        },
        {
            "hostname": "CTCLRDAZ01HI001",
            "role": "infra",
            "mac": "AA:BB:CC:DD:EE:04",
            "mgmtnetworkIPs": {
                "ipv4": "10.24.34.16",
                "ipv6": "2001:1998:3b01:201::16"
            },
            "storageIPs": {
                "503": "10.3.121.16",
                "504": "10.3.123.16"
            },
            "rootDeviceHints": {
                "deviceName": "/dev/sda",
                "serialNumber": "",
                "vendor": "Dell",
                "minSizeGigabytes": "",
                "wwn": "",
                "rotational": false
            }
        },
        {
            "hostname": "CTCLRDAZ01HI002",
            "role": "infra",
            "mac": "AA:BB:CC:DD:EE:05",
            "mgmtnetworkIPs": {
                "ipv4": "10.24.34.17",
                "ipv6": "2001:1998:3b01:201::17"
            },
            "storageIPs": {
                "503": "10.3.121.17",
                "504": "10.3.123.17"
            },
            "rootDeviceHints": {
                "deviceName": "/dev/sda",
                "serialNumber": "",
                "vendor": "Dell",
                "minSizeGigabytes": "",
                "wwn": "",
                "rotational": false
            }
        },
        {
            "hostname": "CTCLRDAZ01HI003",
            "role": "infra",
            "mac": "AA:BB:CC:DD:EE:06",
            "mgmtnetworkIPs": {
                "ipv4": "10.24.34.18",
                "ipv6": "2001:1998:3b01:201::18"
            },
            "storageIPs": {
                "503": "10.3.121.18",
                "504": "10.3.123.18"
            },
            "rootDeviceHints": {
                "deviceName": "/dev/sda",
                "serialNumber": "",
                "vendor": "Dell",
                "minSizeGigabytes": "",
                "wwn": "",
                "rotational": false
            }
        }
    ]
}

---

## ✅ Validations Performed

The generator validates before rendering YAML:

    ✔ Duplicate MACs across ALL nodes
    ✔ Duplicate IPv4 (mgmt + storage)
    ✔ Duplicate IPv6
    ✔ Invalid MAC format
    ✔ Invalid IPv4/IPv6 format
    ✔ CIDR overlaps
    ✔ VIP outside subnet
    ✔ Even master count