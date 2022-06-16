# ADSJournalsDB

ADS Journals Database: 

This repository consists of two separate packages that both utilize the same models.py (journalsdb.models):

# journalsservice: Deploy with microservices

This service returns data from the journals database for selected queries.

## Summary endpoint

Provides information about the journal/publication, common title spellings,
selected identifiers, and current publisher information when a bibcode
is provided.

Example:

```
curl 'http://api.adsabs.harvard.edu/v1/journals/Summary/ApJ'

{"summary": {"master": {"masterid": 396, "bibstem": "ApJ", "journal_name": "The Astrophysical Journal", "primary_language": null, "multilingual": false, "defunct": false, "pubtype": "Journal", "refereed": "yes"}, "idents": [{"id_type": "ISSN", "id_value": "0004-637X"}, {"id_type": "CROSSREF", "id_value": "4876"}], "abbrev": ["ASTROPHYSICAL JOURNAL", "Ap. J.", "Ap. J. Lett.", "ApJ Letters", "ApJL", "Astrophy. J.", "Astrophys J", "Astrophys J Lett Ed", "Astrophys J.", "Astrophys. J", "Astrophys. J.", "Astrophys. J. :", "Astrophys. J. Let.", "Astrophys. J. Lett.", "Astrophys. J. Letters", "Astrophys. Journ.", "Astrophysic. J.", "Astrophysical J.", "Astrophysical J. US", "Astrophysical Jour.", "Astrophysical Journal Letters", "Astrosphys. J.", "J. Astrophys"], "publisher": [{"pubname": "IOP", "pubaddress": null, "pubcontact": null, "puburl": "https://iopscience.iop.org/journal/0004-637X", "year_start": null, "year_end": null}]}}
```

## Journal endpoint

Attempts to match a bibstem and formal name to a partial match to a journal title.

Example:

```
curl 'http://api.adsabs.harvard.edu/v1/journals/Journal/Astron%20Jour/'

{"journal": [{"bibstem": "AJ", "name": "The Astronomical Journal"}, {"bibstem": "RoAJ", "name": "Romanian Astronomical Journal"}, {"bibstem": "QJRAS", "name": "Quarterly Journal of the Royal Astronomical Society"}, {"bibstem": "JRASC", "name": "Journal of the Royal Astronomical Society of Canada"}, {"bibstem": "JBAA", "name": "Journal of the British Astronomical Association"}, {"bibstem": "IrAJ", "name": "Irish Astronomical Journal"}]}
```

## Holdings endpoint

Returns the number of available fulltext sources for a given bibstem/volume.  It is not intended to give the links, just to indicate whether and how many
fulltext sources are available at the Journal/volume level.

Example:

