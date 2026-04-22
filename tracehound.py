#!/usr/bin/env python3
"""
TraceHound - Main unified menu-driven OSINT tool.
Run this script to access all modules.
Enhanced with better output formatting and module integrations.
"""

import sys
import os
import json
from colorama import init, Fore, Style

init(autoreset=True)

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.printer import banner, section, info, success, warning, error
from modules import ip_module, domain_module, email_module, username_module, phone_module

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_ip_results(data):
    """Display enhanced IP lookup results."""
    if 'geo' in data:
        section("📍 GEOLOCATION")
        geo = data['geo']
        info("IP", geo.get('ip', 'N/A'))
        info("City", geo.get('city', 'N/A'))
        info("Region", geo.get('region', 'N/A'))
        info("Country", geo.get('country', 'N/A'))
        info("Postal Code", geo.get('zip', 'N/A'))
        info("Coordinates", geo.get('location', 'N/A'))
        info("ISP", geo.get('isp', 'N/A'))
        info("Organization", geo.get('org', 'N/A'))
        info("ASN", geo.get('as', 'N/A'))
    if 'threat_intel' in data:
        section("🛡️ THREAT INTELLIGENCE")
        info("GreyNoise", data['threat_intel'].get('GreyNoise', 'N/A'))
    if 'shodan' in data:
        section("🔍 SHODAN (if API key set)")
        shodan = data['shodan']
        info("Open Ports", ', '.join(map(str, shodan.get('ports', []))) or 'None')
        info("Organization", shodan.get('org', 'N/A'))
    if 'summary' in data:
        section("📊 SUMMARY")
        success(data['summary'])

def print_domain_results(data):
    """Display enhanced domain lookup results."""
    if 'whois' in data:
        section("📋 WHOIS")
        whois = data['whois']
        info("Registrar", whois.get('registrar', 'N/A'))
        info("Creation Date", whois.get('creation_date', 'N/A'))
        info("Expiration Date", whois.get('expiration_date', 'N/A'))
        info("Organization", whois.get('org', 'N/A'))
        info("Name Servers", whois.get('name_servers', 'N/A'))
    if 'dns' in data:
        section("🌍 DNS RECORDS")
        for rtype, records in data['dns'].items():
            if records:
                info(rtype, ', '.join(records[:3]))

def print_email_results(data):
    """Display enhanced email breach results."""
    if 'breach_check' in data:
        section("🔓 BREACH CHECK")
        bc = data['breach_check']
        if bc.get('breached'):
            warning(f"⚠️ EMAIL BREACHED! Found in {bc.get('count', 0)} data breaches!")
            if bc.get('breaches'):
                info("Sample breaches", ', '.join(bc.get('breaches', [])[:3]))
                warning("Change your passwords and enable 2FA immediately!")
        else:
            success("✅ Good news! Email not found in known data breaches.")
    else:
        error("Could not perform breach check. API may be unavailable.")

def print_username_results(data):
    """Display enhanced username search results."""
    if 'error' in data:
        error(f"Error: {data['error']}")
        return
    section("📱 USERNAME SEARCH RESULTS")
    if data.get('found_on'):
        success(f"Username found on {len(data['found_on'])} websites:")
        for site in data['found_on'][:20]:  # Show first 20 to avoid overwhelming the terminal
            info(site['name'], site['url'])
        if len(data['found_on']) > 20:
            info("... and more", f"{len(data['found_on']) - 20} additional sites")
    else:
        info("No accounts found", f"Checked {data.get('total_checked', 0)} websites. Username may not be used or profile is private.")
    section("📊 SUMMARY")
    info("Result", data.get('summary', 'No summary available'))

def print_phone_results(data):
    """Display enhanced phone number results."""
    if 'error' in data:
        error(data['error'])
        return
    if 'details' in data:
        section("📞 PHONE DETAILS")
        d = data['details']
        info("International", d.get('international', 'N/A'))
        info("National", d.get('national', 'N/A'))
        info("E.164 Format", d.get('e164', 'N/A'))
        info("Country Code", d.get('country_code', 'N/A'))
        info("Location", d.get('location', 'N/A'))
        info("Carrier", d.get('carrier', 'N/A'))
        info("Number Type", d.get('number_type', 'N/A'))
        info("Timezone", d.get('timezone', 'N/A'))
        info("Valid", "✅ Yes" if d.get('is_valid') else "❌ No")
        info("Possible", "✅ Yes" if d.get('is_possible') else "❌ No")

