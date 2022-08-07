
from sqlalchemy import (
    CHAR,
    Column,
    # Date,
    DateTime,
    # Float,
    Index,
    Integer,
    # LargeBinary,
    # SmallInteger,
    String,
    # Table,
    Text,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import declarative_base as _declarative_base

Base: _declarative_base = declarative_base()
metadata = Base.metadata


class TObject(Base):
    __tablename__ = 't_object'
    __table_args__ = (
        Index('ix_object_eaguidclassifier', 'ea_guid', 'classifier'),
        Index('ix_object_pkgidpdata1class', 'package_id', 'pdata1', 'classifier')
    )

    object_id = Column(Integer, primary_key=True, server_default=text("nextval(('object_id_seq'::text)::regclass)"))
    object_type = Column(String(255), index=True)
    diagram_id = Column(Integer, server_default=text("0"))
    name = Column(String(255), index=True)
    alias = Column(String(255))
    author = Column(String(255))
    version = Column(String(50), server_default=text("'1.0'::character varying"))
    note = Column(Text)
    package_id = Column(Integer, index=True, server_default=text("0"))
    stereotype = Column(String(255))
    ntype = Column(Integer, index=True, server_default=text("0"))
    complexity = Column(String(50), server_default=text("'2'::character varying"))
    effort = Column(Integer, server_default=text("0"))
    style = Column(String(255))
    backcolor = Column(Integer, server_default=text("0"))
    borderstyle = Column(Integer, server_default=text("0"))
    borderwidth = Column(Integer, server_default=text("0"))
    fontcolor = Column(Integer, server_default=text("0"))
    bordercolor = Column(Integer, server_default=text("0"))
    createddate = Column(DateTime, server_default=text("now()"))
    modifieddate = Column(DateTime, server_default=text("now()"))
    status = Column(String(50))
    abstract = Column(CHAR(1))
    tagged = Column(Integer, server_default=text("0"))
    pdata1 = Column(String(255), index=True)
    pdata2 = Column(Text, index=True)
    pdata3 = Column(Text, index=True)
    pdata4 = Column(Text, index=True)
    pdata5 = Column(String(255), index=True)
    concurrency = Column(String(50))
    visibility = Column(String(50))
    persistence = Column(String(50))
    cardinality = Column(String(50))
    gentype = Column(String(50))
    genfile = Column(String(255))
    header1 = Column(Text)
    header2 = Column(Text)
    phase = Column(String(50))
    scope = Column(String(25))
    genoption = Column(Text)
    genlinks = Column(Text, index=True)
    classifier = Column(Integer, index=True)
    ea_guid = Column(String(40), unique=True)
    parentid = Column(Integer, index=True)
    runstate = Column(Text)
    classifier_guid = Column(String(40), index=True)
    tpos = Column(Integer)
    isroot = Column(Integer, server_default=text("0"))
    isleaf = Column(Integer, server_default=text("0"))
    isspec = Column(Integer, server_default=text("0"))
    isactive = Column(Integer, server_default=text("0"))
    stateflags = Column(String(255))
    packageflags = Column(String(255))
    multiplicity = Column(String(50))
    styleex = Column(Text)
    actionflags = Column(String(255))
    eventflags = Column(String(255), index=True)


class TPackage(Base):
    __tablename__ = 't_package'

    package_id = Column(Integer, primary_key=True, server_default=text("nextval(('package_id_seq'::text)::regclass)"))
    name = Column(String(255), index=True)
    parent_id = Column(Integer, index=True, server_default=text("0"))
    createddate = Column(DateTime, server_default=text("now()"))
    modifieddate = Column(DateTime, server_default=text("now()"))
    notes = Column(Text)
    ea_guid = Column(String(40), unique=True)
    xmlpath = Column(String(255))
    iscontrolled = Column(Integer, server_default=text("0"))
    lastloaddate = Column(DateTime)
    lastsavedate = Column(DateTime)
    version = Column(String(50))
    protected = Column(Integer, server_default=text("0"))
    pkgowner = Column(String(255))
    umlversion = Column(String(50))
    usedtd = Column(Integer, server_default=text("0"))
    logxml = Column(Integer, server_default=text("0"))
    codepath = Column(String(255))
    namespace = Column(String(50))
    tpos = Column(Integer)
    packageflags = Column(String(255))
    batchsave = Column(Integer)
    batchload = Column(Integer)


class TXref(Base):
    __tablename__ = 't_xref'
    __table_args__ = (
        Index('ix_xref_nametype', 'name', 'type'),
    )

    xrefid = Column(String(255), primary_key=True)
    name = Column(String(255), index=True)
    type = Column(String(255), index=True)
    visibility = Column(String(255))
    namespace = Column(String(255))
    requirement = Column(String(255))
    Constraint = Column(String(255))
    behavior = Column(String(255))
    partition = Column(String(255))
    description = Column(Text)
    client = Column(String(255), index=True)
    supplier = Column(String(255), index=True)
    link = Column(String(255))


class TAttribute(Base):
    __tablename__ = 't_attribute'

    object_id = Column(Integer, index=True, server_default=text("0"))
    name = Column(String(255), index=True)
    scope = Column(String(50))
    stereotype = Column(String(50))
    containment = Column(String(50))
    isstatic = Column(Integer, server_default=text("0"))
    iscollection = Column(Integer, server_default=text("0"))
    isordered = Column(Integer, server_default=text("0"))
    allowduplicates = Column(Integer, server_default=text("0"))
    lowerbound = Column(String(50))
    upperbound = Column(String(50))
    container = Column(String(50))
    notes = Column(Text)
    derived = Column(CHAR(1))
    id = Column(Integer, primary_key=True, server_default=text("nextval(('id_seq'::text)::regclass)"))
    pos = Column(Integer)
    genoption = Column(Text)
    length = Column(Integer)
    precision = Column(Integer)
    scale = Column(Integer)
    const = Column(Integer)
    style = Column(String(255))
    classifier = Column(String(50), index=True)
    Default = Column(Text)
    type = Column(String(255), index=True)
    ea_guid = Column(String(50), unique=True)
    styleex = Column(Text)
