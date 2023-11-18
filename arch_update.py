#!/usr/bin/env python3

import os
import subprocess
import signal
import shutil
import dbus

myname = 'checkupdates'
myver = '1.0.0'

# Color codes for output
BOLD = '\033[1m'
ALL_OFF = '\033[0m'
BLUE = BOLD + '\033[34m'
GREEN = BOLD + '\033[32m'
RED = BOLD + '\033[31m'
YELLOW = BOLD + '\033[33m'

# Functions for colored output
def plain(message):
    print(f"{BOLD}    {message}{ALL_OFF}")

def msg(message):
    print(f"{GREEN}==> {ALL_OFF}{BOLD} {message}{ALL_OFF}")

def msg2(message):
    print(f"{BLUE}  ->{ALL_OFF}{BOLD} {message}{ALL_OFF}")

def ask(message):
    return input(f"{BLUE}::{ALL_OFF}{BOLD} {message}{ALL_OFF}")

def warning(message):
    print(f"{YELLOW}==> WARNING:{ALL_OFF}{BOLD} {message}{ALL_OFF}")

def error(message):
    print(f"{RED}==> ERROR:{ALL_OFF}{BOLD} {message}{ALL_OFF}")

# Notify function using dbus
def send_notification(message):
    try:
        bus = dbus.SessionBus()
        notify_obj = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
        notify_interface = dbus.Interface(notify_obj, 'org.freedesktop.Notifications')
        notify_interface.Notify(myname, 0, '', 'checkupdates', message, [], {}, 10000)
    except Exception as e:
        print(f"Error sending notification: {e}")


# Check for command-line arguments
if __name__ == "__main__":
    if len(os.sys.argv) > 1:
        print(f"{myname} v{myver}")
        print("\nSafely print a list of pending updates")
        print("\nUsage: {myname}")
        print('Note: Export the "CHECKUPDATES_DB" variable to change the path of the temporary database.')
        os.sys.exit(0)

    
# Check for the existence of fakeroot
    if shutil.which("fakeroot") is None:
        error('Cannot find the fakeroot binary.')
        os.sys.exit(1)
    # Set up temporary database directory
    CHECKUPDATES_DB = os.getenv("CHECKUPDATES_DB", os.path.join(os.getenv("TMPDIR", "/tmp"), f"checkup-db-{os.getenv('USER')}/"))
    DBPath = subprocess.check_output(["pacman-conf", "DBPath"]).decode().strip() or "/var/lib/pacman/"
    if not os.path.exists(CHECKUPDATES_DB):
        os.makedirs(CHECKUPDATES_DB)
    try:
        os.symlink(os.path.join(DBPath, "local"), os.path.join(CHECKUPDATES_DB, "local"))
    except OSError:
        pass

    # Trap for cleanup
    
    def cleanup(signum, frame):
        os.remove(os.path.join(CHECKUPDATES_DB, "db.lck"))

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    # Update Pacman database
    try:
        subprocess.run(["fakeroot", "--", "pacman", "-Sy", "--dbpath", CHECKUPDATES_DB, "--logfile", "/dev/null"], check=True)
    except subprocess.CalledProcessError:
        error('Cannot fetch updates')
        os.sys.exit(1)
    
 # List pending updates
try:
    updates_bytes = subprocess.check_output(["pacman", "-Qu", "--dbpath", CHECKUPDATES_DB], stderr=subprocess.DEVNULL)
    updates = updates_bytes.decode('utf-8')  # Decode bytes to string
    if updates:
        send_notification("Pending updates:\n" + str(updates))
except subprocess.CalledProcessError:
    pass  # You can add any specific handling for the error here

os.sys.exit(0)   
