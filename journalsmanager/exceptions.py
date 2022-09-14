# SheetManager Exceptions
class GoogleConnectionException(Exception):
    pass


class InitSheetManagerException(Exception):
    pass


class AuthSheetManagerException(Exception):
    pass


class CreateSheetException(Exception):
    pass


class OpenSheetException(Exception):
    pass


class WriteTableException(Exception):
    pass


class ProtectColumnsException(Exception):
    pass


class FetchTableException(Exception):
    pass


class CheckinProcessException(Exception):
    pass


class TableCheckinException(Exception):
    pass


class FatalCheckinException(Exception):
    pass


class UpdateStatusException(Exception):
    pass


class UpdateRowException(Exception):
    pass


class UpdateTableException(Exception):
    pass


# Holdings Exceptions
class HoldingsQueryException(Exception):
    pass


class BadBibstemException(Exception):
    pass


#Tasks Exceptions
class DBCommitException(Exception):
    """Non-recoverable Error with making database commits."""
    pass


class DBReadException(Exception):
    """Non-recoverable Error with making database selection."""
    pass

class DBClearException(Exception):
    """Non-recoverable Error with clearing a full table (prior to reload)."""
    pass


class InvalidTableException(Exception):
    pass


class WriteDataToSheetException(Exception):
    pass


class TableCheckinException(Exception):
    pass


class TableCheckoutException(Exception):
    pass


class ClearTableException(Exception):
    pass


#Utils Exceptions
class ReadBibstemException(Exception):
    pass


class ReadCompletenessException(Exception):
    pass


class ReadCanonicalException(Exception):
    pass


class ReadEncodingException(Exception):
    pass


class RequestsException(Exception):
    pass


class ReadRefsourcesException(Exception):
    pass


class ExportBibstemsException(Exception):
    pass


class ExportISSNException(Exception):
    pass


class AutocompleteExportException(Exception):
    pass


class BackupFileException(Exception):
    pass


class FileOwnershipError(Exception):
    pass