```
curl 'http://api.adsabs.harvard.edu/v1/journals/Holdings/ApJ/880'

{"holdings": [[{"page": "1", "esources": 60}, {"page": "2", "esources": 60}, {"page": "3", "esources": 60}, {"page": "4", "esources": 60}, {"page": "5", "esources": 60}, {"page": "6", "esources": 60}, {"page": "7", "esources": 60}, {"page": "8", "esources": 60}, {"page": "9", "esources": 60}, {"page": "10", "esources": 60}, {"page": "11", "esources": 60}, {"page": "12", "esources": 60}, {"page": "13", "esources": 60}, {"page": "14", "esources": 48}, {"page": "15", "esources": 60}, {"page": "16", "esources": 60}, {"page": "17", "esources": 48}, {"page": "18", "esources": 60}, {"page": "19", "esources": 60}, {"page": "20", "esources": 60}, {"page": "21", "esources": 60}, {"page": "22", "esources": 60}, {"page": "23", "esources": 60}, {"page": "24", "esources": 60}, {"page": "25", "esources": 60}, {"page": "26", "esources": 60}, {"page": "27", "esources": 60}, {"page": "28", "esources": 60}, {"page": "29", "esources": 60}, {"page": "30", "esources": 60}, {"page": "31", "esources": 48}, {"page": "32", "esources": 60}, {"page": "33", "esources": 60}, {"page": "34", "esources": 60}, {"page": "35", "esources": 60}, {"page": "36", "esources": 60}, {"page": "37", "esources": 60}, {"page": "38", "esources": 60}, {"page": "39", "esources": 48}, {"page": "40", "esources": 60}, {"page": "41", "esources": 60}, {"page": "42", "esources": 60}, {"page": "43", "esources": 48}, {"page": "44", "esources": 60}, {"page": "45", "esources": 60}, {"page": "46", "esources": 60}, {"page": "47", "esources": 60}, {"page": "48", "esources": 60}, {"page": "49", "esources": 60}, {"page": "50", "esources": 48}, {"page": "51", "esources": 60}, {"page": "52", "esources": 48}, {"page": "53", "esources": 48}, {"page": "54", "esources": 60}, {"page": "55", "esources": 60}, {"page": "56", "esources": 60}, {"page": "57", "esources": 60}, {"page": "58", "esources": 60}, {"page": "59", "esources": 60}, {"page": "60", "esources": 60}, {"page": "61", "esources": 48}, {"page": "62", "esources": 48}, {"page": "63", "esources": 60}, {"page": "64", "esources": 60}, {"page": "65", "esources": 60}, {"page": "66", "esources": 60}, {"page": "67", "esources": 60}, {"page": "68", "esources": 60}, {"page": "69", "esources": 60}, {"page": "70", "esources": 60}, {"page": "71", "esources": 60}, {"page": "72", "esources": 60}, {"page": "73", "esources": 48}, {"page": "74", "esources": 48}, {"page": "75", "esources": 48}, {"page": "76", "esources": 60}, {"page": "77", "esources": 48}, {"page": "78", "esources": 60}, {"page": "79", "esources": 60}, {"page": "80", "esources": 48}, {"page": "81", "esources": 60}, {"page": "82", "esources": 60}, {"page": "83", "esources": 60}, {"page": "84", "esources": 60}, {"page": "85", "esources": 60}, {"page": "86", "esources": 60}, {"page": "87", "esources": 60}, {"page": "88", "esources": 60}, {"page": "89", "esources": 60}, {"page": "90", "esources": 60}, {"page": "91", "esources": 48}, {"page": "92", "esources": 60}, {"page": "93", "esources": 60}, {"page": "94", "esources": 60}, {"page": "95", "esources": 60}, {"page": "96", "esources": 48}, {"page": "97", "esources": 60}, {"page": "98", "esources": 60}, {"page": "99", "esources": 60}, {"page": "100", "esources": 48}, {"page": "101", "esources": 48}, {"page": "102", "esources": 60}, {"page": "103", "esources": 60}, {"page": "104", "esources": 60}, {"page": "105", "esources": 60}, {"page": "106", "esources": 48}, {"page": "107", "esources": 60}, {"page": "108", "esources": 60}, {"page": "109", "esources": 60}, {"page": "110", "esources": 60}, {"page": "111", "esources": 60}, {"page": "112", "esources": 60}, {"page": "113", "esources": 48}, {"page": "114", "esources": 60}, {"page": "115", "esources": 60}, {"page": "116", "esources": 60}, {"page": "117", "esources": 60}, {"page": "118", "esources": 60}, {"page": "119", "esources": 60}, {"page": "120", "esources": 60}, {"page": "121", "esources": 60}, {"page": "122", "esources": 60}, {"page": "123", "esources": 48}, {"page": "124", "esources": 60}, {"page": "125", "esources": 60}, {"page": "126", "esources": 60}, {"page": "127", "esources": 60}, {"page": "128", "esources": 60}, {"page": "129", "esources": 60}, {"page": "130", "esources": 60}, {"page": "131", "esources": 60}, {"page": "132", "esources": 60}, {"page": "133", "esources": 60}, {"page": "134", "esources": 60}, {"page": "135", "esources": 60}, {"page": "136", "esources": 48}, {"page": "137", "esources": 60}, {"page": "138", "esources": 60}, {"page": "139", "esources": 60}, {"page": "140", "esources": 60}, {"page": "141", "esources": 48}, {"page": "142", "esources": 60}, {"page": "143", "esources": 60}, {"page": "144", "esources": 60}, {"page": "145", "esources": 60}, {"page": "146", "esources": 60}, {"page": "147", "esources": 48}, {"page": "148", "esources": 60}, {"page": "149", "esources": 60}, {"page": "150", "esources": 60}, {"page": "151", "esources": 60}, {"page": "152", "esources": 48}, {"page": "153", "esources": 60}, {"page": "154", "esources": 60}, {"page": "155", "esources": 60}, {"page": "156", "esources": 60}, {"page": "157", "esources": 60}, {"page": "158", "esources": 60}, {"page": "159", "esources": 60}, {"page": "160", "esources": 48}, {"page": "161", "esources": 48}, {"page": "162", "esources": 48}]]}
```

## Refsources endpoint

Returns a list of where our references for a given Journal come from, if available.

Example:

```
curl 'http://api.adsabs.harvard.edu/v1/journals/Refsource/PhRvX'

{"refsource": {"bibstem": "PhRvX", "volumes": [{"volume": "...1", "year": "2011", "refsources": {"PUBLISHER": 38}}, {"volume": "...2", "year": "2012", "refsources": {"PUBLISHER": 71}}, {"volume": "...3", "year": "2013", "refsources": {"PUBLISHER": 94}}, {"volume": "...4", "year": "2014", "refsources": {"PUBLISHER": 213, "AUTHOR": 1}}, {"volume": "...5", "year": "2015", "refsources": {"PUBLISHER": 175}}, {"volume": "...6", "year": "2016", "refsources": {"PUBLISHER": 198}}, {"volume": "...7", "year": "2017", "refsources": {"PUBLISHER": 218}}, {"volume": "...8", "year": "2018", "refsources": {"PUBLISHER": 277}}, {"volume": "...9", "year": "2019", "refsources": {"PUBLISHER": 238}}, {"volume": "..10", "year": "2020", "refsources": {"PUBLISHER": 279}}, {"volume": "..11", "year": "2021", "refsources": {"PUBLISHER": 267, "AUTHOR": 1}}, {"volume": "..12", "year": "2022", "refsources": {"PUBLISHER": 6}}]}}
```




# journalsmanager: deploy to backoffice

backoffice database storage and curation/management utilities for the curated
database of journal-level status, processing, related information, and history
tables.

This is the package that creates and manages the database, and its connection
with Google Sheets.

## Initial table population via run.py

```
python3 run.py -lf
```

## Clear and reload refsources from autogenerated file:

```
python3 run.py -ls
```

## Clear and reload raster configurations from file:

```
python3 run.py -lr
```

## Table checkout to / checkin from Google Sheets

```
python3 run.py -xo tablename
```

```
python3 run.py -xi tablename
```


