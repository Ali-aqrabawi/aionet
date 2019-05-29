aionet
******

Asynchronous multi-vendor library for interacting with network devices

this is a fork from netdev, with code refactor and new features added.

Requires:
---------
* asyncio
* AsyncSSH
* Python >=3.5
* pyYAML
* asyncssh
 
Supports: 
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

Features:
---------
* SSH
* Telnet
* TextFSM

Examples:
---------
Example of interacting with Cisco IOS devices:

.. code-block:: python

    import asyncio
    import aionet

    async def task(param):
        async with aionet.ConnectionHandler(**param) as conn:
            # for sending command
            out = await conn.send_command("show ver")
            print(out)
            # for config commands
            commands = ["interface vlan1", "ip address 4.4.4.4 255.255.255.255"]
            out = await conn.send_config_set(commands)
            print(out)


    async def run():
        dev1 = { 'username' : 'user',
                 'password' : 'pass',
                 'device_type': 'cisco_ios',
                 'host': 'ip address',
        }
        dev2 = { 'username' : 'user',
                 'password' : 'pass',
                 'device_type': 'cisco_ios',
                 'host': 'ip address',
        }
        devices = [dev1, dev2]
        tasks = [task(dev) for dev in devices]
        await asyncio.wait(tasks)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


