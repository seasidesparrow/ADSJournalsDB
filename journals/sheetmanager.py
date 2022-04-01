import gspread
from datetime import datetime
from journals.exceptions import *

PROTECTED_COLS = 'A1:B99999'
HILIGHT_PROTECTED = {'textFormat': {'bold': True},
                     'backgroundColor': {'red': 1.0,
                                         'green': 0.30,
                                         'blue': 0.30}}
SENSITIVE_COLS = 'C1:C99999'
HILIGHT_SENSITIVE = {'textFormat': {'bold': True},
                     'backgroundColor': {'red': 1.0,
                                         'green': 0.80,
                                         'blue': 0.20}}

def xform_google(indict):
    outdict = {}
    for k, v in indict.items():
        if v == '':
            v = None
        if type(v) == str:
            if v.lower() == 't' or v.lower() == 'true' :
                v = True
            elif v.lower() == 'f' or v.lower() == 'false':
                v = False
        outdict[k] = v
    return outdict


class SpreadsheetManager(object):

    def __init__(self, creds=None, token=None, sheetid=None, folderid=None, editors=[]):
        try:
            self.editors = editors
            self.folderid = folderid
            self.sheetid = sheetid
            self.service = gspread.oauth(credentials_filename=creds,
                                         authorized_user_filename=token)
            if self.sheetid:
                self.open_sheet(sheetid=self.sheetid)
            else:
                self.sheet = None
        except Exception as err:
            raise InitSheetManagerException(err)

    def open_sheet(self, sheetid=None):
        try:
            self.sheet = self.service.open_by_key(sheetid)
        except Exception as err:
            raise OpenSheetException(err)

    def create_sheet(self, title=None, folderid=None):
        try:
            timestamp = '_' + str(datetime.now()).replace(' ','_')
            title = title + timestamp
            self.sheet = self.service.create(title, folder_id=folderid)
            self.sheetid = self.sheet.id
        except Exception as err:
            raise CreateSheetException(err)

    def write_table(self, sheetid=None, data=None, tablename=None, encoding='utf-8'):
        try:
            self.service.import_csv(sheetid, data=data.encode(encoding))
            if self.sheet:
                self._protect_rows(tablename)
        except Exception as err:
            raise WriteTableException(err)

    def _protect_rows(self, tablename=None):
        try:
            if tablename == 'master' or tablename == 'publisher':
                self.sheet.sheet1.add_protected_range('A1:A99999', self.editors)
                self.sheet.sheet1.format('A1:A99999', HILIGHT_PROTECTED)
                self.sheet.sheet1.format('B1:B99999', HILIGHT_SENSITIVE)
            else:
                self.sheet.sheet1.add_protected_range(PROTECTED_COLS, self.editors)
                self.sheet.sheet1.format(PROTECTED_COLS, HILIGHT_PROTECTED)
                self.sheet.sheet1.format(SENSITIVE_COLS, HILIGHT_SENSITIVE)
        except Exception as err:
            raise ProtectColumnsException(err)

    def fetch_table(self):
        try:
            raw_from_google = self.sheet.sheet1.get_all_records(value_render_option='UNFORMATTED_VALUE', numericise_ignore=['all'])
            checkin_data = [xform_google(r) for r in raw_from_google]
            return checkin_data
        except Exception as err:
            raise FetchTableException(err)
