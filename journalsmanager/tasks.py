from __future__ import absolute_import, unicode_literals
from builtins import str
import csv
import io
import json
import os
from kombu import Queue
from journalsmanager import app as app_module
from journalsdb.models import JournalsMaster as master
from journalsdb.models import JournalsMasterHistory as master_hist
from journalsdb.models import JournalsNames as names
from journalsdb.models import JournalsNamesHistory as names_hist
from journalsdb.models import JournalsAbbreviations as abbrevs
from journalsdb.models import JournalsAbbreviationsHistory as abbrevs_hist
from journalsdb.models import JournalsIdentifiers as idents
from journalsdb.models import JournalsIdentifiersHistory as idents_hist
from journalsdb.models import JournalsPublisher as publisher
from journalsdb.models import JournalsPublisherHistory as publisher_hist
from journalsdb.models import JournalsRaster as raster
from journalsdb.models import JournalsRasterHistory as raster_hist
from journalsdb.models import JournalsRasterVolume as rastervol
from journalsdb.models import JournalsRefSource as refsource
from journalsdb.models import JournalsTitleHistory as titlehistory
from journalsdb.models import JournalsTitleHistoryHistory as titlehistory_hist
from journalsdb.models import JournalsEditControl as editctrl
from journalsmanager.utils import *
from journalsmanager.exceptions import *
from journalsmanager.sheetmanager import SpreadsheetManager
from journalsmanager.slackhandler import SlackPublisher
import journalsmanager.refsource as refsrc

TABLES = {'master': master, 'master_hist': master_hist,
          'names': names, 'names_hist': names_hist,
          'abbrevs': abbrevs, 'abbrevs_hist': abbrevs_hist,
          'idents': idents, 'idents_hist': idents_hist,
          'publisher': publisher, 'publisher_hist': publisher_hist,
          'raster': raster, 'raster_hist': raster_hist,
          'titlehistory': titlehistory, 'titlehistory_hist': titlehistory_hist,
          'refsource': refsource, 'rastervol': rastervol}

TABLE_UNIQID = {'master': 'masterid',
                'names': 'nameid',
                'abbrevs': 'abbrevid',
                'idents': 'identid',
                'publisher': 'publisherid',
                'titlehistory': 'titlehistoryid',
                'raster': 'rasterid',
                'rastervol': 'rvolid'}

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))

app = app_module.ADSJournalsCelery('journals', proj_home=proj_home,
                                   config=globals().get('config', {}),
                                   local_config=globals().get('local_config', {}))
logger = app.logger

app.conf.CELERY_QUEUES = (
    Queue('load-datafiles', app.exchange, routing_key='load-datafiles'),
)


def is_type_conversion(newval, oldval):
    if newval != oldval:
        if oldval and type(oldval) == str:
            try:
                if newval and (type(newval) == int or type(newval) == float):
                    if str(newval) == oldval:
                        return True
            except Exception as noop:
                pass
    return False


@app.task(queue='load-datafiles')
def task_setstatus(idno, status_msg):
    with app.session_scope() as session:
        try:
            update = (session.query(editctrl).filter(editctrl.editid==idno).first())
            update.editstatus = status_msg
            session.commit()
        except Exception as err:
            session.rollback()
            session.flush()
            raise UpdateStatusException(err)


@app.task(queue='load-datafiles')
def task_db_bibstems_to_master(recs):
    pubtypes = {'C': 'Conf. Proc.', 'J': 'Journal', 'R': 'Journal'}
    reftypes = {'C': 'na', 'J': 'no', 'R': 'yes'}
    with app.session_scope() as session:
        extant_bibstems = [x[0] for x in session.query(master.bibstem)]
        if recs:
            for r in recs:
                if r[0] not in extant_bibstems:
                    if r[1] in pubtypes:
                        ptype = pubtypes[r[1]]
                    else:
                        ptype = 'Other'
                    if r[1] in reftypes:
                        rtype = reftypes[r[1]]
                    else:
                        rtype = 'na'
                    session.add(master(bibstem=r[0],
                                       journal_name=r[2],
                                       primary_language='en',
                                       pubtype=ptype,
                                       refereed=rtype,
                                       defunct=False,
                                       not_indexed=False))
                else:
                    logger.debug("task_db_bibstems_to_master: Bibstem %s already in master", r[0])
            try:
                session.commit()
            except Exception as err:
                logger.error("Problem with database commit: %s", err)
                raise DBCommitException("Could not commit to db, stopping now.")


