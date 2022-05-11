import os
import json
from flask import current_app, request

class HoldingsInitException(Exception):
    pass


class HoldingsQueryException(Exception):
    pass


class EmptyBibstemException(Exception):
    pass


class ADSQuery(object):

    def __init__(self):
        try:
            self.token = current_app.config.get('SERVICE_TOKEN', None) or \
                         request.headers.get('X-Forwarded-Authorization', \
                         request.headers.get('Authorization', ''))
            self.queryurl = current_app.config.get('HOLDINGS_ADS_QUERY_URL', None)
            # self.holdings_query = '?q=bibstem:%s,volume:%s&fl=bibstem,year,volume,page,esources&rows=2000&sort=page+asc&wt=json'
        except Exception as err:
            raise HoldingsInitException(err)
        else:
            pass


    def search(self, bibstem=None, volume='*'):
        if bibstem:
            try:
                params = {
                    'q': 'bibstem:%s,volume:%s' % (bibstem, volume),
                    'wt': 'json',
                    'fl': 'bibstem,year,volume,page,esources'
                }
                headers = {
                    'Authorization': self.token
                }
                response = current_app.client.get(
                    url=self.queryurl,
                    params=params,
                    headers=headers,
                )
                response.raise_for_status()
                results = response.json()
            except Exception as err:
                raise HoldingsQueryException(err)
            else:
                return results
        else:
            raise EmptyBibstemException('You must provide a bibstem.')