def save_to_json(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        success(f"Report saved to {filename}")
    except Exception as e:
        error(f"Failed to save: {e}")

def main():
    while True:
        clear_screen()
        # Custom banner (fallback if utils.printer.banner fails)
        print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════╗
║                        🕵️ TRACEHOUND v2.0 🕵️                       ║
║                  Open Source Intelligence Toolkit                ║
║                   Menu-Driven | Ethical Use Only                 ║
╚══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
{Fore.YELLOW}🔐 Author: Ali Talha | GitHub: alitalhahere{Style.RESET_ALL}
{Fore.GREEN}📡 Multi-Source OSINT | Follow digital footprints{Style.RESET_ALL}
        """)
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📌 SELECT A MODULE:{Style.RESET_ALL}")
        print("  " + f"{Fore.GREEN}1.{Style.RESET_ALL} 🌐 IP Address Lookup")
        print("  " + f"{Fore.GREEN}2.{Style.RESET_ALL} 🌍 Domain Lookup")
        print("  " + f"{Fore.GREEN}3.{Style.RESET_ALL} ✉️ Email Breach Check")
        print("  " + f"{Fore.GREEN}4.{Style.RESET_ALL} 👤 Username Search")
        print("  " + f"{Fore.GREEN}5.{Style.RESET_ALL} 📞 Phone Number Lookup")
        print("  " + f"{Fore.GREEN}6.{Style.RESET_ALL} 🚪 Exit")
        print(f"{Fore.CYAN}{'─'*50}{Style.RESET_ALL}")
        
        choice = input(f"{Fore.YELLOW}Enter choice (1-6): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            target = input(f"{Fore.YELLOW}Enter IP address: {Style.RESET_ALL}").strip()
            if target:
                print(f"\n{Fore.MAGENTA}[*] Hunting IP: {target}...{Style.RESET_ALL}")
                result = ip_module.lookup(target)
                print_ip_results(result)
                save = input(f"\n{Fore.YELLOW}Save report to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
                if save == 'y':
                    save_to_json(result, f"ip_{target}.json")
            else:
                error("No IP entered")
        
        elif choice == '2':
            target = input(f"{Fore.YELLOW}Enter domain: {Style.RESET_ALL}").strip()
            if target:
                print(f"\n{Fore.MAGENTA}[*] Hunting domain: {target}...{Style.RESET_ALL}")
                result = domain_module.lookup(target)
                print_domain_results(result)
                save = input(f"\n{Fore.YELLOW}Save report to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
                if save == 'y':
                    save_to_json(result, f"domain_{target}.json")
            else:
                error("No domain entered")
        
        elif choice == '3':
            target = input(f"{Fore.YELLOW}Enter email address: {Style.RESET_ALL}").strip()
            if target:
                print(f"\n{Fore.MAGENTA}[*] Hunting email: {target}...{Style.RESET_ALL}")
                result = email_module.lookup(target)
                print_email_results(result)
                save = input(f"\n{Fore.YELLOW}Save report to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
                if save == 'y':
                    save_to_json(result, f"email_{target}.json")
            else:
                error("No email entered")
        
        elif choice == '4':
            target = input(f"{Fore.YELLOW}Enter username: {Style.RESET_ALL}").strip()
            if target:
                print(f"\n{Fore.MAGENTA}[*] Hunting username: {target}...{Style.RESET_ALL}")
                result = username_module.lookup(target)
                print_username_results(result)
                save = input(f"\n{Fore.YELLOW}Save report to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
                if save == 'y':
                    save_to_json(result, f"username_{target}.json")
            else:
                error("No username entered")
        
        elif choice == '5':
            target = input(f"{Fore.YELLOW}Enter phone number (with country code, e.g., +1234567890): {Style.RESET_ALL}").strip()
            if target:
                print(f"\n{Fore.MAGENTA}[*] Hunting phone: {target}...{Style.RESET_ALL}")
                result = phone_module.lookup(target)
                print_phone_results(result)
                save = input(f"\n{Fore.YELLOW}Save report to JSON? (y/n): {Style.RESET_ALL}").strip().lower()
                if save == 'y':
                    save_to_json(result, f"phone_{target}.json")
            else:
                error("No phone number entered")
        
        elif choice == '6':
            print(f"\n{Fore.GREEN}Exiting TraceHound. Stay curious.{Style.RESET_ALL}")
            break
        
        else:
            error("Invalid choice. Press Enter to continue...")
            input()
            continue
        
        input(f"\n{Fore.CYAN}Press Enter to return to menu...{Style.RESET_ALL}")

if __name__ == '__main__':
    main()
