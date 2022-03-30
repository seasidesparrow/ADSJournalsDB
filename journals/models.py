from adsputils import get_date, UTCDateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Table, Column, Integer, Numeric, String, TIMESTAMP,
                        ForeignKey, Boolean, Float, Text, UniqueConstraint)
from sqlalchemy.dialects.postgresql import ENUM

Base = declarative_base()


class JournalsMaster(Base):
    __tablename__ = 'master'

    pub_type = ENUM('Journal', 'Conf. Proc.', 'Monograph', 'Book',
                    'Software', 'Other', name='pub_type')
    ref_status = ENUM('yes', 'no', 'partial', 'na', name='ref_status')

    masterid = Column(Integer, primary_key=True, unique=True)
    bibstem = Column(String, unique=True, nullable=False)
    journal_name = Column(String, nullable=False)
    primary_language = Column(String, nullable=False, default='en')
    multilingual = Column(Boolean, default=False)
    defunct = Column(Boolean, default=False)
    pubtype = Column(pub_type, nullable=False)
    refereed = Column(ref_status, nullable=False)
    collection = Column(String, nullable=True)
    notes = Column(Text)
    not_indexed = Column(Boolean, default=False)
    created = Column(UTCDateTime, default=get_date)
    updated = Column(UTCDateTime, onupdate=get_date)

    def __repr__(self):
        return "master.masterid='{self.masterid}'".format(self=self)

    def toJSON(self):
        return {'masterid': self.masterid,
                'bibstem': self.bibstem,
                'journal_name': self.journal_name,
                'primary_language': self.primary_language,
                'multilingual': self.multilingual,
                'defunct': self.defunct,
                'pubtype': self.pubtype,
                'refereed': self.refereed,
                'collection': self.collection,
                'notes': self.notes,
                'not_indexed': self.not_indexed,
                'created': self.created,
                'updated': self.updated}


class JournalsMasterHistory(Base):
    __tablename__ = 'master_hist'

    histid = Column(Integer, primary_key=True, autoincrement=True,
                    unique=True, nullable=False)
    editid = Column(Integer)
    masterid = Column(Integer)
    bibstem = Column(String)
    journal_name = Column(String)
    primary_language = Column(String)
    multilingual = Column(Boolean)
    defunct = Column(Boolean)
    pubtype = Column(String)
    refereed = Column(String)
    collection = Column(String)
    notes = Column(Text)
    not_indexed = Column(Boolean)
    created = Column(UTCDateTime)
    updated = Column(UTCDateTime)
    superseded = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "master_hist.masterid='{self.masterid}'".format(self=self)


