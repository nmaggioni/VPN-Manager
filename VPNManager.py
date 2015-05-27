#!/usr/bin/env python3
import os
import glob

__author__ = "Niccolò Maggioni"
__copyright__ = "Copyright 2015, Niccolò Maggioni"
__license__ = "MIT"
__version__ = "2.0.0"

networks = {}
path = os.path.dirname(__file__)


class Rete:
    def __init__(self, name, start_cmd, stop_cmd, lock_custom, lock):
        self.name = name
        self.start_cmd = start_cmd
        self.stop_cmd = stop_cmd
        self.lock_custom = lock_custom
        self.lock = lock


def connect(n):
    name = networks_list[n]
    command = networks[name].start_cmd.replace('#PATH#', path)
    os.system(command)
    if networks[name].lock_custom:
        lock = open(networks[name].lock, 'w+')
        lock.close()


def disconnect(n):
    name = networks_list[n]
    command = networks[name].stop_cmd.replace('#PATH#', path)
    os.system(command)
    lock = networks[name].lock
    if networks[name].lock_custom:
        if os.path.isfile(lock):
            os.remove(lock)


def ask(n):
    print("")
    choice_input = input("Connect or Disconnect? [C/D]: ")
    if choice_input == "C" or choice_input == "c":
        connect(n - 1)
    elif choice_input == "D" or choice_input == "d":
        disconnect(n - 1)


def choose():
    global choice
    choice = input("[1..n] ")
    if choice == "e" or choice == "E" or choice == "q" or choice == "Q":
        raise SystemExit
    try:
        choice = int(choice)
    except ValueError:
        print("Please enter a number.\n")
        choose()


def print_running(el, running):
    if running:
        print(str(networks_list.index(el) + 1) + ") " + el + " (Connected)")
    else:
        print(str(networks_list.index(el) + 1) + ") " + el)


def print_list():
    global networks_list
    networks_list = list(networks)
    for el in networks_list:
        if os.path.isfile(networks[el].lock):
            print_running(el, True)
        else:
            print_running(el, False)


def parse_confs():
    confs = glob.glob(path + '/*.conf')
    for conf in confs:
        with open(conf) as file:
            for line in file:
                global tmp_lock_custom
                if line.startswith("NAME"):
                    tmp_name = line.split('=')[1].replace('\n', '')
                elif line.startswith("START"):
                    tmp_start_cmd = line.split('=')[1].replace('\n', '')
                elif line.startswith("STOP"):
                    tmp_stop_cmd = line.split('=')[1].replace('\n', '')
                elif line.startswith("LOCK"):
                    tmp_lock_custom = True
                    tmp_lock = line.split('=')[1].replace('\n', '')
                elif line.startswith("SYSLOCK"):
                    tmp_lock_custom = False
                    tmp_lock = line.split('=')[1].replace('\n', '')

        try:
            tmp_name
        except NameError:
            raise KeyError("Unable to find the NAME key in the configuration file: " + conf)
        try:
            tmp_start_cmd
        except NameError:
            raise KeyError("Unable to find the START key in the configuration file: " + conf)
        try:
            tmp_stop_cmd
        except NameError:
            raise KeyError("Unable to find the STOP key in the configuration file: " + conf)
        try:
            tmp_lock
        except NameError:
            raise KeyError("Unable to find the LOCK or the SYSLOCK key in the configuration file: " + conf)

        tmp_class = Rete(tmp_name, tmp_start_cmd, tmp_stop_cmd, tmp_lock_custom, tmp_lock)
        networks[tmp_name] = tmp_class


print("""
        (       )     *                                    
        )\ ) ( /(   (  `                                   
 (   ( (()/( )\())  )\))(     )          ) (  (    (  (    
 )\  )\ /(_)|(_)\  ((_)()\ ( /(  (    ( /( )\))(  ))\ )(   
((_)((_|_))  _((_) (_()((_))(_)) )\ ) )(_)|(_))\ /((_|()\  
\ \ / /| _ \| \| | |  \/  ((_)_ _(_/(((_)_ (()(_|_))  ((_) 
 \ V / |  _/| .` | | |\/| / _` | ' \)) _` / _` |/ -_)| '_| 
  \_/  |_|  |_|\_| |_|  |_\__,_|_||_|\__,_\__, |\___||_|   
                                          |___/      v""" + __version__ + "\n")

print("Available networks:                            {Q|E} to exit")
print("===================                            =============")
parse_confs()
print_list()
print("")
try:
    choose()
    while True:
        if choice not in [n for n in range(1, len(networks) + 1)]:
            print("The number you entered does not match any network.\n")
            choose()
        else:
            break
    ask(choice)
except KeyboardInterrupt:
    raise SystemExit
