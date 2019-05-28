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
        async with aionet.create(**param) as ios:
            # Testing sending simple command
            out = await ios.send_command("show ver")
            print(out)
            # Testing sending configuration set
            commands = ["line console 0", "exit"]
            out = await ios.send_config_set(commands)
            print(out)
            # Testing sending simple command with long output
            out = await ios.send_command("show run")
            print(out)
            # Testing interactive dialog
            out = await ios.send_command("conf", pattern=r'\[terminal\]\?', strip_command=False)
            out += await ios.send_command("term", strip_command=False)
            out += await ios.send_command("exit", strip_command=False, strip_prompt=False)
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


