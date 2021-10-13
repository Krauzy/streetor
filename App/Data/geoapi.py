"""
API for positionstack
"""

import json
from http.client import HTTPConnection
from urllib.parse import urlencode
from App.config import get_token


def get_address(lat, lon) -> str:
    """
    Get address fullname of latitude and longitude

    :param lat: Latitude - float
    :param lon: Longitude - float
    :return: Full address
    """

    con = HTTPConnection('api.positionstack.com')
    params = urlencode({
        'access_key': get_token(),
        'query': f'{lat},{lon}',
        'limit': 1
    })
    con.request('GET', f'/v1/reverse?{params}')
    data = con.getresponse().read()
    return str(json.loads(data.decode('utf-8'))['data'][0]['name']).upper()
