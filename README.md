# VPN-Manager
Python script to manage virtually any VPN network under Linux, based on configuration files.

This script was born from the need of a central control system for all my VPNs, as my ZSH aliases grew to an unmanageable mess.

How it works
------------
The core mechanism is simple enough: you specify the path of your configurations folder in a line starting with `CONF_DIR` in the `vpnmanager.conf` file (in the same directory as the script), and all the `*.conf` files in that path are parsed, VPN infos and necessary commands being extracted from each them.
The script then loops around the parsed data and outputs an intelligible list of the available configurations; after you choose one, a prompt will ask you if you want to connect or disconnect to the selected network.
When connecting a _lockfile_ will be created, so that when you run the script again it will warn you about which connections are already estabilished and which aren't. The _lockfile_ is deleted when you choose to disconnect from the correspondent network.

Configuration files
-------------------
The configuration files __must__ end with the `.conf` extension.
They __must__ also contain _at least_ the following lines (the lines must __start__ with the these words, anything else will be considered a comment):

`NAME`: the display name of the VPN in the main menu.

`START`: the shell command to be executed when you choose to connect to the VPN.

`STOP`: the shell command to be executed when you choose to disconnect from the VPN.

__Note 1: when parsing the START and STOP commands, the word `#PATH#` will be replaced with the script's folder path (in the format `/home/myuser/bin`, for example). The word `#CONF#` will be replaced with the configuration files' folder path instead.__

__Note 2: the replaced path won't have a trailing slash (e.g.: `/foo/bar` and not `/foo/bar/`)__

You must also include __one__ of the following:

`LOCK`: the path to the custom lockfile (inluding the file itself). _I suggest to place it in_ `/tmp`_, so that if the machine is rebooted no false flags will be detected._

`SYSLOCK`: the path to the system's lockfile or pidfile of the program used (usually found in `/var/run` or just `/run`). __Note: this file won't be programmatically created, the script will just check for it's existence at run rime.__

For an example please refer to the [example configuration file](vpnmanager.conf.d/example.conf).
