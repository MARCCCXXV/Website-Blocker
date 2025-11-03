#!/usr/bin/env python3

import platform
import os
import ctypes
import sys


def show_blocked_websites():
    with open(hosts_path, "r") as file:
        print("Currently blocked websites: ")
        found = False
        for line in file:
            if line.strip().startswith("#") or not line.strip():
                continue
            if line.strip().startswith("127.0.0.1"):
                print(line, end="")
                found = True
        if not found:
            print("No websites currently blocked")

def normalize_website(website):
    website = website.replace("https://", "")
    website = website.replace("http://", "")
    website = website.split('/')[0] # /'s after .com
    return website.strip()    

def block_website(website):
    website = normalize_website(website)
    if not website.startswith("www."): # if website does NOT start with www
        domains = [website, f"www.{website}"]
    else:
        domains = [website[4:], website]

    try:
        with open(hosts_path, "r+") as file:
            contents = file.read()
            if website in contents:
                print(f"{website} is already blocked")
            else:
                for domain in domains:
                    line_to_add = f"127.0.0.1 {domain}"
                    file.write(line_to_add + "\n")
                file.flush()
                print(f"{website} is now blocked")
            
    except PermissionError:
        print("You need administrator permissions")
    
def unblock_website(website):
    website = normalize_website(website)
    try:
        with open(hosts_path, "r") as file:
            lines = file.readlines()
        
        found = False
        with open(hosts_path, "w") as file:
            for line in lines:
                if website.startswith ("www."):
                    if line.strip() in (f"127.0.0.1 {website}", f"127.0.0.1 {website[4:]}"):
                        found = True
                        continue
                else:
                    if line.strip() in (f"127.0.0.1 {website}", f"127.0.0.1 www.{website}"):
                        found = True
                        continue
                file.write(line)
            file.flush()
                
        if found == True:
            print(f"{website} has been unblocked")
        else:
            print(f"{website} can not be found")
    except PermissionError:
        print("Error access this file. Try running script as admin")

def run_as_admin():
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False

    if not is_admin:
        print("Restarting with admin privileges...")
        # Relaunch the program as admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    
    
# Check and run with administrator priv    
run_as_admin()

# Determine the hosts file path based on OS
if platform.system() == "Windows":
    hosts_path = r"C:/Windows/System32/Drivers/etc/test_hosts"
else:
    hosts_path = "/etc/hosts" # for mac or other OS

# Check if file exists
if not os.path.exists(hosts_path): # if path does not exist
    print(f"Hosts file not found at {hosts_path}")
    exit(1)
else:
    print(f"Reading hosts file at {hosts_path}\n") # ELSE path DOES exist


choice = ""
while(choice != "0"):
    print("1. Show websites \n2. Block website\n3. Unblock website \n0. Exit\n")
    choice = input("Type in number:\n")
    if choice == "1":
        show_blocked_websites()

    elif choice == "2":
        website = input("What website do you want to block?\n")
        block_website(website)

    elif choice == "3":
        website = input("What website do you want to unblock? \n")
        unblock_website(website)
    elif choice =="0":
        print("Exiting program...")