@app.task(queue='load-datafiles')
def task_export_classic_files():

    # pending successful returns...
    result_bibstems = 'failed'
    result_issn = 'failed'

    # bibstems
    with app.session_scope() as session:
        result = session.query(master.bibstem,master.pubtype,master.refereed,master.journal_name).filter_by(not_indexed=False).order_by(master.bibstem.asc()).all()
        rows = []
        for r in result:
            (bibstem,pubtype,refereed,journal_name) = r
            rows.append({'bibstem': bibstem, 'pubtype': pubtype, 'refereed': refereed, 'pubname':journal_name})
        try:
            result_bibstems = export_to_bibstemsdat(rows)
        except Exception as err:
            logger.error("Problem exporting master to bibstems.dat: %s" % err)

    # ISSNs
    with app.session_scope() as session:
        result = session.query(idents.id_value, master.bibstem, master.journal_name).join(master, idents.masterid == master.masterid).filter(idents.id_type=='ISSN_print').all()
        rows = []
        for r in result:
            (issn, bibstem, name) = r
            bibstem = bibstem.ljust(5, '.')
            rows.append({'bibstem': bibstem, 'issn': issn, 'name': name})
        try:
            result_issn = export_issns(rows)
        except Exception as err:
            logger.error("Problem exporting ISSNs to files: %s" % err)

    # Publishers
    with app.session_scope() as session:
        result = session.query(master.bibstem, titlehistory.publisherid, publisher.pubabbrev).join(master, titlehistory.masterid == master.masterid).join(publisher, titlehistory.publisherid == publisher.publisherid).all()
        rows = []
        for r in result:
            (bibstem, pubid, pubabbrev) = r
            bibstem = bibstem.ljust(5, '.')
            rows.append({'bibstem': bibstem, 'publisher': pubabbrev})
        try:
            result_publisher = export_publishers(rows)
        except Exception as err:
            logger.error("Problem exporting publishers to file: %s" % err)

    # ISSNs for IngestParser
    with app.session_scope() as session:
        result = session.query(master.bibstem, idents.id_type, idents.id_value).join(master, idents.masterid == master.masterid).all()
        rows = []
        for r in result:
            (bibstem, id_type, id_value) = r
            if "ISSN" in id_type:
                rows.append({"bibstem": bibstem, "id_type": id_type, "id_value": id_value})
        try:
            result_issn_ident = export_issn_identifiers(rows)
        except Exception as err:
            logger.error("Problem exporting issn-identifier mapping to file: %s" % err)

    # return "Bibstems: %s ; ISSNs: %s" % (result_bibstems, result_issn)


@app.task(queue='load-datafiles')
def task_db_load_abbrevs(recs):
    with app.session_scope() as session:
        if recs:
            for r in recs:
                try:
                    session.add(abbrevs(masterid=r[0],
                                        abbreviation=r[1]))
                    session.commit()
                except Exception as err:
                    logger.debug("Problem with abbreviation: %s,%s" %
                                (r[0], r[1]))
        else:
            logger.info("There were no abbreviations to load!")


@app.task(queue='load-datafiles')
def task_db_load_identifier(recs, idtype='ISSN_print'):
    with app.session_scope() as session:
        if recs:
            for r in recs:
                try:
                    session.add(idents(masterid=r[0],
                                       id_type=idtype,
                                       id_value=r[1]))
                    session.commit()
                except Exception as err:
                    logger.debug("Duplicate %s skipped: %s,%s" %
                                (idtype, r[0], r[1]))
                    session.rollback()
                    session.flush()
        else:
            logger.info("No %s loaded!" % idtype)