class JournalsNames(Base):
    __tablename__ = 'names'

    nameid = Column(Integer, primary_key=True, autoincrement=True,
                    unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    name_english_translated = Column(String, nullable=False)
    title_language = Column(String, nullable=False)
    name_native_language = Column(String, nullable=False)
    name_normalized = Column(String, nullable=False)
    created = Column(UTCDateTime, default=get_date)
    updated = Column(UTCDateTime, onupdate=get_date)

    def __repr__(self):
        return "names.masterid='{self.masterid}'".format(self=self)

    def toJSON(self):
        return {'nameid': self.nameid,
                'masterid': self.masterid,
                'name_english_translated': self.name_english_translated,
                'title_language': self.title_language,
                'name_native_language': self.name_native_language,
                'name_normalized': self.name_normalized,
                'created': self.created,
                'updated': self.updated}


class JournalsNamesHistory(Base):
    __tablename__ = 'names_hist'

    histid = Column(Integer, primary_key=True, autoincrement=True,
                    unique=True, nullable=False)
    editid = Column(Integer)
    nameid = Column(Integer)
    masterid = Column(Integer)
    name_english_translated = Column(String)
    title_language = Column(String)
    name_native_language = Column(String)
    name_normalized = Column(String)
    created = Column(UTCDateTime)
    updated = Column(UTCDateTime)
    superseded = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "names_hist.masterid='{self.masterid}'".format(self=self)


class JournalsAbbreviations(Base):
    __tablename__ = 'abbrevs'

    abbrevid = Column(Integer, primary_key=True, autoincrement=True,
                      unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    abbreviation = Column(String)
    created = Column(UTCDateTime, default=get_date)
    updated = Column(UTCDateTime, onupdate=get_date)

    def __repr__(self):
        return "abbrevs.abbrevid='{self.abbrevid}'".format(self=self)

    def toJSON(self):
        return {'abbrevid': self.abbrevid,
                'masterid': self.masterid,
                'abbreviation': self.abbreviation,
                'created': self.created,
                'updated': self.updated}


class JournalsAbbreviationsHistory(Base):
    __tablename__ = 'abbrevs_hist'

    histid = Column(Integer, primary_key=True, autoincrement=True,
                    unique=True, nullable=False)
    editid = Column(Integer)
    abbrevid = Column(Integer)
    masterid = Column(Integer)
    abbreviation = Column(String)
    created = Column(UTCDateTime)
    updated = Column(UTCDateTime)
    superseded = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "abbrevs.abbrevid='{self.abbrevid}'".format(self=self)


class JournalsIdentifiers(Base):
    __tablename__ = 'idents'

    identid = Column(Integer, primary_key=True, autoincrement=True,
                     unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    id_type = Column(String)
    id_value = Column(String)
    created = Column(UTCDateTime, default=get_date)
    updated = Column(UTCDateTime, onupdate=get_date)

    def __repr__(self):
        return "idents.identid='{self.identid}'".format(self=self)

    def toJSON(self):
        return{'identid': self.identid,
               'masterid': self.masterid,
               'id_type': self.id_type,
               'id_value': self.id_value,
               'created': self.created,
               'updated': self.updated}


class JournalsIdentifiersHistory(Base):
    __tablename__ = 'idents_hist'

    histid = Column(Integer, primary_key=True, autoincrement=True,
                    unique=True, nullable=False)
    editid = Column(Integer)
    identid = Column(Integer)
    masterid = Column(Integer)
    id_type = Column(String)
    id_value = Column(String)
    created = Column(UTCDateTime)
    updated = Column(UTCDateTime)
    superseded = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "idents_histidentid='{self.identid}')".format(self=self)


class JournalsPublisher(Base):
    __tablename__ = 'publisher'

    publisherid = Column(Integer, primary_key=True, autoincrement=True,
                         unique=True, nullable=False)
    pubname = Column(String)
    pubaddress = Column(String)
    pubcontact = Column(Text)
    puburl = Column(String)
    pubextid = Column(String)
    notes = Column(Text)
    created = Column(UTCDateTime, default=get_date)
    updated = Column(UTCDateTime, onupdate=get_date)

    def __repr__(self):
        return "publisher.publisherid='{self.publisherid}'".format(self=self)

    def toJSON(self):
        return {'publisherid': self.publisherid,
                'pubname': self.pubname,
                'pubaddress': self.pubaddress,
                'pubcontact': self.pubcontact,
                'puburl': self.puburl,
                'pubextid': self.pubgrid,
                'notes': self.notes,
                'created': self.created,
                'updated': self.updated}

class JournalsPublisherHistory(Base):
    __tablename__ = 'publisher_hist'

    histid = Column(Integer, primary_key=True, unique=True)
    editid = Column(Integer)
    publisherid = Column(Integer)
    pubname = Column(String)
    pubaddress = Column(String)
    pubcontact = Column(Text)
    puburl = Column(String)
    pubextid = Column(String)
    notes = Column(Text)
    created = Column(UTCDateTime)
    updated = Column(UTCDateTime)
    superseded = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "publisher_hist.publisherid='{self.publisherid}'"\
               .format(self=self)


class JournalsTitleHistory(Base):
    __tablename__ = 'titlehistory'

    titlehistoryid = Column(Integer, primary_key=True, autoincrement=True,
                       unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    year_start = Column(Integer)
    year_end = Column(Integer)
    complete = Column(Text)
    publisherid = Column(Integer, ForeignKey('publisher.publisherid'))
    successor_masterid = Column(Integer)
    notes = Column(String)
    created = Column(UTCDateTime, default=get_date)
    updated = Column(UTCDateTime, onupdate=get_date)

    def __repr__(self):
        return "titlehistory.titlehistoryid='{self.titlehistoryid}'".format(self=self)

    def toJSON(self):
        return {'titlehistoryid': self.titlehistoryid,
                'masterid': self.masterid,
                'year_start': self.year_start,
                'year_end': self.year_end,
                'complete': self.complete,
                'publisherid': self.publisherid,
                'successor_masterid': self.successor_masterid,
                'notes': self.notes,
                'created': self.created,
                'updated': self.updated}

class JournalsTitleHistoryHistory(Base):
    __tablename__ = 'titlehistory_hist'

    histid = Column(Integer, primary_key=True, autoincrement=True,
                    unique=True, nullable=False)
    editid = Column(Integer)
    titlehistoryid = Column(Integer)
    masterid = Column(Integer)
    year_start = Column(Integer)
    year_end = Column(Integer)
    complete = Column(Text)
    publisherid = Column(Integer)
    successor_masterid = Column(Integer)
    notes = Column(String)
    created = Column(UTCDateTime)
    updated = Column(UTCDateTime)
    superseded = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "pubhist_hist.pubhistid='{self.pubhistid}')".format(self=self)


class JournalsRaster(Base):
    __tablename__ = 'raster'

    rasterid = Column(Integer, primary_key=True, autoincrement=True,
                      unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                       primary_key=True, nullable=False)
    copyrt_file = Column(String, nullable=True)
    pubtype = Column(String, nullable=True)
    bibstem = Column(String, nullable=True)
    abbrev = Column(String, nullable=True)
    width = Column(String, nullable=True)
    height = Column(String, nullable=True)
    embargo = Column(String, nullable=True)
    options = Column(String, nullable=True)
    created = Column(UTCDateTime, default=get_date)
    updated = Column(UTCDateTime, onupdate=get_date)

    def __repr(self):
        return "raster.rasterid='{self.rasterid}'".format(self=self)

    def toJSON(self):
        return{'rasterid': self.rasterid,
               'masterid': self.masterid,
               'copyrt_file': self.copyrt_file,
               'pubtype': self.pubtype,
               'bibstem': self.bibstem,
               'abbrev': self.abbrev,
               'width': self.width,
               'height': self.height,
               'embargo': self.embargo,
               'options': self.options,
               'created': self.created,
               'updated': self.updated}


class JournalsRasterHistory(Base):
    __tablename__ = 'raster_hist'

    histid = Column(Integer, primary_key=True, autoincrement=True,
                    unique=True, nullable=False)
    editid = Column(Integer)
    rasterid = Column(Integer)
    masterid = Column(Integer)
    copyrt_file = Column(String)
    pubtype = Column(String)
    bibstem = Column(String)
    abbrev = Column(String)
    width = Column(String)
    height = Column(String)
    embargo = Column(String)
    options = Column(String)
    created = Column(UTCDateTime)
    updated = Column(UTCDateTime)
    superseded = Column(UTCDateTime, default=get_date)

    def __repr(self):
        return "raster.rasterid='{self.rasterid}'".format(self=self)


class JournalsRasterVolume(Base):
    __tablename__ = 'rastervolume'
    rvolid = Column(Integer, primary_key=True, autoincrement=True,
                    unique=True, nullable=False)
    rasterid = Column(Integer, ForeignKey('raster.rasterid'),
                      primary_key=True, nullable=False)
    volume_number = Column(String, nullable=False)
    volume_properties = Column(Text)
    created = Column(UTCDateTime, default=get_date)
    updated = Column(UTCDateTime, onupdate=get_date)

    def __repr(self):
        return "rastervolume.rvolid='{self.rasterid}'".format(self=self)

    def toJSON(self):
        return {'rvolid': self.rvolid,
                'rasterid': self.rasterid,
                'volume_number': self.volume_number,
                'volume_properties': self.volume_properties,
                'created': self.created,
                'updated': self.updated}

class JournalsRefSource(Base):
    __tablename__ = 'refsource'

    refsourceid = Column(Integer, primary_key=True, autoincrement=True,
                         unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    refsource_list = Column(Text)
    created = Column(UTCDateTime, default=get_date)
    updated = Column(UTCDateTime, onupdate=get_date)

    def __repr__(self):
        return "refsource.refsourceid='{self.refsourceid}'".format(self=self)


class JournalsEditControl(Base):
    __tablename__ = 'editcontrol'

    editid = Column(Integer, primary_key=True, autoincrement=True,
                    unique=True, nullable=False)
    tablename = Column(String, nullable=False)
    editstatus = Column(String, nullable=False)
    editfileid = Column(String, nullable=False)
    created = Column(UTCDateTime, default=get_date)
    updated = Column(UTCDateTime, onupdate=get_date)

    def __repr__(self):
        return "editcontrol.editid='{self.editid}'".format(self=self)
