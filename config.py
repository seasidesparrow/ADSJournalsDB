LOGGING_LEVEL = 'WARNING'
LOG_STDOUT = True

'''
    configuration for ADSJournals database
'''
# COLLECTIONS is a list of which collections/databases are stored
COLLECTIONS = ['ast', 'phy', 'gen', 'pre']

# DATA_DIRECTORY:
JDB_DATA_DIR = '/data_source/'

# BIBSTEMS has bibstem, R/J/C/etc, and canonical name
BIBSTEMS_FILE = JDB_DATA_DIR + 'bibstems.dat'

# JOURNAL_ABBREV has bibstem and multiple title abbreviations (e.g.
# A&A, AA, Astron. & Astrophys.)
JOURNAL_ABBREV_FILE = JDB_DATA_DIR + 'journals_abbrev.dat'

JOURNAL_ISSN_FILE = JDB_DATA_DIR + 'journal_issn'
ISSN_JOURNAL_FILE = JDB_DATA_DIR + 'issn2journal'
CANONICAL_BIB_FILE = JDB_DATA_DIR + 'bib2accno.dat'

NONINDEXED_FILE = JDB_DATA_DIR + 'non_indexed.txt'

# RASTERIZING.xml directory
RASTER_CONFIG_DIR = JDB_DATA_DIR + 'raster_config/'

# REFSOURCE_FILE
BIB_TO_REFS_FILE = JDB_DATA_DIR + 'citing2file.dat'

BIBSTEM_VOLUMES = ['book', 'conf', 'work', 'proc', 'rept', 'symp', 'prop']

EDITABLE_TABLES = ['abbrevs', 'master', 'idents', 'names', 'publisher', 'titlehistory']

CLEARABLE_TABLES = ['raster', 'rastervol', 'refsource']

'''
   configuration for Google Sheets service
'''
SECRETS_PATH = '/secrets/'

CREDENTIALS_FILE = SECRETS_PATH + 'foo.dat'

TOKEN_FILE = SECRETS_PATH + 'bar.dat'

HOME_FOLDER_ID = 'dummy_folder_id'

EDITORS = ['mygmailaccount@gmail.com']

PADCOUNT_DEFAULT = 50

#----------------------------------------------------------

'''
    configuration for journalsdb_service microservice
'''
# Holdings query config
SERVICE_TOKEN = None
HOLDINGS_ADS_QUERY_URL = 'https://api.adsabs.harvard.edu/v1/search/query'

# Specify the maximum number of bibstems the microservice can query
JOURNALSDB_MAX_SUBMITTED = 100

# Specify where the journals database lives
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://user:pwd@localhost:5432/journals'
#SQLALCHEMY_ECHO = False
DISCOVERER_PUBLISH_ENDPOINT = '/resources'

# Advertise its own route within DISCOVERER_PUBLISH_ENDPOINT
DISCOVERER_SELF_PUBLISH = False