@app.task(queue='load-datafiles')
def task_db_load_titlehist(recs):
    with app.session_scope() as session:
        if recs:
            for r in recs:
                try:
                    session.add(titlehistory(masterid=r[0],
                                             year_start=r[1],
                                             vol_start=r[2],
                                             vol_end=r[3],
                                             publisherid=r[4],
                                             notes=r[5]))
                    session.commit()
                except Exception as err:
                    logger.debug("Problem loading titlehistory: %s,%s" %
                                (r, err))
                    session.rollback()
                    session.flush()
        else:
            logger.info("No titlehistory loaded.")


@app.task(queue='load-datafiles')
def task_db_load_publisher(recs):
    with app.session_scope() as session:
        if recs:
            for r in recs:
                try:
                    session.add(publisher(pubabbrev=r))
                    session.commit()
                except Exception as err:
                    logger.debug("Problem loading publisher: %s,%s" % (r, err))
                    session.rollback()
                    session.flush()
        else:
            logger.info("There were no publishers to load!")


@app.task(queue='load-datafiles')
def task_db_load_raster(recs):
    with app.session_scope() as session:
        if recs:
            for r in recs:
                if 'label' in r[1]:
                    copyrt_file = r[1]['label']
                else:
                    copyrt_file = ''
                if 'pubtype' in r[1]:
                    pubtype = r[1]['pubtype']
                else:
                    pubtype = ''
                if 'bibstem' in r[1]:
                    bibstem = r[1]['bibstem']
                else:
                    bibstem = ''
                if 'abbrev' in r[1]:
                    abbrev = r[1]['abbrev']
                else:
                    abbrev = ''
                if 'width' in r[1]:
                    width = r[1]['width']
                else:
                    width = ''
                if 'height' in r[1]:
                    height = r[1]['height']
                else:
                    height = ''
                if 'embargo' in r[1]:
                    embargo = r[1]['embargo']
                else:
                    embargo = ''
                if 'options' in r[1]:
                    options = r[1]['options']
                else:
                    options = ''

                try:
                    session.add(raster(masterid=r[0],
                                       copyrt_file=copyrt_file,
                                       pubtype=pubtype,
                                       bibstem=bibstem,
                                       abbrev=abbrev,
                                       width=width,
                                       height=height,
                                       embargo=embargo,
                                       options=options))
                    session.commit()
                    result = session.query(raster.rasterid).filter_by(masterid=r[0]).first()
                except Exception as err:
                    result = None
                    logger.debug("Cant load raster data for (%s, %s): %s" %
                                (r[0], bibstem, err))
                    session.rollback()
                    session.flush()
                try:
                    r[1]['rastervol']
                except Exception as err:
                    result = None
                else:
                    if result:
                        try:
                            for v in r[1]['rastervol']:
                                session.add(rastervol(rasterid=result,
                                                      volume_number=v['range'],
                                                      volume_properties=json.dumps(v['param'])))
                                session.commit()
                        except Exception as err:
                            logger.debug("Cant load rastervolume data for %s: %s" %
                                        (result, err))
                            session.rollback()
                            session.flush()
        else:
            logger.info("There were no raster configs to load!")



@app.task(queue='load-datafiles')
def task_db_get_bibstem_masterid():
    dictionary = {}
    with app.session_scope() as session:
        try:
            for record in session.query(master.masterid,
                                        master.bibstem):
                dictionary[record.bibstem] = record.masterid
        except Exception as err:
            logger.error("Failed to read bibstem-masterid dict from table master: %s" % err)
            raise DBReadException("Could not read from master: %s" % err)
    return dictionary


