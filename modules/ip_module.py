#!/usr/bin/env python3
"""
IP intelligence module for TraceHound.
"""

import requests
import os

SHODAN_API_KEY = os.environ.get('SHODAN_API_KEY', '')

def get_ip_geo(ip):
    """Get IP geolocation using ip-api.com (free, no API key required)."""
    try:
        # Using ip-api.com's JSON endpoint. The 'fields' parameter limits the response to what we need.
        url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,query"
        r = requests.get(url, timeout=8)
        if r.status_code == 200 and r.json().get('status') == 'success':
            d = r.json()
            return {
                'ip': d.get('query', ip),
                'city': d.get('city', 'N/A'),
                'region': d.get('regionName', 'N/A'),
                'country': d.get('country', 'N/A'),
                'zip': d.get('zip', 'N/A'),
                'location': f"{d.get('lat', 'N/A')},{d.get('lon', 'N/A')}",
                'isp': d.get('isp', 'N/A'),
                'org': d.get('org', 'N/A'),
                'as': d.get('as', 'N/A'),
            }
        else:
            error_msg = r.json().get('message', 'Unknown error')
            return {'error': f"API error: {error_msg}"}
    except Exception as e:
        return {'error': str(e)}

def get_greynoise(ip):
    # ... (keep the existing function as it's already good) ...
    try:
        r = requests.get(f"https://api.greynoise.io/v3/community/{ip}", timeout=8)
        if r.status_code == 200:
            data = r.json()
            if data.get('noise'):
                return "⚠️ Mass scanner (internet background noise)"
            elif data.get('riot'):
                return "✅ Known benign service (CDN, search engine, etc.)"
            else:
                return f"ℹ️ Classification: {data.get('classification', 'unknown')}"
        return "Not found in GreyNoise"
    except:
        return "GreyNoise lookup failed"

def get_shodan(ip):
    # ... (keep the existing function) ...
    if not SHODAN_API_KEY:
        return None
    try:
        import shodan
        api = shodan.Shodan(SHODAN_API_KEY)
        host = api.host(ip)
        return {
            'ports': host.get('ports', [])[:10],
            'org': host.get('org', 'N/A'),
            'hostnames': host.get('hostnames', [])[:3],
        }
    except:
        return None

def lookup(ip):
    result = {}
    geo = get_ip_geo(ip)
    if 'error' not in geo:
        result['geo'] = geo
    result['threat_intel'] = {'GreyNoise': get_greynoise(ip)}
    shodan_data = get_shodan(ip)
    if shodan_data:
        result['shodan'] = shodan_data
    if 'geo' in result:
        result['summary'] = f"IP {ip} - {result['geo'].get('city', 'Unknown')}, {result['geo'].get('country', 'Unknown')} | ISP: {result['geo'].get('isp', 'Unknown')}"
    return result
