# VPN-Manager
Python script to manage virtually any VPN network under Linux, based on configuration files.

This script was born from the need of a central control system for all my VPNs, as my ZSH aliases grew to an unmanageable mess.

How it works
------------
The core mechanism is simple enough: all the `*.conf` files in the __same folder as the script__ are parsed, and VPN infos and necessary commands are extracted.
The script then loops around the parsed data and outputs an intelligible list of the available configurations; after you choose one, a prompt will ask you if you want to connect or disconnect to the selected network.
When connecting a _lockfile_ will be created, so that when you run the script again it will warn you about which connections are already estabilished and which aren't. The _lockfile_ is deleted when you choose to disconnect from the correspondent network.

Configuration files
-------------------
The configuration files __must__ end with the `.conf` extension.
They __must__ also contain _at least_ the following lines:

`NAME`: the display name of the VPN in the main menu.

`START`: the shell command to be executed when you choose to connect to the VPN.

`STOP`: the shell command to be executed when you choose to disconnect from the VPN.

`LOCK`: the path to the lockfile (inluding the file itself). _I suggest to place it in_ `/tmp`_, so that if the machine is rebooted no false flags will be detected._

For an example please refer to the [example configuration file](example.conf).