@app.task(queue='load-datafiles')
def task_db_get_publisherid():
    dictionary = {}
    with app.session_scope() as session:
        try:
            for record in session.query(publisher.publisherid,
                                        publisher.pubabbrev):
                dictionary[publisher.pubabbrev] = publisher.publisherid
        except Exception as err:
            logger.error("Failed to read publisher-publisherid dict from table publisher")
            raise DBReadException("Could not read from publisher: %s" % err)
    return dictionary

@app.task(queue='load-datafiles')
def task_db_clear_refsource():
    with app.session_scope() as session:
        try:
            count = session.query(refsource).delete()
            session.commit()
            logger.info("Refsource table cleared.")
        except Exception as err:
            session.rollback()
            session.commit()
            logger.error("Failed to delete rows from refsource! %s" % err)
            raise DBClearException("Could not clear existing rows from refsource: %s" % str(err))

@app.task(queue='load-datafiles')
def task_db_load_refsource(masterid, refsrc):
    with app.session_scope() as session:
        if masterid and refsrc:
            try:
                refsrc = json.dumps(refsrc.toJSON())
                session.add(refsource(masterid=masterid,
                                      refsource_list=refsrc))
                session.commit()
            except Exception as err:
                logger.warning("Error adding refsources for %s: %s" %
                               (masterid, err))
                session.rollback()
                session.commit()
        else:
            logger.error("No refsource data to load!")
    return


@app.task(queue='load-datafiles')
def task_db_insert_nonindexed_bibstems(nonindexed_dict):
    with app.session_scope() as session:
        for k, v in nonindexed_dict.items():
            try:
                session.add(master(bibstem=k,
                                   journal_name=v['name'],
                                   pubtype='Other',
                                   refereed='na',
                                   not_indexed=True))
                session.commit()
            except Exception as err:
                logger.warning("Error adding nonindexed record %s: %s" % (k, err))
                session.rollback()
                session.commit()
    return


@app.task(queue='load-datafiles')
def task_clear_table(cleartable):
    if cleartable in config.get('CLEARABLE_TABLES', []):
        with app.session_scope() as session:
            try:
                tabl = TABLES[cleartable]
                session.query(tabl).delete(synchronize_session='fetch')
                session.commit()
            except Exception as err:
                session.rollback()
                session.commit()
                raise ClearTableException(err)


@app.task(queue='load-datafiles')
def task_export_table_data(tablename, results):
    with app.session_scope() as session:
        try:
            data = io.StringIO()
            csvout = csv.writer(data, quoting=csv.QUOTE_NONNUMERIC)
            if tablename == 'master':
                csvout.writerow(('masterid','bibstem','journal_name','primary_language','multilingual','defunct','pubtype','refereed','collection','completeness_fraction','notes','not_indexed'))
                if not results:
                    results = session.query(master.masterid, master.bibstem, master.journal_name, master.primary_language, master.multilingual, master.defunct, master.pubtype, master.refereed, master.collection, master.completeness_fraction, master.notes, master.not_indexed).order_by(master.masterid.asc()).all()

            elif tablename == 'names':
                csvout.writerow(('nameid','masterid','bibstem','name_english_translated','title_language','name_native_language','name_normalized'))
                if not results:
                    results = session.query(names.nameid, names.masterid, master.bibstem, names.name_english_translated, names.title_language, names.name_native_language, names.name_normalized).join(master, names.masterid == master.masterid).order_by(names.masterid.asc()).all()

            elif tablename == 'idents':
                csvout.writerow(('identid','masterid','bibstem','id_type','id_value'))
                if not results:
                    results = session.query(idents.identid, idents.masterid, master.bibstem, idents.id_type, idents.id_value).join(master, idents.masterid == master.masterid).order_by(idents.masterid.asc()).all()

            elif tablename == 'abbrevs':
                csvout.writerow(('abbrevid','masterid','bibstem','abbreviation','canonical'))
                if not results:
                    results = session.query(abbrevs.abbrevid, abbrevs.masterid, master.bibstem, abbrevs.abbreviation, abbrevs.canonical).join(master, abbrevs.masterid == master.masterid).order_by(abbrevs.masterid.asc()).all()

            elif tablename == 'publisher':
                csvout.writerow(('publisherid','pubabbrev','pubaddress','pubcontact','puburl','pubextid','pubfullname', 'notes'))
                if not results:
                    results = session.query(publisher.publisherid, publisher.pubabbrev, publisher.pubaddress, publisher.pubcontact, publisher.puburl, publisher.pubextid, publisher.pubfullname, publisher.notes).order_by(publisher.publisherid.asc()).all()

            elif tablename == 'titlehistory':
                csvout.writerow(('titlehistoryid','masterid','bibstem','year_start','year_end','vol_start','vol_end','publisherid','successor_masterid','notes'))
                if not results:
                    results = session.query(titlehistory.titlehistoryid, titlehistory.masterid, master.bibstem, titlehistory.year_start, titlehistory.year_end, titlehistory.vol_start, titlehistory.vol_end, titlehistory.publisherid, titlehistory.successor_masterid, titlehistory.notes).join(master, titlehistory.masterid == master.masterid).order_by(titlehistory.masterid.asc()).all()

            else:
                results = []

            # pad the results with [pad_count] blank lines
            if results:
                column_count = len(results[0])
                blank_row = [''] * column_count
                pad_count = config.get('PADCOUNT_DEFAULT', 0)
                for i in range(pad_count):
                    results.append(blank_row)

            for rec in results:
                csvout.writerow(rec)

        except Exception as err:
            return
        else:
            return data.getvalue()

