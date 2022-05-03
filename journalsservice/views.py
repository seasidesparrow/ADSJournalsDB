import json
import re

from flask import current_app
from flask_restful import Resource
from flask_discoverer import advertise
from datetime import datetime
from dateutil import parser
from journalsdb.models import JournalsMaster, JournalsAbbreviations, JournalsIdentifiers, JournalsPublisher, JournalsRefSource
from journalsservice.solrquery import SolrQuery
import adsmutils

def liken(text):
    text_out = re.sub(r'[. ]{1,}', '%', text)
    text_out = '%{}%'.format(text_out)
    text_out = re.sub(r'%{1,}', '%', text_out)
    return text_out

class Summary(Resource):

    scopes = []
    rate_limit = [1000, 60 * 60 * 24]
    decorators = [advertise('scopes', 'rate_limit')]

    def get(self, bibstem):
        if bibstem:
            try:
                with current_app.session_scope() as session:
                    dat_master = session.query(JournalsMaster).filter_by(bibstem=bibstem).first()
                    try:
                        masterid = dat_master.masterid
                    except Exception as err:
                        return {'Error': 'Search failed',
                                'Error Info': 'Bibstem "%s" not found.' % bibstem}, 200
                    else:
                        dat_abbrev = [rec.toJSON() for rec in session.query(JournalsAbbreviations).filter_by(masterid=masterid).all()]
                        dat_idents = [rec.toJSON() for rec in session.query(JournalsIdentifiers).filter_by(masterid=masterid).all()]
                        dat_publisher = [rec.toJSON() for rec in session.query(JournalsPublisher).filter_by(masterid=masterid).all()]
                        result_json = {'summary': 
                                          {'master': dat_master.toJSON(),
                                           'idents': dat_idents,
                                           'abbrev': dat_abbrev,
                                           'publisher': dat_publisher
                                          }
                                      }
    
                        return result_json, 200
            except Exception as err:
                return {'Error': 'Summary search failed',
                        'Error Info': 'Unspecified error.  Try again.'}, 500
        else:
            result_json = {'summary': {}}
            return result_json, 200

class Journal(Resource):

    scopes = []
    rate_limit = [1000, 60 * 60 * 24]
    decorators = [advertise('scopes', 'rate_limit')]

    def get(self, journalname):
        journal_list = []
        if journalname:
            jname = liken(journalname)
            try:
                with current_app.session_scope() as session:
                    dat_abbrev = session.query(JournalsAbbreviations).filter(JournalsAbbreviations.abbreviation.ilike(jname)).all()
                    rec_found = list(set([rec.masterid for rec in dat_abbrev]))
                    for mid in rec_found:
                        dat_master = session.query(JournalsMaster).filter_by(masterid=mid).first()
                        journal_list.append({"bibstem": dat_master.bibstem, "name": dat_master.journal_name})
            except Exception as err:
                return {'Error': 'Journal search failed',
                        'Error Info': 'Unspecified error.  Try again.'}, 500

        result_json = {'journal': journal_list}
        return result_json, 200


class Holdings(Resource):

    scopes = []
    rate_limit = [1000, 60 * 60 * 24]
    decorators = [advertise('scopes', 'rate_limit')]

    def get(self, bibstem, volume):
        try:
            q = SolrQuery()
            result = q.search(bibstem, volume)
        except Exception as err:
            return {'Error': 'Holdings search failed',
                    'Error Info': 'Unspecified error.  Try again.'}, 500
        else:
            return result, 200


class Refsource(Resource):

    scopes = []
    rate_limit = [1000, 60 * 60 * 24]
    decorators = [advertise('scopes', 'rate_limit')]

    def get(self, bibstem):
        request_json = {}
        if bibstem:
            try:
                with current_app.session_scope() as session:
                    try:
                        # exact match to bibstem
                        id_master = session.query(JournalsMaster).filter_by(bibstem=bibstem).first()
                        # case-insensitive match to bibstem
                        # id_master = session.query(JournalsMaster).filter(JournalsMaster.bibstem.ilike(bibstem)).first()
                        masterid = id_master.masterid
                    except Exception as err:
                        pass
                    else:
                        dat_refsource = session.query(JournalsRefSource).filter_by(masterid=masterid).first()
                        request_json = json.loads(dat_refsource.refsource_list)
            except Exception as err:
                return {'Error': 'Refsource search failed',
                        'Error Info': 'Unspecified error.  Try again.'}, 500
        return {'refsource': request_json}, 200

