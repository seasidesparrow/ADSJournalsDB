'''
No.
'''
from __future__ import print_function
import argparse
import json
import os
from adsputils import setup_logging, load_config
from journals import tasks
from journals import utils

proj_home = os.path.realpath(os.path.dirname(__file__))
config = load_config(proj_home=proj_home)
logger = setup_logging('run.py', proj_home=proj_home,
                       level=config.get('LOGGING_LEVEL', 'INFO'),
                       attach_stdout=config.get('LOG_STDOUT', False))



def get_arguments():
    '''
    No.
    '''

    parser = argparse.ArgumentParser(description='Command line options.')

    parser.add_argument('-lf',
                        '--load-full',
                        dest='load_full',
                        action='store_true',
                        help='Load all files from text / classic')

    parser.add_argument('-dc',
                        '--dump-classic-files',
                        dest='dump_classic',
                        action='store_true',
                        help='Dump table data to files used for classic')

    parser.add_argument('-xi',
                        '--checkin-table',
                        dest='checkin_table',
                        action='store',
                        default=None,
                        help='Check IN table TABLE from GSheets')

    parser.add_argument('-xo',
                        '--checkout-table',
                        dest='checkout_table',
                        action='store',
                        default=None,
                        help='Check OUT table TABLE to GSheets')

    parser.add_argument('-xd',
                        '--delete-checkin-sheet',
                        dest='delete_flag',
                        action='store_true',
                        default=False,
                        help='Delete checked-in sheet from Google')

    args = parser.parse_args()
    return args


def load_master():
    '''
    No.
    '''
    bibstems = utils.read_bibstems_list()
    recs = []
    for key, value in list(bibstems.items()):
        bibstem = key
        pubtype = value['type']
        journal_name = value['pubname']
        recs.append((bibstem, pubtype, journal_name))
    if recs:
        logger.debug("Inserting %s bibstems into Master", len(recs))
        tasks.task_db_bibstems_to_master(recs)
    else:
        logger.debug("No bibstems to insert")
    return


def load_rasterconfig(masterdict):
    '''
    No.
    '''
    try:
        recsr = utils.read_raster_xml(masterdict)
    except Exception as e:
        logger.warning('error in utils.read_raster_xml: %s' % e)
    else:
        logger.debug("Inserting %s raster config records" % len(recsr))
        try:
            tasks.task_db_load_raster(recsr)
        except Exception as err:
            logger.warning("Could not load raster config: %s" % err)
    return


def load_abbreviations(masterdict):
    '''
    No.
    '''
    abbrevs = utils.read_abbreviations_list()
    recs = []
    for key, value in list(abbrevs.items()):
        try:
            if key in masterdict:
                logger.debug("Got masterid for bibstem %s", key)
                masterid = masterdict[key]
                for attrib in value:
                    recs.append((masterid, attrib))
            else:
                logger.debug("No masterid for bibstem %s", key)
        except Exception as err:
            logger.warning("Error with bibstem %s", key)
            logger.warning("Error: %s", err)
    if recs:
        logger.debug("Inserting %s abbreviations into Abbreviations",
                     len(recs))
        try:
            tasks.task_db_load_abbrevs(recs)
        except Exception as err:
            logger.warning("Could not load abbreviations: %s" % err)
    else:
        logger.debug("There are no abbreviations to load.")
    return


