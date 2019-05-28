"""
Factory function for creating aionet classes
"""
from aionet.vendors.devices import AristaEOS
from aionet.vendors.devices import ArubaAOS6, ArubaAOS8
from aionet.vendors.devices import CiscoASA, CiscoIOS, CiscoIOSXR, CiscoNXOS
from aionet.vendors.devices import FujitsuSwitch
from aionet.vendors.devices import HPComware, HPComwareLimited
from aionet.vendors.devices import JuniperJunOS
from aionet.vendors.devices import MikrotikRouterOS
from aionet.vendors.devices import Terminal
from aionet.vendors.devices import UbiquityEdgeSwitch

# @formatter:off
# The keys of this dictionary are the supported device_types
CLASS_MAPPER = {
    "arista_eos": AristaEOS,
    "aruba_aos_6": ArubaAOS6,
    "aruba_aos_8": ArubaAOS8,
    "cisco_asa": CiscoASA,
    "cisco_ios": CiscoIOS,
    "cisco_ios_xe": CiscoIOS,
    "cisco_ios_xr": CiscoIOSXR,
    "cisco_nxos": CiscoNXOS,
    "fujitsu_switch": FujitsuSwitch,
    "hp_comware": HPComware,
    "hp_comware_limited": HPComwareLimited,
    "juniper_junos": JuniperJunOS,
    "mikrotik_routeros": MikrotikRouterOS,
    "ubiquity_edge": UbiquityEdgeSwitch,
    "terminal": Terminal,
}

# @formatter:on

platforms = list(CLASS_MAPPER.keys())
platforms.sort()
platforms_str = u"\n".join(platforms)


def create(*args, **kwargs):
    """Factory function selects the proper class and creates object based on device_type"""
    if kwargs["device_type"] not in platforms:
        raise ValueError(
            "Unsupported device_type: "
            "currently supported platforms are: {0}".format(platforms_str)
        )
    connection_class = CLASS_MAPPER[kwargs["device_type"]]
    return connection_class(*args, **kwargs)
