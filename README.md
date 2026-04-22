# 🕵️ TraceHound

**Open Source Intelligence Toolkit – IP, Domain, Email, Username & Phone Number Lookups**  
*Unified menu-driven interface | Ethical use only*

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![OSINT](https://img.shields.io/badge/OSINT-Toolkit-orange)

## 🎯 Purpose

TraceHound consolidates multiple OSINT gathering capabilities into a single, easy-to-use menu-driven tool. Perfect for SOC analysts, threat hunters, and cybersecurity professionals.

## 📦 Installation (Kali Linux)

```bash
git clone https://github.com/alitalhahere/TraceHound.git
cd TraceHound
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## 🔑 Optional API Keys

For enhanced Shodan lookups:
```bash
export SHODAN_API_KEY="your_key_here"
```
All other features work without keys.

## 🚀 Usage
```bash
python tracehound.py
```
Then select a module from the menu, enter the target, and view results.

## 📝 Example

```text
$ python tracehound.py

╔══════════════════════════════════════════════════╗
║              🕵️ TRACEHOUND v1.0 🕵️              ║
╚══════════════════════════════════════════════════╝

📌 SELECT A MODULE:
  1. 🌐 IP Address Lookup
  2. 🌍 Domain Lookup
  3. ✉️ Email Breach Check
  4. 👤 Username Search
  5. 📞 Phone Number Lookup
  6. 🚪 Exit

Enter choice (1-6): 1
Enter IP address: 8.8.8.8

[*] Hunting IP: 8.8.8.8...

📍 GEOLOCATION
  IP: 8.8.8.8
  City: Mountain View
  Country: US
  ISP/Org: Google LLC

📊 SUMMARY
✓ IP 8.8.8.8 - Mountain View, US | ISP: Google LLC
```
## 🛣️ Roadmap

Unified menu interface

All five OSINT modules

JSON report export

Bulk scanning from file

Web dashboard version

## 👤 Author

Ali Talha – [LinkedIn](https://www.linkedin.com/in/imalitalha)
 
