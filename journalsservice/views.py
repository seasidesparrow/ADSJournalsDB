import json
import re

from flask import current_app
from flask_restful import Resource
from flask_discoverer import advertise
from datetime import datetime
from dateutil import parser
from journalsdb.models import JournalsMaster, JournalsAbbreviations, JournalsIdentifiers, JournalsPublisher, JournalsRefSource, JournalsTitleHistory, JournalsNames
from journalsservice.adsquery import ADSQuery
import adsmutils
from sqlalchemy import or_, and_

def liken(text):
    text_out = re.sub(r'[. ]{1,}', '%', text)
    text_out = '%{}%'.format(text_out)
    text_out = re.sub(r'%{1,}', '%', text_out)
    return text_out

def sort_journals(results):
    # sort to put journal results at the front of the list
    try:
        sorted_journals = []
        pubtypeOrder = ["Journal","Conf. Proc.","Other"]
        for pt in pubtypeOrder:
            for j in results:
                if j.get("pubtype","") == pt:
                    sorted_journals.append(j)
        for j in results:
            if j.get("pubtype","") not in pubtypeOrder:
                sorted_journals.append(j)
        for j in sorted_journals:
            if j.get("pubtype", None):
                del j["pubtype"]
        return sorted_journals
    except:
        return results

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
                        dat_abbrev = [rec.toJSON()['abbreviation'] for rec in session.query(JournalsAbbreviations).filter_by(masterid=masterid).all()]
                        dat_idents = [rec.toJSON() for rec in session.query(JournalsIdentifiers).filter_by(masterid=masterid).all()]
                        dat_names = [rec.toJSON() for rec in session.query(JournalsNames).filter_by(masterid=masterid).all()]
                        dat_titlehist = [rec.toJSON() for rec in session.query(JournalsTitleHistory).filter_by(masterid=masterid).all()]
                        dat_pubhist = []
                    
                        if dat_titlehist:
                            for t in dat_titlehist:
                                publisherid = t.pop('publisherid', None)
                                if publisherid:
                                    pub = session.query(JournalsPublisher).filter_by(publisherid=publisherid).first()
                                    pubhist = {'publisher': pub.toJSON()['pubabbrev'], 'title': t}
                                    dat_pubhist.append(pubhist)
                        result_json = {'summary':
                                          {'master': dat_master.toJSON(),
                                           'idents': dat_idents,
                                           'abbrev': dat_abbrev,
                                           'pubhist': dat_pubhist,
                                           'names': dat_names
                                          }
                                      }

                        return result_json, 200
            except Exception as err:
                return {'Error': 'Summary search failed',
                        'Error Info': str(err)}, 500
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
                    rec_found = []
                    # search Abbreviations
                    dat_abbrev = session.query(JournalsAbbreviations).filter(JournalsAbbreviations.abbreviation.ilike(jname)).all()
                    dat_names = session.query(JournalsNames).filter(or_(JournalsNames.name_english_translated.ilike(jname),
                                                                        JournalsNames.name_native_language.ilike(jname),
                                                                        JournalsNames.name_normalized.ilike(jname))).all()
                    dat_master = session.query(JournalsMaster).filter(or_(JournalsMaster.journal_name.ilike(jname),
                                                                          JournalsMaster.bibstem.ilike(jname))).all()
                    rec_found.extend([rec.masterid for rec in dat_abbrev])
                    rec_found.extend([rec.masterid for rec in dat_names])
                    rec_found.extend([rec.masterid for rec in dat_master])
                    rec_found = list(set(rec_found))
                    for mid in rec_found:
                        dat_master = session.query(JournalsMaster).filter_by(masterid=mid).first()
                        journal_list.append({"bibstem": dat_master.bibstem, "name": dat_master.journal_name, "pubtype": dat_master.pubtype})
                journal_list = sort_journals(journal_list)
            except Exception as err:
                return {'Error': 'Journal search failed',
                        'Error Info': str(err)}, 500
        result_json = {'journal': journal_list}
        return result_json, 200


class Holdings(Resource):

    scopes = []
    rate_limit = [1000, 60 * 60 * 24]
    decorators = [advertise('scopes', 'rate_limit')]

    def get(self, bibstem, volume):
        try:
            q = ADSQuery()
            solr_result = q.search(bibstem, volume)
            data = solr_result.get('response', None)
            if data:
                count = data.get('numFound', 0)
                docs = data.get('docs', [])
                if docs:
                    volume = docs[0].get('volume', None)
                    bibstem = docs[0].get('bibstem', [])
                    if bibstem:
                        bibstem = bibstem[0]
                    holdings = [{'esources': rec.get('esources', None), 'page': rec.get('page', [None])[0]} for rec in docs]
                    result = {'bibstem': bibstem,
                              'volume': volume,
                              'numFound': count,
                              'holdings': holdings}
                else:
                    result = {}
            else:
                result = {}
        except Exception as err:
            return {'Error': 'Holdings search failed',
                    'Error Info': str(err)}, 500
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
                        'Error Info': str(err)}, 500
        return {'refsource': request_json}, 200