@app.task(queue='load-datafiles')
def task_checkout_table(tablename, results):

    if tablename.lower() not in app.conf.EDITABLE_TABLES:
        raise InvalidTableException("Tablename %s is not valid" % tablename)

    with app.session_scope() as session:
        try:
            table_record = session.query(editctrl).filter(editctrl.tablename.ilike(tablename), editctrl.editstatus=='active').first()

            if table_record:
                sheet = SpreadsheetManager(creds=app.conf.CREDENTIALS_FILE,
                                           token=app.conf.TOKEN_FILE,
                                           folderid=app.conf.HOME_FOLDER_ID,
                                           editors=app.conf.EDITORS,
                                           sheetid=table_record.editfileid)
                logger.debug("Table %s is already checked out: Time: %s, ID: %s" % (tablename, table_record.created, table_record.editfileid))

            else:
                sheet = SpreadsheetManager(creds=app.conf.CREDENTIALS_FILE,
                                           token=app.conf.TOKEN_FILE,
                                           folderid=app.conf.HOME_FOLDER_ID,
                                           editors=app.conf.EDITORS)
                sheet.create_sheet(title=tablename,
                                   folderid=app.conf.HOME_FOLDER_ID)
                session.add(editctrl(tablename=tablename,
                                     editstatus='active',
                                     editfileid=sheet.sheetid))
                session.commit()

                try:
                    data = task_export_table_data(tablename, results)
                    sheet.write_table(sheetid=sheet.sheetid,
                                      data=data,
                                      tablename=tablename,
                                      encoding='utf-8')
                except Exception as err:
                    raise WriteDataToSheetException(err)
            try:
                fileurl = 'https://docs.google.com/spreadsheets/d/' + sheet.sheetid
                message = 'Table %s checked out to %s' % (tablename, fileurl)
                slack = SlackPublisher()
                slack.publish(message)
            except Exception as err:
                logger.warning('error publishing message to Slack: %s' % err)
        except Exception as err:
            raise TableCheckoutException("Error checking out table %s: %s" % (tablename, err))


