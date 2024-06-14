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

    ENDACE_SEARCH_URL = 'https://dim-1.lab.endace.com/vision2/v1/pivotintovision/?datasources=tag%3Arotation-file%26title=Pivot from XDR%26ip={ip}%26tools=conversations_by_ipaddress'

    ENDACE_OBSERVABLE_TYPES = {
        'ip': 'IP'
    }