class ISSN(Resource):

    scopes = []
    rate_limit = [1000, 60 * 60 * 24]
    decorators = [advertise('scopes', 'rate_limit')]

    def get(self, issn):
        request_json = {}
        if issn:
            try:
                if len(issn) == 8:
                    issn = issn[0:4] + "-" + issn[4:]
                with current_app.session_scope() as session:
                    dat_idents = session.query(JournalsIdentifiers).filter(and_(JournalsIdentifiers.id_value==issn, JournalsIdentifiers.id_type.like("ISSN%"))).first()
                    if dat_idents:
                        pub_abbrev = None
                        masterid = dat_idents.masterid
                        id_value = dat_idents.id_value
                        id_type = dat_idents.id_type
                        dat_master = session.query(JournalsMaster).filter_by(masterid=masterid).first()
                        bibstem = dat_master.bibstem
                        journal_name = dat_master.journal_name
                        dat_titlehist = [rec.toJSON() for rec in session.query(JournalsTitleHistory).filter_by(masterid=masterid).all()]
                        if dat_titlehist:
                            dat_pubhist = []
                            for t in dat_titlehist:
                                publisherid = t.pop('publisherid', None)
                                if publisherid:
                                    pub = session.query(JournalsPublisher).filter_by(publisherid=publisherid).first()
                                    pubhist = {'publisher': pub.toJSON()['pubabbrev'], 'title': t}
                                    dat_pubhist.append(pubhist)
                            for p in dat_pubhist:
                                if not p.get("title", {}).get("year_end", None):
                                    if p.get("publisher", None):
                                        pub_abbrev = p.get("publisher")

                        request_json = {'issn': {'ISSN': id_value,
                                                'ISSN_type': id_type,
                                                'bibstem': bibstem,
                                                'publisher': pub_abbrev,
                                                'journal_name': journal_name}}
            except Exception as err:
                return {'Error': 'issn search failed',
                        'Error Info': str(err)}, 500
        else:
            request_json = {'issn': {}}
        return request_json, 200

class Browse(Resource):

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
                        dat_abbrev = [rec.toJSON()['abbreviation'] for rec in session.query(JournalsAbbreviations).filter_by(masterid=masterid, canonical=True).all()]
                        dat_idents = [rec.toJSON() for rec in session.query(JournalsIdentifiers).filter_by(masterid=masterid).all()]
                        dat_names = [rec.toJSON() for rec in session.query(JournalsNames).filter_by(masterid=masterid).all()]
                        dat_titlehist = [rec.toJSON() for rec in session.query(JournalsTitleHistory).filter_by(masterid=masterid).all()]
                        dat_pubhist = [] 
                        if dat_titlehist:
                            for t in dat_titlehist:
                                publisherid = t.pop('publisherid', None)
                                if publisherid:
                                    pub = session.query(JournalsPublisher).filter_by(publisherid=publisherid).first()
                                    pubhist = {'publisher': pub.toJSON()['pubabbrev'], 'title': t}
                                    dat_pubhist.append(pubhist)

                        # browse return data
                        request_json = {}

                        # master
                        canonical_name = dat_master.toJSON().get("journal_name", "")
                        refereed_status = dat_master.toJSON().get("refereed", "")
                        completeness_fraction = dat_master.toJSON().get("completeness_fraction", "")
                        classic_bibstem = dat_master.toJSON().get("bibstem", "")
                        primary_language = dat_master.toJSON().get("primary_language", "")

                        # abbrevs
                        if dat_abbrev:
                            canonical_abbreviation = dat_abbrev[0]
                        else:
                            canonical_abbreviation = ""

                        # idents
                        if dat_idents:
                            identifiers = dat_idents
                        else:
                            identifiers = []

                        # names
                        if dat_names and type(dat_names[0]) == dict:
                            native_language_title = dat_names[0].get("name_native_language", "")
                            title_language = dat_names[0].get("title_language", "")
                        else:
                            native_language_title = ""
                            title_language = ""

                        # pubhist
                        if dat_pubhist:
                            pubhist = []
                            for p in dat_pubhist:
                                pubhist.append(
                                    {
                                        "publisher": p.get("publisher", ""), 
                                        "start_year": p.get("title", {}).get("year_start", ""),
                                        "start_volume": p.get("title", {}).get("vol_start", "")
                                    }
                                )
                        else:
                            pubhist = []
                        request_json = {
                            "browse": {
                                "canonical_name": canonical_name,
                                "classic_bibstem": classic_bibstem,
                                "canonical_abbreviation": canonical_abbreviation,
                                "primary_language": primary_language,
                                "native_language_title": native_language_title,
                                "title_language": title_language,
                                "completeness_estimate": completeness_fraction,
                                "external_identifiers": identifiers,
                                "publication_history": pubhist
                            }
                        }
                        return request_json, 200

            except Exception as err:
                return {"Error": "browse search failed",
                        "Error Info": str(err)}, 500
        else:
            return {"browse": {}}, 200
