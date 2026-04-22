#!/usr/bin/env python3
"""
Domain intelligence module for TraceHound.
Enhanced with better error handling and output formatting.
"""

import whois
import dns.resolver
import datetime

def get_whois(domain):
    try:
        w = whois.whois(domain)
        # Format dates nicely if they exist
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        expiration_date = w.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
            
        return {
            'registrar': str(w.registrar) if w.registrar else 'N/A',
            'creation_date': creation_date.strftime('%Y-%m-%d') if creation_date else 'N/A',
            'expiration_date': expiration_date.strftime('%Y-%m-%d') if expiration_date else 'N/A',
            'name_servers': ', '.join(w.name_servers) if w.name_servers else 'N/A',
            'org': str(w.org) if w.org else 'N/A',
            'emails': ', '.join(w.emails) if w.emails else 'N/A',
        }
    except Exception as e:
        return {'error': f"WHOIS lookup failed: {str(e)}"}

def get_dns_records(domain):
    records = {}
    types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
    for t in types:
        try:
            answers = dns.resolver.resolve(domain, t)
            records[t] = [str(r) for r in answers][:5]
        except:
            records[t] = []
    return records

def lookup(domain):
    result = {}
    whois_data = get_whois(domain)
    if 'error' not in whois_data:
        result['whois'] = whois_data
    result['dns'] = get_dns_records(domain)
    return result
