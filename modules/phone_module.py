#!/usr/bin/env python3
"""
Phone intelligence module for TraceHound.
Enhanced with detailed number type and timezone information.
"""

import phonenumbers
from phonenumbers import carrier, geocoder, timezone

def lookup(phone):
    try:
        parsed = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(parsed):
            return {'error': 'Invalid phone number. Please ensure it includes the country code (e.g., +44...)'}
        
        # Get detailed number type
        number_type = phonenumbers.number_type(parsed)
        type_map = {
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed line",
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed line or mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium rate",
            phonenumbers.PhoneNumberType.SHARED_COST: "Shared cost",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal number",
            phonenumbers.PhoneNumberType.PAGER: "Pager",
            phonenumbers.PhoneNumberType.UAN: "UAN",
            phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
            phonenumbers.PhoneNumberType.UNKNOWN: "Unknown"
        }
        number_type_str = type_map.get(number_type, "Unknown")
        
        # Get timezones for this number
        timezones = timezone.time_zones_for_number(parsed)
        timezone_str = ', '.join(timezones) if timezones else "Unknown"
        
        details = {
            'international': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            'national': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
            'e164': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
            'country_code': parsed.country_code,
            'national_number': parsed.national_number,
            'location': geocoder.description_for_number(parsed, 'en') or 'N/A',
            'carrier': carrier.name_for_number(parsed, 'en') or 'N/A',
            'number_type': number_type_str,
            'timezone': timezone_str,
            'is_valid': True,
            'is_possible': phonenumbers.is_possible_number(parsed),
        }
        return {'details': details}
    except phonenumbers.NumberParseException as e:
        return {'error': f"Parse error: {str(e)}. Please ensure the number includes the country code."}
    except Exception as e:
        return {'error': str(e)}
