'''
No.
'''
from __future__ import print_function
import argparse
import json
import os
from adsputils import setup_logging, load_config
from journalsmanager import tasks
from journalsmanager import utils

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

    parser.add_argument('-lr',
                        '--load-rasterconf',
                        dest='load_raster',
                        action='store_true',
                        help='Load rasterization control parameters')

    parser.add_argument('-ls',
                        '--load-refsources',
                        dest='load_refsources',
                        action='store_true',
                        help='Load refsources from citing2file.dat')

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

    parser.add_argument('-ac',
                        '--autocomplete-data',
                        dest='autocomplete',
                        action='store_true',
                        default=False,
                        help='Export journal name & bibstem data to json')

    parser.add_argument('-re',
                        '--revert-edit',
                        dest='revertid',
                        action='store',
                        default=None,
                        help='Undo edit # from editcontrol')

    parser.add_argument('-cc',
                        '--cancel-checkout',
                        dest='cancelxo',
                        action='store',
                        default=None,
                        help='Cancel active export id # from editcontrol')

    parser.add_argument('-aa',
                        '--abandon-all',
                        dest='abandonall',
                        action='store_true',
                        default=False,
                        help='Abandon all active sheet exports (use with caution -- this will abort **ALL** sheets currently being edited!)')

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
    Completeness loads multiple tables: publisher, idents, titlehistory
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
            completeness_fraction = value.get('completeness_fraction', None)
            url = value.get('url', None)
            notes = '; '.join([value.get('notes', None), url]).strip('; ')
            recsh.append((mid,year_start,vol_start,vol_end,completeness_fraction,pid,notes))
    if recsh:
        tasks.task_db_load_titlehist(recsh)


def load_refsources(masterdict):
    refsources = utils.create_refsource()
    missing_stems = []
    loaded_stems = []

    if refsources:
        try:
            tasks.task_db_clear_refsource()
        except Exception as err:
            logger.warning("Unable to clear existing refsources table: %s" % err)
        else:
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


def load_nonindexed():
    try:
        nonindexed = utils.read_nonindexed()
        tasks.task_db_insert_nonindexed_bibstems(nonindexed)
    except Exception as err:
        logger.error("Failed to load nonindexed bibstems from %s: %s" % ((config.get('JDB_DATA_DIR','/') + config.get('NONINDEXED_FILE', 'error.file')), err))
    else:
        masterdict = tasks.task_db_get_bibstem_masterid()
        recsi = []
        for k, v in nonindexed.items():
            try:
                mid = masterdict[k]
            except Exception as err:
                logger.warning("missing masterid for bibstem %s" % k)
            else:
                r = {'masterid': mid, 'id_type': 'ISSN_print', 'id_value': v['issn']}
                recsi.append(r)
        if len(recsi) != len(nonindexed.keys()):
            logger.warning("Lines were skipped when reading ISSNs from file")
        if recsi:
            checkin = {'tablename': 'idents',
                       'editid': -1,
                       'data': recsi
                      }
            status = tasks.task_update_table(checkin, masterdict)

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
        tasks.task_checkout_table(tablename, [])
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
            load_nonindexed()
        except Exception as err:
            logger.warning("Error loading auxilliary tables: %s" % err)


def main():
    '''
    No.
    '''

    args = get_arguments()

    # These don't require masterdict
    if args.load_full:
        load_full_database()

    elif args.abandonall:
        tasks.task_abandon_active_checkouts()

    elif args.checkout_table:
        checkout_table(args.checkout_table)

    elif args.dump_classic:
        tasks.task_export_classic_files()

    elif args.autocomplete:
        tasks.task_export_autocomplete_data()

    elif args.revertid:
        tasks.task_revert_editid(args.revertid)

    elif args.cancelxo:
        tasks.task_cancel_checkout(args.cancelxo)

    else:
        # These do require masterdict
        try:
            masterdict = tasks.task_db_get_bibstem_masterid()
        except Exception as err:
            logger.warning("Error loading masterdict: %s" % err)
        else:

            if args.checkin_table:
                try:
                    checkin_table(args.checkin_table, masterdict, args.delete_flag)
                except Exception as err:
                    logger.warning("Error checking in table %s: %s" % (args.checkin_table, err))

            elif args.load_raster:
                try:
                    tasks.task_clear_table('rastervol')
                    tasks.task_clear_table('raster')
                except Exception as err:
                    logger.warning("Error clearing raster tables: %s" % err)
                else:
                    load_rasterconfig(masterdict)

            elif args.load_refsources:
                try:
                    tasks.task_clear_table('refsource')
                except Exception as err:
                    logger.warning("Error clearing refsource table: %s" % err)
                else:
                    load_refsources(masterdict)


if __name__ == '__main__':
    main()
