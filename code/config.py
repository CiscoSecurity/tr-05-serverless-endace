import json


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings['VERSION']

    CTR_HEADERS = {
        'User-Agent': (
            'Endace Pivot-to-Vision Integration '
            '<support@endace.com>'
        )
    }

    ENDACE_SEARCH_URL = 'https://{endaceprobe_fqdn}/vision2/v1/pivotintovision/?datasources=tag%3Arotation-file%26reltime=10m%26title=Pivot%20from%20XDR%26ip={ip}%26tools=trafficOverTime_by_app%2CconversationsChords_by_ipaddress'
    
    ENDACE_OBSERVABLE_TYPES = {
        'ip': 'IP'
    }