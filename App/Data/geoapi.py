from http.client import HTTPConnection
from urllib.parse import urlencode
from App.config import get_token
import json


def get_address(lat, lon) -> str:
    con = HTTPConnection('api.positionstack.com')
    params = urlencode({
        'access_key': get_token(),
        'query': '{},{}'.format(lat, lon),
        'limit': 1
    })
    con.request('GET', '/v1/reverse?{}'.format(params))
    data = con.getresponse().read()
    return json.loads(data.decode('utf-8'))['data'][0]['name']
