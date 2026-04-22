#!/usr/bin/env python3
"""
Email intelligence module for TraceHound.
Uses XposedOrNot API for real breach checks.
"""

import requests

def check_breaches(email):
    """Check if email has been in a breach using XposedOrNot API."""
    # Using the CORRECT free API endpoint
    url = f"https://api.xposedornot.com/v1/check-email/{email}"
    
    try:
        response = requests.get(url, timeout=10)
        
        # Check if request was successful (HTTP 200 OK)
        if response.status_code == 200:
            data = response.json()
            
            # If the email was NOT found in any breaches
            if "Error" in data and data["Error"] == "Not found":
                return {'breached': False, 'message': 'Email not found in known breaches'}
            
            # If the email WAS found in breaches (the response contains a 'breaches' list)
            elif "breaches" in data:
                return {
                    'breached': True,
                    'count': len(data['breaches']),
                    'breaches': data['breaches']
                }
            # Handle other unexpected JSON structures
            else:
                return {'error': 'Unexpected API response format'}
        
        # Handle specific HTTP error codes
        elif response.status_code == 429:
            return {'error': 'Rate limit exceeded. Please wait a moment and try again.'}
        elif response.status_code == 404:
            return {'error': 'API endpoint not found'}
        else:
            return {'error': f'API error (HTTP {response.status_code})'}
            
    except requests.exceptions.Timeout:
        return {'error': 'Request timed out. The API might be slow or unavailable.'}
    except requests.exceptions.ConnectionError:
        return {'error': 'Connection error. Please check your internet connection.'}
    except Exception as e:
        return {'error': str(e)}

def lookup(email):
    """Main function to gather all email intelligence."""
    result = {}
    breach_result = check_breaches(email)
    
    # Only add to final result if it's not an error
    if 'error' not in breach_result:
        result['breach_check'] = breach_result
    else:
        # If there's an error, we can still return it to display to the user
        result['breach_check'] = breach_result
    
    return result
