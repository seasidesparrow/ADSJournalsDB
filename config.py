LOGGING_LEVEL = 'INFO'
LOG_STDOUT = True

'''
    configuration for ADSJournals database manager
'''
# COLLECTIONS is a list of which collections/databases are stored
COLLECTIONS = ['ast', 'phy', 'gen', 'pre']

BIBSTEM_VOLUMES = ['book', 'conf', 'work', 'proc', 'rept', 'symp', 'prop']

# list of tables that can be exported to google sheets
EDITABLE_TABLES = ['abbrevs', 'master', 'idents', 'names', 'publisher', 'titlehistory']

# list of tables that can be automatically dropped and reloaded
CLEARABLE_TABLES = ['raster', 'rastervol', 'refsource']


# Data files used to initialize the DB (run.py -lf option)
# DATA_DIRECTORY:
JDB_DATA_DIR = '/data_source/'

# BIBSTEMS has bibstem, R/J/C/etc, and canonical name
BIBSTEMS_FILE = '/bibstems.dat'

# PUBLISHER has bibstem, publisher abbrev
BIBSTEM_PUBLISHER_FILE = '/publisher_bibstem.dat'
 
# JOURNAL_ABBREV has bibstem and multiple title abbreviations (e.g.
# A&A, AA, Astron. & Astrophys.)
JOURNAL_ABBREV_FILE = '/journals_abbrev.dat'

# some bibstems are tracked for disambiguation but aren't indexed
NONINDEXED_FILE = '/non_indexed.txt'

# ISSN - Bibstem mappings
JOURNAL_ISSN_FILE = '/journal_issn'
ISSN_JOURNAL_FILE = '/issn2journal'

# Canonical Abbreviation - Bibstem mapping
BIBSTEM_CANONICAL_ABBREV = '/bibstem_canonical_abbrev.dat'

# ISSN-Identifier mapping for ADSManualParser
ISSN_IDENTIFIER = '/issn_identifiers'

# Journal name data for nodejs autocomplete function
JOURNALS_AUTOCOMPLETE_FILE = '/journals_autocomplete.json'

# Backoffice ranking data files for nodejs autocomplete function
CANONICAL_BIBS = '/canonical_bibcodes.current'
CITATION_COUNTS = '/citation.counts'

# REFSOURCE_FILE
BIB_TO_REFS_FILE = '/citing2file.dat'

# RASTERIZING.xml directory
RASTER_CONFIG_DIR = '/raster_config/'

# Completeness statistics from completeness_statistics_pipeline
# If CRIT_VALUE is 0.0, load statistics for all journals
COMPLETENESS_JSON_FILE = '/completeness_export.json'
COMPLETENESS_CRIT_VALUE = 0.0

#------------------------------------------------------

'''
   configuration for Google Sheets service
'''

SECRETS_PATH = '/secrets/'

CREDENTIALS_FILE = SECRETS_PATH + 'foo.dat'

TOKEN_FILE = SECRETS_PATH + 'bar.dat'

HOME_FOLDER_ID = 'dummy_folder_id'

EDITORS = ['mygmailaccount@gmail.com']

PADCOUNT_DEFAULT = 500

#----------------------------------------------------------

'''
    configuration for journalsdb_service microservice
'''
VERSION = 'v1.0'

# Holdings ADS query config
HOLDINGS_ADS_QUERY_URL = 'https://api.adsabs.harvard.edu/v1/search/query'

# Specify the maximum number of bibstems the microservice can query
JOURNALSDB_MAX_SUBMITTED = 100

# Specify where the journals database lives
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://user:pwd@localhost:5432/journals'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

DISCOVERER_PUBLISH_ENDPOINT = '/resources'

# Advertise its own route within DISCOVERER_PUBLISH_ENDPOINT
DISCOVERER_SELF_PUBLISH = False
