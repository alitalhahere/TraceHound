#!/usr/bin/env python3
"""
Display utilities for TraceHound.
"""

from colorama import Fore, Style

def banner():
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════╗
║                    🕵️ TRACEHOUND v1.0 🕵️                        ║
║              Open Source Intelligence Toolkit                    ║
║                   Menu-Driven | Ethical Use Only                 ║
╚══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
{Fore.YELLOW}🔐 Author: Ali Talha (CEH) | GitHub: alitalhahere{Style.RESET_ALL}
{Fore.GREEN}📡 Multi-Source OSINT | Follow digital footprints{Style.RESET_ALL}
    """)

def section(title):
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'='*50}")
    print(f" {title}")
    print(f"{'='*50}{Style.RESET_ALL}")

def info(key, value):
    print(f"  {Fore.CYAN}{key}:{Style.RESET_ALL} {value}")

def success(msg):
    print(f"  {Fore.GREEN}✓ {msg}{Style.RESET_ALL}")

def warning(msg):
    print(f"  {Fore.YELLOW}⚠ {msg}{Style.RESET_ALL}")

def error(msg):
    print(f"  {Fore.RED}✗ {msg}{Style.RESET_ALL}")
