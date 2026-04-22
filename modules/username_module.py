#!/usr/bin/env python3
"""
Username intelligence module for TraceHound.
"""

import subprocess
import json
import tempfile
import os

def lookup(username):
    print(f"[*] Checking username across multiple platforms via socialscan...")
    try:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        result = subprocess.run(
            ['socialscan', username, '--json', tmp_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            os.unlink(tmp_path)
            return {'error': f"socialscan failed: {result.stderr}"}
        
        with open(tmp_path, 'r') as f:
            data = json.load(f)
        os.unlink(tmp_path)
        
        if not isinstance(data, dict) or username not in data:
            return {'error': 'Unexpected JSON structure'}
        
        platforms_data = data[username]
        found_sites = []
        failed_checks = 0
        
        for entry in platforms_data:
            platform = entry.get('platform', 'Unknown')
            # Check if username is taken
            is_taken = False
            # Primary method: available == "False" and check succeeded
            if entry.get('available') == 'False' and entry.get('success') == 'True':
                is_taken = True
            # Fallback: message contains 'Taken' (some versions)
            elif 'Taken' in entry.get('message', ''):
                is_taken = True
            
            if is_taken:
                # Build a plausible URL
                url = f"https://{platform.lower()}.com/{username}" if platform != 'Unknown' else '#'
                found_sites.append({'name': platform, 'url': url})
            elif entry.get('success') == 'False':
                failed_checks += 1
        
        total = len(platforms_data)
        if failed_checks > 0 and not found_sites:
            print(f"[!] Warning: {failed_checks}/{total} platform checks failed (network/timeout). Try again later.")
        
        return {
            'total_checked': total,
            'found_on': found_sites,
            'summary': f"Username '{username}' found on {len(found_sites)}/{total} platforms"
        }
        
    except Exception as e:
        return {'error': str(e)}
