#!/usr/bin/env python3

import platform
import os

# Determine the hosts file path based on OS
if platform.system() == "Windows":
    hosts_path = r"C:/Windows/System32/Drivers/etc/hosts"
else:
    hosts_path = "/etc/hosts"

# Check if file exists
if not os.path.exists(hosts_path):
    print(f"Hosts file not found at {host_path}")
else:
    print(f"Reading hosts file at {host_file}...\n")
    try:
        with open(hosts_path, "r") as file:
            contents = file.read()
            print(contents)
    except PermissionError:
        print("Permission denied! You need to run this script as administrator/root.")
