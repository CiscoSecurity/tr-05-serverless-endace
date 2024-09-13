from functools import partial

from flask import Blueprint, current_app
from urllib.parse import quote

from api.schemas import ObservableSchema
from api.utils import get_json, jsonify_data

enrich_api = Blueprint('enrich', __name__)


get_observables = partial(get_json, schema=ObservableSchema(many=True))


def get_browse_pivot(ip):
    return {
        'id': f'ref-endace-detail-ip-{ip}',
        'title': 'Search Packets for IP',
        'description': 'Pivot to EndaceVision using this IP',
        'url': current_app.config['ENDACE_SEARCH_URL'].format(endaceprobe_fqdn=current_app.config['HOST'], ip=ip),
        'categories': ['Browse', 'Endace'],
    }

@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    observables = get_observables()
    data = []

    for observable in observables:
        value = observable['value']
        type = observable['type'].lower()

        if type in current_app.config['ENDACE_OBSERVABLE_TYPES']:
            if type == 'ip':
                data.append(get_browse_pivot(value))

    return jsonify_data(data)
