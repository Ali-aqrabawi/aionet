from aionet.vendors.devices.arista import AristaEOS
from aionet.vendors.devices.aruba import ArubaAOS8, ArubaAOS6
from aionet.vendors.devices.base import BaseDevice
from aionet.vendors.devices.cisco import CiscoNXOS, CiscoIOSXR, CiscoASA, CiscoIOS
from aionet.vendors.devices.comware_like import ComwareLikeDevice
from aionet.vendors.devices.fujitsu import FujitsuSwitch
from aionet.vendors.devices.hp import HPComware, HPComwareLimited
from aionet.vendors.devices.ios_like import IOSLikeDevice
from aionet.vendors.devices.juniper import JuniperJunOS
from aionet.vendors.devices.junos_like import JunOSLikeDevice
from aionet.vendors.devices.mikrotik import MikrotikRouterOS
from aionet.vendors.devices.terminal import Terminal
from aionet.vendors.devices.ubiquiti import UbiquityEdgeSwitch

__all__ = (
    "CiscoASA",
    "CiscoIOS",
    "CiscoIOSXR",
    "CiscoNXOS",
    "HPComware",
    "HPComwareLimited",
    "FujitsuSwitch",
    "MikrotikRouterOS",
    "JuniperJunOS",
    "JunOSLikeDevice",
    "AristaEOS",
    "ArubaAOS6",
    "ArubaAOS8",
    "BaseDevice",
    "IOSLikeDevice",
    "ComwareLikeDevice",
    "Terminal",
    "arista",
    "aruba",
    "cisco",
    "fujitsu",
    "hp",
    "juniper",
    "mikrotik",
    "UbiquityEdgeSwitch",
)