@app.task(queue='load-datafiles')
def task_checkin_table(tablename, masterdict, delete_flag=False):

    if tablename.lower() not in app.conf.EDITABLE_TABLES:
        raise InvalidTableException("Tablename %s is not valid" % tablename)

    with app.session_scope() as session:
        try:
            table_record = session.query(editctrl).filter(editctrl.tablename.ilike(tablename), editctrl.editstatus=='active').first()

            if table_record:
                sheet = SpreadsheetManager(creds=app.conf.CREDENTIALS_FILE,
                                           token=app.conf.TOKEN_FILE,
                                           folderid=app.conf.HOME_FOLDER_ID,
                                           editors=app.conf.EDITORS,
                                           sheetid=table_record.editfileid)
                logger.debug("Table %s is currently checked out: Time: %s, ID: %s" % (tablename, table_record.created, table_record.editfileid))

                data = sheet.fetch_table()
                checkin = {'tablename': tablename,
                           'editid': table_record.editid,
                           'data': data
                          }
                try:
                    task_update_table(checkin, masterdict)
                except Exception as err:
                    raise FatalCheckinException(err)

            else:
                logger.debug("Table %s is not checked out." % tablename)

        except Exception as err:
            raise TableCheckinException("Error checking in table %s: %s" % (tablename, err))


@app.task(queue='load-datafiles')
def task_update_table(checkin, masterdict):
    try:
        tablename = checkin['tablename']
        editid = checkin['editid']
        checkin_data = checkin['data']
        create = list()
        modify = list()
        discard = list()
        failure = list()
        status = 'completed'
        # determine what's new and what's an update, and perform updates
        # as they're found
        t = TABLES[tablename]
        tk = TABLE_UNIQID[tablename]
        with app.session_scope() as session:
            for row in checkin_data:
                keyval = row.get(tk, -1)
                try:
                    q = session.query(t).filter(t.__table__.c[tk]==keyval).all()
                    if len(q) == 1:
                        # this is what you want an existing record to be
                        # r is what you're going to modify and update,
                        # s is what you're going to put into _hist.
                        r = q[0]
                        update = 0
                        old_rowdat = {}
                        for k in r.__table__.columns.keys():
                            old_rowdat[k] = getattr(r,k)
                        for k,v in row.items():
                            try:
                                if k != tk and v != getattr(r,k):
                                    # do a quick check to see if the difference
                                    # is due to str(v) != int(v)
                                    if not is_type_conversion(v, getattr(r,k)):
                                        update += 1
                                        setattr(r,k,v)
                            except Exception as noop:
                                # unset columns in a returned row may get here,
                                # but that's ok in most cases.
                                pass
                        if update > 0:
                            # this commits changes made to r
                            try:
                                session.commit()
                                modify.append(old_rowdat)
                            except Exception as err:
                                logger.warning("Problem with row update: %s" % err)
                                session.rollback()
                                session.flush()
                                failure.append(row)

                            # insert the original record into modify list
                            # to be written to _hist
                        else:
                            discard.append(row)
                    elif len(q) == 0:
                        # this is what you want a new record to be
                        create.append(row)
                    else:
                        # this means you have two or more records with the
                        # same key which should not happen unless you're
                        # adding a record to a table that already exists with
                        # the same key.
                        failure.append(row)
                except Exception as err:
                    # something really fundamentally bad happened while
                    # handling this...
                    failure.append(row)

        # create new records
        # with app.session_scope() as session:
            for r in create:
                try:
                    data = t()
                    try:
                        new_masterid = r['masterid']
                        new_bibstem = r['bibstem']
                        if masterdict[new_bibstem]:
                            if r['masterid'] == '' or r['masterid'] == None:
                                r['masterid'] = masterdict[new_bibstem]
                    except Exception as noop:
                        # masterid is not a key in this table, no worries
                        pass
                    for k,v in r.items():
                        if v == '':
                            v = None
                        setattr(data, k, v)
                    session.add(data)
                    session.commit()
                except Exception as err:
                    logger.warning('problem with commit: %s' % err)
                    failure.append(r)
                    session.rollback()
                    session.flush()

            # add modified records to the history table
            for s in modify:
                try:
                    thist = tablename + '_hist'
                    tb = TABLES[thist]
                    data = tb()
                    for k, v in s.items():
                        setattr(data, k, s[k])
                    setattr(data, 'editid', editid)
                    session.add(data)
                    session.commit()
                except Exception as err:
                    logger.warning('problem with commit: %s' % err)
                    failure.append(s)
                    session.rollback()
                    session.flush()

        logger.info('Total records from sheet: %s New; %s Updates; %s Ignored; %s Problematic' % (len(create), len(modify), len(discard), len(failure)))

        # Finishing up: mark table as failed or completed, re-export failed
        # rows, and send messages to slack
        if len(failure) != 0:
            status = 'failed'

        try:
            if editid > 0:
                task_setstatus(editid, status)
                message = 'Table %s checked in from Sheets with status: %s' % (tablename, status)
                slack = SlackPublisher()
                slack.publish(message)
        except Exception as err:
            logger.warning('error publishing message to Slack: %s' % err)

        if len(failure) != 0:
            try:
                re_export = []
                for rec in failure:
                    lineout=[]
                    for k,v in rec.items():
                        lineout.append(v)
                    re_export.append(lineout)
                task_checkout_table(tablename, re_export)
            except Exception as err:
                logger.warning('unable to re-export failed rows: %s' % err)
        else:
            if status == 'completed':
                if tablename == 'master' or tablename == 'idents':
                    try:
                        task_export_classic_files()
                    except Exception as err:
                        raise TableCheckinException("Failed to export bibstems.dat: %s" % err)


    except Exception as err:
        raise UpdateTableException(err)


