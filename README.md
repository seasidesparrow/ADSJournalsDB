# ADSJournalsDB

ADS Journals Database: 

This repository consists of two separate packages that both utilize the same models.py (journalsdb.models):

# journalsservice: Deploy with microservices

This service returns data from the journals database for selected queries.

## Summary endpoint

Provides information about the journal/publication, common title spellings,
selected identifiers, and current publisher information when a bibstem
is provided.

Example:

```
curl 'http://api.adsabs.harvard.edu/v1/journals/Summary/ApJ'

{"summary": {"master": {"bibstem": "ApJ", "journal_name": "The Astrophysical Journal", "primary_language": "en", "multilingual": false, "defunct": false, "pubtype": "Journal", "refereed": "yes", "collection": null, "notes": null, "not_indexed": false}, "idents": [{"id_type": "ISSN_print", "id_value": "0004-637X"}, {"id_type": "Crossref", "id_value": "4876"}, {"id_type": "ISSN_electronic", "id_value": "1538-4357"}], "abbrev": ["ASTROPHYSICAL JOURNAL", "Ap. J.", "Ap. J. Lett.", "ApJ Letters", "ApJL", "Astrophy. J.", "Astrophys J", "Astrophys J Lett Ed", "Astrophys J.", "Astrophys. J", "Astrophys. J.", "Astrophys. J. :", "Astrophys. J. Let.", "Astrophys. J. Lett.", "Astrophys. J. Letters", "Astrophys. Journ.", "Astrophysic. J.", "Astrophysical J.", "Astrophysical J. US", "Astrophysical Jour.", "Astrophysical Journal Letters", "Astrosphys. J.", "J. Astrophys"], "pubhist": [{"publisher": "IOP", "title": {"year_start": 1895, "year_end": null, "vol_start": "1", "vol_end": "-", "complete": "Y", "successor_masterid": null, "notes": "https://iopscience.iop.org/journal/0004-637X"}}], "names": []}}

```

## Journal endpoint

Attempts to match a bibstem and formal name to a partial match to a journal title.

Example:

```
curl 'http://api.adsabs.harvard.edu/v1/journals/Journal/Astron%20Jour/'

{"journal": [{"bibstem": "AJ", "name": "The Astronomical Journal"}, {"bibstem": "AJS", "name": "The Astronomical Journal Supplement"}, {"bibstem": "RadA", "name": "Radio Astronomy: Journal of the Society of Amateur Radio Astronomers,"}, {"bibstem": "2010AIPC.1283", "name": "Mathematics and Astronomy: A Joint Long Journey"}, {"bibstem": "IrAJ", "name": "Irish Astronomical Journal"}, {"bibstem": "ChSAJ", "name": "Chinese Society of Astronautics Journal"}, {"bibstem": "IrAJS", "name": "Irish Astronomical Journal Supplement"}, {"bibstem": "SerAJ", "name": "Serbian Astronomical Journal"}, {"bibstem": "BUAAJ", "name": "Beijing University Aeronautics and Astronautics Journal"}, {"bibstem": "NUAAJ", "name": "Nanjing University Aeronautics and Astronautics Journal"}, {"bibstem": "JRASC", "name": "Journal of the Royal Astronomical Society of Canada"}, {"bibstem": "CAPJ", "name": "Communicating Astronomy with the Public Journal"}, {"bibstem": "AEdJ", "name": "Astronomy Education Journal"}, {"bibstem": "RoAJ", "name": "Romanian Astronomical Journal"}, {"bibstem": "OAJ", "name": "The Open Astronomy Journal"}, {"bibstem": "JBAA", "name": "Journal of the British Astronomical Association"}, {"bibstem": "BlgAJ", "name": "Bulgarian Astronomical Journal"}, {"bibstem": "PAIJ", "name": "Physics &amp; Astronomy International Journal"}, {"bibstem": "QJRAS", "name": "Quarterly Journal of the Royal Astronomical Society"}, {"bibstem": "AzAJ", "name": "Azerbaijani Astronomical Journal"}]}
```

## Holdings endpoint

Returns the number of available fulltext sources for a given bibstem/volume.  It is not intended to give the links, just to indicate whether and how many
fulltext sources are available at the Journal/volume level.

Example:

```
curl 'http://api.adsabs.harvard.edu/v1/journals/Holdings/ApJ/880'

{"bibstem": "ApJ", "holdings": [{"esources": ["PUB_HTML", "PUB_PDF"], "page": "1"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "2"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "3"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "4"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "5"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "6"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "7"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "8"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "9"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "10"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "11"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "12"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "13"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "14"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "15"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "16"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "17"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "18"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "19"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "20"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "21"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "22"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "23"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "24"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "25"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "26"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "27"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "28"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "29"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "30"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "31"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "32"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "33"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "34"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "35"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "36"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "37"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "38"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "39"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "40"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "41"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "42"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "43"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "44"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "45"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "46"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "47"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "48"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "49"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "50"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "51"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "52"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "53"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "54"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "55"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "56"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "57"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "58"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "59"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "60"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "61"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "62"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "63"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "64"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "65"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "66"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "67"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "68"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "69"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "70"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "71"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "72"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "73"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "74"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "75"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "76"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "77"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "78"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "79"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "80"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "81"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "82"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "83"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "84"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "85"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "86"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "87"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "88"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "89"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "90"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "91"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "92"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "93"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "94"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "95"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "96"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "97"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "98"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "99"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "100"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "101"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "102"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "103"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "104"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "105"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "106"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "107"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "108"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "109"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "110"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "111"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "112"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "113"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "114"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "115"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "116"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "117"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "118"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "119"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "120"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "121"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "122"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "123"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "124"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "125"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "126"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "127"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "128"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "129"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "130"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "131"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "132"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "133"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "134"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "135"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "136"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "137"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "138"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "139"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "140"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "141"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "142"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "143"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "144"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "145"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "146"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "147"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "148"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "149"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "150"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "151"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "152"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "153"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "154"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "155"}, {"esources": ["PUB_HTML", "PUB_PDF"], "page": "156"}, {"esources": ["EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"], "page": "157"}], "numFound": 157, "volume": "880"}


```

## Refsources endpoint

Returns a list of where our references for a given Journal (bibstem) come from, if available.

Example:

```
curl 'http://api.adsabs.harvard.edu/v1/journals/Refsource/PhRvX'

{"refsource": {"bibstem": "PhRvX", "volumes": [{"volume": "1", "year": "2011", "refsources": {"PUBLISHER": 38}}, {"volume": "2", "year": "2012", "refsources": {"PUBLISHER": 71}}, {"volume": "3", "year": "2013", "refsources": {"PUBLISHER": 94}}, {"volume": "4", "year": "2014", "refsources": {"PUBLISHER": 213, "AUTHOR": 1}}, {"volume": "5", "year": "2015", "refsources": {"PUBLISHER": 175}}, {"volume": "6", "year": "2016", "refsources": {"PUBLISHER": 198}}, {"volume": "7", "year": "2017", "refsources": {"PUBLISHER": 218}}, {"volume": "8", "year": "2018", "refsources": {"PUBLISHER": 277}}, {"volume": "9", "year": "2019", "refsources": {"PUBLISHER": 238}}, {"volume": "10", "year": "2020", "refsources": {"PUBLISHER": 279}}, {"volume": "11", "year": "2021", "refsources": {"PUBLISHER": 267, "AUTHOR": 1}}, {"volume": "12", "year": "2022", "refsources": {"PUBLISHER": 114, "AUTHOR": 1}}]}}

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
