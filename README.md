# ADSJournalsDB

ADS Journals Database: backoffice database storage and curation/management
utilities for the curated database of journal-level status, processing, related 
information, and history tables.

## Initial table population via run.py

```
python3 run.py -lf
```

## Table checkout to / checkin from Google Sheets

```
python3 run.py -xo tablename
```

```
python3 run.py -xi tablename
```
