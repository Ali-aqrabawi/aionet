[<img src="https://api.gitsponsors.com/api/badge/img?id=189100742" height="20">](https://api.gitsponsors.com/api/badge/link?p=s/bIl/DSZ7HepRgke8KW2Vt4Pi/Q3xXs9E6KBJtgn2X1UlNsUFTLHp1GigANZtx9MQX6ghXb+Yf72QNh8p3oV+C9ModLWLBuGfyDclwaWgmne5pYAA++TVeZV6mvougXpMIvDycu+iktpXiZ0dRwZQ==)

# aionet
******

Asynchronous multi-vendor library for interacting with network devices

this is a fork from netdev, with code refactor and new features added.

## Requires:
---------
* asyncio
* AsyncSSH
* Python >=3.5
* pyYAML
* asyncssh
 
## Supports: 
---------
* Cisco IOS 
* Cisco IOS XE
* Cisco IOS XR
* Cisco ASA
* Cisco NX-OS 
* HP Comware
* Fujitsu Blade Switches
* Mikrotik RouterOS
* Arista EOS
* Juniper JunOS
* Aruba AOS 6.X
* Aruba AOS 8.X
* Terminal

## Features:
---------
* SSH
* Telnet
* TextFSM

## Examples:
---------
Example of interacting with Cisco IOS devices:

```python

    import asyncio
    import aionet

    async def task(device):
        async with aionet.ConnectionHandler(**device) as conn:

            out = await conn.send_command("show ver")
            print(out)

            commands = ["interface vlan2", "no shut"]
            out = await conn.send_config_set(commands)



    async def run():
        dev1 = { 'username' : 'user',
                 'password' : 'pass',
                 'device_type': 'cisco_ios',
                 'ip': 'ip address',
        }
        dev2 = { 'username' : 'user',
                 'password' : 'pass',
                 'device_type': 'cisco_ios',
                 'ip': 'ip address',
        }
        devices = [dev1, dev2]
        tasks = [task(dev) for dev in devices]
        await asyncio.wait(tasks)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

```