def load_completeness(masterdict):
    '''
    Completeness loads multiple tables: publisher, idents, status
    '''
    pub_dict = utils.read_complete_csvs()
    recsp = []
    for key, value in list(pub_dict.items()):
        if value.get('publisher', None):
            recsp.append(value['publisher'])
    if recsp:
        recsp = list(set(recsp))
        recsp.sort()
        tasks.task_db_load_publisher(recsp)
    publisherdict = tasks.task_db_get_publisherid()

    recsi = []
    recsx = []
    for key, value in list(pub_dict.items()):
        if key in masterdict:
            mid = masterdict[key]
            if value.get('issn', None):
                recsi.append((mid, value['issn']))
            if value.get('xref', None):
                recsx.append((mid, value['xref']))
    if recsi:
        tasks.task_db_load_identifier(recsi, idtype='ISSN_print')
    if recsx:
        tasks.task_db_load_identifier(recsx, idtype='Crossref')
        
    recsh = []
    for key, value in list(pub_dict.items()):
        if key in masterdict:
            mid = masterdict[key]
            pub = value.get('publisher', None)
            pid = publisherdict.get(pub, None)
            year_start = value.get('startyear', None)
            vol_start = value.get('startvol', None)
            vol_end = value.get('endvol', None)
            complete = value.get('complete', None)
            url = value.get('url', None)
            notes = '; '.join([value.get('notes', None), url]).strip('; ')
            recsh.append((mid,year_start,vol_start,vol_end,complete,pid,notes))
    if recsh:
        tasks.task_db_load_titlehist(recsh)


def load_refsources(masterdict):
    refsources = utils.create_refsource()
    missing_stems = []
    loaded_stems = []

    if refsources:
        for bibstem, refsource in refsources.items():
            try:
                bibstem = bibstem.rstrip('.')
                masterid = masterdict[bibstem]
            except Exception as err:
                logger.debug("missing masterdict bibstem: (%s)" % bibstem)
                missing_stems.append(bibstem)
            else:
                tasks.task_db_load_refsource(masterid,refsource)
                loaded_stems.append(bibstem)

        logger.debug("Loaded bibstems: %s\tMissing bibstems: %s" % (len(loaded_stems), len(missing_stems)))


def load_issn(masterdict):
    try:
        issn_dict = utils.read_issn_file()
        recsif = []
        for k, v in issn_dict.items():
            try:
                mid = masterdict[k]
                recsif.append((mid, v))
            except Exception as noop:
                logger.debug("bibstem %s is not in masterdict, skipping" % k)
        if len(recsi) != len(issn_dict.keys()):
            logger.warning("Lines were skipped when reading ISSNs from file")
        if recsi:
            tasks.task_db_upsert_issn(recsi)
    except Exception as err:
        logger.error("Failed to load ISSNs from %s: %s" % (config.get('JOURNAL_ISSN_FILE', None), err))

    return


def checkin_table(tablename, masterdict, delete_flag):
    try:
        tasks.task_checkin_table(tablename, masterdict, delete_flag=delete_flag)
    except Exception as err:
        logger.error("Unable to checkin table %s: %s" % (tablename, err))
        return
    else:
        logger.warning("Table %s successfully checked in from Sheets" % tablename)


def checkout_table(tablename):
    try:
        tasks.task_checkout_table(tablename)
    except Exception as err:
        logger.warning("Unable to checkout table %s: %s" % (tablename, err))
    else:
        logger.warning("Table %s is available in Sheets" % tablename)


def load_full_database():
    # This is used to create a database from scratch from all
    # input files: master, abbreviations, completeness (publisher, ids), raster,
    # refsources.

    try:
        load_master()
        masterdict = tasks.task_db_get_bibstem_masterid()
        logger.debug("masterdict has %s records", len(masterdict))
    except Exception as err:
        logger.warning("Error loading master table: %s" % err)
    else:
        try:
            load_completeness(masterdict)
            load_abbreviations(masterdict)
            load_rasterconfig(masterdict)
            load_refsources(masterdict)
        except Exception as err:
            logger.warning("Error loading auxilliary tables: %s" % err)


def main():
    '''
    No.
    '''

    args = get_arguments()

    if args.load_full:
        load_full_database()
    else:
        if args.checkin_table:
            try:
                masterdict = tasks.task_db_get_bibstem_masterid()
                checkin_table(args.checkin_table, masterdict, args.delete_flag)
            except Exception as err:
                logger.warning("Error checking in table %s: %s" % (args.checkin_table, err))
        
        if args.checkout_table:
            checkout_table(args.checkout_table)

        if args.dump_classic:
            tasks.task_export_classic_files()


if __name__ == '__main__':
    main()