@app.task(queue='load-datafiles')
def task_export_autocomplete_data():
    try:
        with app.session_scope() as session:
            result = session.query(master.bibstem, master.journal_name, names.name_english_translated, names.name_native_language, names.name_normalized).outerjoin(names, master.masterid == names.masterid).order_by(master.bibstem.asc()).all()
            # result = session.query(master.bibstem,master.pubtype,master.refereed,master.journal_name).filter_by(not_indexed=False).order_by(master.masterid.asc()).all()
            rows = []
            for r in result:
                rows.append({'bibstem': r[0], 'name': r[1],
                             'translated_name': r[2],
                             'native_name':r[3],
                             'transliterated_name': r[4]})
    except Exception as err:
        logger.error("Failed to query autocomplete data from tables: %s" % err)
    else:
        try:
            result_autocomplete = export_to_autocomplete(rows)
        except Exception as err:
            logger.error("Failed to export autocomplete data: %s" % err)


@app.task(queue='load-datafiles')
def task_revert_editid(idno):
    try:
        with app.session_scope() as session:
            result = session.query(editctrl.editid, editctrl.editstatus, editctrl.tablename).filter_by(editid=idno).all()
        if len(result) == 0:
            raise RevertException("History id %s does not exist" % idno)
        elif len(result) > 1:
            raise RevertException("Multiple revisions (%s) with id %s!" % (len(result), idno))
        elif len(result) == 1:
            # you will read from tablename_hist and write to tablename
            tablename = result[0][2]
            tablehist = tablename + '_hist'
            t = TABLES[tablename]
            th = TABLES[tablehist]
            tk = TABLE_UNIQID[tablename]
            with app.session_scope() as session:
                revert_data = session.query(th).filter_by(editid=idno).all()
                for r in revert_data:
                    uid = getattr(r,tk)
                    d = session.query(t).filter(t.__table__.c[tk]==uid).first()
                    for k in d.__table__.columns.keys():
                        dnew = getattr(r,k)
                        setattr(d,k,dnew)
                    try:
                        session.commit()
                    except Exception as err:
                        session.rollback()
                        logger.warning("Unable to rollback editid %s, record %s: %s" % (idno, uid, err))

    except Exception as err:
        raise RevertEditHistoryException(err)
    else:
        try:
            task_setstatus(idno, 'reverted')
        except Exception as err:
            raise DBCommitException("Could not update editstatus: %s" % err)
        else:
            logger.info("Revision %s in editcontrol has been reverted" % idno)

