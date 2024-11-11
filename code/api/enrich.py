from functools import partial

from flask import Blueprint, current_app
from urllib.parse import quote

from api.schemas import ObservableSchema
from api.utils import get_json, jsonify_data, get_key

enrich_api = Blueprint('enrich', __name__)
get_observables = partial(get_json, schema=ObservableSchema(many=True))


def get_browse_pivot(ip, host):
    return {
        'id': f'ref-endace-search-ip-{ip}',
        'title': 'Generate Pivot to EndaceVision link',
        'description': 'Generate a Pivot-to-Vision URL from this IP address',
        'url': current_app.config['ENDACE_SEARCH_URL'].format(endaceprobe_fqdn=host, ip=ip),
        'categories': ['Search', 'Endace'],
    }


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    observables = get_observables()
    data = []
    
    key = get_key()

    if key is None:
        raise AuthenticationRequiredError

    for observable in observables:
        value = observable['value']
        type = observable['type'].lower()

        if type in current_app.config['ENDACE_OBSERVABLE_TYPES']:
            if type == 'ip':
                # retrieve target host from token
                host = current_app.config['endaceprobe_fqdn']
                
                data.append(get_browse_pivot(value, host))

    return jsonify_data(data)
