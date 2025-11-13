# LockIn Timer

A simple app that I made which will help me become more productive by blocking distracting websites.

### How it works
Focus Blocker temporarily modifies your system's hosts file to redirect blocked websites to localhost (127.0.0.1), making them inaccessible during your focus session.

--------------
 
 **Warning**: If the app closes unexpectedly while blocking is active, you may need to open app again and press block, then press unblock to reset host files. 
 Alternatively, you can go directly to host file and manually edit it.

  Administrator Privileges Required: This app needs admin/root access to modify the hosts file.



## Features
- Customizable block list: add or remove websites.
- Timer feature
- Currently only works on Windows, Mac
- Edits hosts file located in C:\Windows\System32\drivers\etc\hosts

## Troubleshooting
- Windows: Edits hosts file located in C:\Windows\System32\drivers\etc\hosts
- Mac: Edit hosts file located in: /etc/hosts 
- Not needed, but if websites aren't being blocked then:
  1.  flushDNS
  2.  Restart browswer
  3.  Run as administrator