def task_cancel_checkout(idno):
    try:
        status='cancelled'
        task_setstatus(idno, status)
        logger.info("Cancelled checkout editctrl.edit %s" % idno)
    except Exception as err:
        raise CancelCheckoutException("Could not cancel checkout %s: %s" % (idno, err))


def task_abandon_active_checkouts():
    try:
        with app.session_scope() as session:
            table_record = session.query(editctrl.editid).filter(editctrl.editstatus=='active').all()
            for t in table_record:
                idno = getattr(t, 'editid')
                task_setstatus(idno, 'cancelled')
                logger.info("Cancelled checkout editctrl.edit %s" % idno)
    except Exception as err:
        raise AbandonCheckoutsException("Problem cancelling active checkouts: %s" % err)


def task_load_completeness_data():
    try:
        infile = app.conf.get('JDB_DATA_DIR', '/') + app.conf.get('COMPLETENESS_JSON_FILE', '/error.dat')
        critc = app.conf.get('COMPLETENESS_CRIT_VALUE', 0.95)
        with open(infile, 'r') as fj:
            completeness_data = json.load(fj)
    except Exception as err:
        raise LoadCompletenessDataException("Problem loading completeness data from JSON file: %s" % err)
    else:
        for d in completeness_data:
            fraction = d.get('completeness_fraction', 0)
            bibstem = d.get('bibstem', None)
            details = json.dumps(d.get('completeness_details', '{}'))
            if fraction >= critc:
                try:
                    with app.session_scope() as session:
                        q = session.query(master).filter(master.bibstem==bibstem).all()
                        if len(q) != 1:
                            logger.warn("Error: There should be exactly one record that matches the bibstem '%s' in master, not %s!" % (bibstem, len(q)))
                        else:
                            r = q[0]
                            setattr(r, 'completeness_fraction', fraction)
                            setattr(r, 'completeness_details', details)
                            session.commit()
                except Exception as err:
                    session.rollback()
                    session.flush()
                    logger.warn("Can't write completeness data for %s: %s" % (bibstem, err))

def task_delete_masterid(masterid):
    editid = None
    try:
        with app.session_scope() as session:
            qxo = session.query(editctrl).filter(editctrl.editstatus=='active').all()
            if len(qxo) > 0:
                checkouts = [getattr(x, "tablename") for x in qxo]
                raise ActiveCheckoutException("Deletion failed because the following tables are checked out: %s" % (",".join(checkouts)))
            else:
                new_status = editctrl(tablename="master",
                                      editstatus="active",
                                      editfileid="Command line deletion")
                session.add(new_status)
                session.commit()
                editid = new_status.editid

        for dbname in ['names', 'abbrevs', 'idents', 'raster', 'titlehistory', 'refsource', 'master']:
            db = TABLES.get(dbname, None)
            dbhist = TABLES.get(dbname+'_hist', None)

            backup_rows = []
            delete_rows = []
            with app.session_scope() as session:
                q = session.query(db).filter(db.masterid==masterid).all()
                if len(q) > 0:
                    for r in q:
                        data = {}
                        for k in r.__table__.columns.keys():
                            data[k] = getattr(r,k)
                        data['editid'] = editid
                        backup_rows.append(data)
                    delete_rows.append(masterid)

            if backup_rows:
                try:
                    with app.session_scope() as session:
                        if dbname != 'refsource':
                            for row in backup_rows:
                                data = dbhist()
                                for k,v in row.items():
                                    setattr(data, k, v)
                                session.add(data)
                            session.commit()
                        for row in delete_rows:
                            session.query(db).filter(db.masterid==row).delete()
                        session.commit()
                except Exception as err:
                    session.rollback()
                    session.flush()
                    raise Exception("Well, what? %s" % err)
            else:
                logger.debug("Nothing for table %s" % dbname)
        task_setstatus(editid, "completed")
    except Exception as err:
        if editid:
            task_setstatus(editid, "failed")
        raise Exception("Failed to delete masterid %s: %s" % (masterid, err))
