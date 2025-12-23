#!/usr/bin/env python3
"""
🔥 Neon SSH Manager — Python CLI
Kali / WSL / Linux / Termux
"""

import os
import subprocess
import sys
import time
import itertools

# ===== Colors =====
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
C = "\033[96m"
M = "\033[95m"
W = "\033[97m"
END = "\033[0m"

# ===== UI Helpers =====
def clear():
    os.system("clear")


def slow_print(text, delay=0.002):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def spinner(task="Working", duration=1.2):
    spin = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write(f"\r{C}{task} {next(spin)}{END}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 40 + "\r")


# ===== Banner =====
BANNER = f"""
{M}███████╗███████╗██╗  ██╗    ███╗   ██╗███████╗ ██████╗ ███╗   ██╗
██╔════╝██╔════╝██║  ██║    ████╗  ██║██╔════╝██╔═══██╗████╗  ██║
███████╗███████╗███████║    ██╔██╗ ██║█████╗  ██║   ██║██╔██╗ ██║
╚════██║╚════██║██╔══██║    ██║╚██╗██║██╔══╝  ██║   ██║██║╚██╗██║
███████║███████║██║  ██║    ██║ ╚████║███████╗╚██████╔╝██║ ╚████║
╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝{END}

{Y}⚡ NEON SSH MANAGER — Control your daemon like a hacker ⚡{END}
"""

MENU = f"""
{G}[1]{W} Install SSH (Kali / WSL)
{G}[2]{W} SSH Status
{G}[3]{W} Start SSH
{G}[4]{W} Enable SSH on Boot
{G}[5]{W} Disable SSH on Boot
{G}[6]{W} Stop SSH
{G}[7]{W} Restart SSH
{G}[8]{W} service ssh stop (legacy)
{G}[9]{W} Change SSH Port
{G}[10]{W} Install SSH (Termux / Android)
{G}[11]{W} Run sshd manually
{G}[12]{W} Kill sshd
{R}[x]{W} Exit
"""

# ===== Core Logic =====
def run(cmd):
    print(f"\n{Y}▶ Command:{END} {C}{cmd}{END}\n")
    spinner("Executing")
    subprocess.call(cmd, shell=True)
    input(f"\n{G}Press ENTER to continue…{END}")


def change_port():
    port = input(f"{Y}Enter new SSH port:{END} ")
    if not port.isdigit():
        print(f"{R}Invalid port number!{END}")
        time.sleep(1)
        return
    cmd = (
        f"sudo sed -i 's/^#\?Port .*/Port {port}/' /etc/ssh/sshd_config "
        f"&& sudo systemctl restart ssh"
    )
    run(cmd)


def install_android():
    clear()
    slow_print(f"{C}📱 Termux SSH Setup (Android){END}\n")
    slow_print(f"{G}pkg update && pkg install openssh{END}")
    slow_print(f"{G}sshd{END}")
    slow_print(f"{Y}Default port: 8022{END}")
    input(f"\n{G}Press ENTER to continue…{END}")


# ===== Main Loop =====
def main():
    while True:
        clear()
        print(BANNER)
        print(MENU)
        choice = input(f"{C}ssh-manager ❯ {END}").lower().strip()

        actions = {
            "1": lambda: run("sudo apt update && sudo apt install -y openssh-server"),
            "2": lambda: run("sudo systemctl status ssh"),
            "3": lambda: run("sudo systemctl start ssh"),
            "4": lambda: run("sudo systemctl enable ssh"),
            "5": lambda: run("sudo systemctl disable ssh"),
            "6": lambda: run("sudo systemctl stop ssh"),
            "7": lambda: run("sudo systemctl restart ssh"),
            "8": lambda: run("sudo service ssh stop"),
            "9": change_port,
            "10": install_android,
            "11": lambda: run("sudo sshd"),
            "12": lambda: run("sudo pkill sshd"),
        }

        if choice == "x":
            clear()
            slow_print(f"{R}👋 Disconnecting… Stay stealthy.{END}")
            sys.exit(0)
        elif choice in actions:
            actions[choice]()
        else:
            print(f"{R}Invalid option!{END}")
            time.sleep(1)


if __name__ == "__main__":
    main()
