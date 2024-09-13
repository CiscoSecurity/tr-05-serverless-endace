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

    ENDACE_SEARCH_URL = '{endaceprobe_fqdn}/vision2/v1/pivotintovision/?datasources=tag%3Arotation-file%26title=Pivot%20from%20XDR%26ip={ip}%26tools=conversations_by_ipaddress'

    ENDACE_OBSERVABLE_TYPES = {
        'ip': 'IP'
    }
