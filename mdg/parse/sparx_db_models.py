from datetime import datetime

from sqlalchemy import (
    CHAR,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    text,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    relationship,
)

class Base(DeclarativeBase):
    pass


class TObject(Base):
    __tablename__ = 't_object'
    __table_args__ = (
        Index('ix_object_eaguidclassifier', 'ea_guid', 'classifier'),
        Index('ix_object_pkgidpdata1class', 'package_id', 'pdata1', 'classifier')
    )

    object_id: Mapped[int] = mapped_column(Integer, primary_key=True, server_default=text("nextval(('object_id_seq'::text)::regclass)"))
    object_type: Mapped[str] = mapped_column(String(255), index=True)
    diagram_id: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    name: Mapped[str] = mapped_column(String(255), index=True)
    alias: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    version: Mapped[str] = mapped_column(String(50), server_default=text("'1.0'::character varying"))
    note: Mapped[str] = mapped_column(Text)
    package_id: Mapped[int] = mapped_column(Integer, index=True, server_default=text("0"))
    stereotype: Mapped[str] = mapped_column(String(255))
    ntype: Mapped[int] = mapped_column(Integer, index=True, server_default=text("0"))
    complexity: Mapped[str] = mapped_column(String(50), server_default=text("'2'::character varying"))
    effort: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    style: Mapped[str] = mapped_column(String(255))
    backcolor: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    borderstyle: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    borderwidth: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    fontcolor: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    bordercolor: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    createddate: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"))
    modifieddate: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"))
    status: Mapped[str] = mapped_column(String(50))
    abstract: Mapped[str] = mapped_column(CHAR(1))
    tagged: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    pdata1: Mapped[str] = mapped_column(String(255), index=True)
    pdata2: Mapped[str] = mapped_column(Text, index=True)
    pdata3: Mapped[str] = mapped_column(Text, index=True)
    pdata4: Mapped[str] = mapped_column(Text, index=True)
    pdata5: Mapped[str] = mapped_column(String(255), index=True)
    concurrency: Mapped[str] = mapped_column(String(50))
    visibility: Mapped[str] = mapped_column(String(50))
    persistence: Mapped[str] = mapped_column(String(50))
    cardinality: Mapped[str] = mapped_column(String(50))
    gentype: Mapped[str] = mapped_column(String(50))
    genfile: Mapped[str] = mapped_column(String(255))
    header1: Mapped[str] = mapped_column(Text)
    header2: Mapped[str] = mapped_column(Text)
    phase: Mapped[str] = mapped_column(String(50))
    scope: Mapped[str] = mapped_column(String(25))
    genoption: Mapped[str] = mapped_column(Text)
    genlinks: Mapped[str] = mapped_column(Text, index=True)
    classifier: Mapped[int] = mapped_column(Integer, index=True)
    ea_guid: Mapped[str] = mapped_column(String(40), unique=True)
    parentid: Mapped[int] = mapped_column(Integer, index=True)
    runstate: Mapped[str] = mapped_column(Text)
    classifier_guid: Mapped[str] = mapped_column(String(40), index=True)
    tpos: Mapped[int] = mapped_column(Integer)
    isroot: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    isleaf: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    isspec: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    isactive: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    stateflags: Mapped[str] = mapped_column(String(255))
    packageflags: Mapped[str] = mapped_column(String(255))
    multiplicity: Mapped[str] = mapped_column(String(50))
    styleex: Mapped[str] = mapped_column(Text)
    actionflags: Mapped[str] = mapped_column(String(255))
    eventflags: Mapped[str] = mapped_column(String(255), index=True)


class TPackage(Base):
    __tablename__ = 't_package'

    package_id: Mapped[int] = mapped_column(Integer, primary_key=True, server_default=text("nextval(('package_id_seq'::text)::regclass)"))
    name: Mapped[str] = mapped_column(String(255), index=True)
    parent_id: Mapped[int] = mapped_column(Integer, index=True, server_default=text("0"))
    createddate: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"))
    modifieddate: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"))
    notes: Mapped[str] = mapped_column(Text)
    ea_guid: Mapped[str] = mapped_column(String(40), unique=True)
    xmlpath: Mapped[str] = mapped_column(String(255))
    iscontrolled: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    lastloaddate: Mapped[datetime] = mapped_column(DateTime)
    lastsavedate: Mapped[datetime] = mapped_column(DateTime)
    version: Mapped[str] = mapped_column(String(50))
    protected: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    pkgowner: Mapped[str] = mapped_column(String(255))
    umlversion: Mapped[str] = mapped_column(String(50))
    usedtd: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    logxml: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    codepath: Mapped[str] = mapped_column(String(255))
    namespace: Mapped[str] = mapped_column(String(50))
    tpos: Mapped[int] = mapped_column(Integer)
    packageflags: Mapped[str] = mapped_column(String(255))
    batchsave: Mapped[int] = mapped_column(Integer)
    batchload: Mapped[int] = mapped_column(Integer)


class TXref(Base):
    __tablename__ = 't_xref'
    __table_args__ = (
        Index('ix_xref_nametype', 'name', 'type'),
    )

    xrefid: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    type: Mapped[str] = mapped_column(String(255), index=True)
    visibility: Mapped[str] = mapped_column(String(255))
    namespace: Mapped[str] = mapped_column(String(255))
    requirement: Mapped[str] = mapped_column(String(255))
    Constraint: Mapped[str] = mapped_column(String(255))
    behavior: Mapped[str] = mapped_column(String(255))
    partition: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    client: Mapped[str] = mapped_column(String(255), index=True)
    supplier: Mapped[str] = mapped_column(String(255), index=True)
    link: Mapped[str] = mapped_column(String(255))


class TAttribute(Base):
    __tablename__ = 't_attribute'

    object_id: Mapped[int] = mapped_column(Integer, index=True, server_default=text("0"))
    name: Mapped[str] = mapped_column(String(255), index=True)
    scope: Mapped[str] = mapped_column(String(50))
    stereotype: Mapped[str] = mapped_column(String(50))
    containment: Mapped[str] = mapped_column(String(50))
    isstatic: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    iscollection: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    isordered: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    allowduplicates: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    lowerbound: Mapped[str] = mapped_column(String(50))
    upperbound: Mapped[str] = mapped_column(String(50))
    container: Mapped[str] = mapped_column(String(50))
    notes: Mapped[str] = mapped_column(Text)
    derived: Mapped[str] = mapped_column(CHAR(1))
    id: Mapped[int] = mapped_column(Integer, primary_key=True, server_default=text("nextval(('id_seq'::text)::regclass)"))
    pos: Mapped[int] = mapped_column(Integer)
    genoption: Mapped[str] = mapped_column(Text)
    length: Mapped[int] = mapped_column(Integer)
    precision: Mapped[int] = mapped_column(Integer)
    scale: Mapped[int] = mapped_column(Integer)
    const: Mapped[int] = mapped_column(Integer)
    style: Mapped[str] = mapped_column(String(255))
    classifier: Mapped[str] = mapped_column(String(50), index=True)
    Default: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(255), index=True)
    ea_guid: Mapped[str] = mapped_column(String(50), unique=True)
    styleex: Mapped[str] = mapped_column(Text)


class TConnector(Base):
    __tablename__ = 't_connector'
    __table_args__ = (
        Index('ix_connector_startobjidconnid', 'start_object_id', 'connector_id'),
        Index('ix_connector_endobjidconnid', 'end_object_id', 'connector_id')
    )

    connector_id: Mapped[int] = mapped_column(Integer, primary_key=True, server_default=text("nextval(('connector_id_seq'::text)::regclass)"))
    name: Mapped[str] = mapped_column(String(255))
    direction: Mapped[str] = mapped_column(String(50))
    notes: Mapped[str] = mapped_column(Text)
    connector_type: Mapped[str] = mapped_column(String(50), index=True)
    subtype: Mapped[str] = mapped_column(String(50), index=True)
    sourcecard: Mapped[str] = mapped_column(String(50))
    sourceaccess: Mapped[str] = mapped_column(String(50))
    sourceelement: Mapped[str] = mapped_column(String(50))
    destcard: Mapped[str] = mapped_column(String(50))
    destaccess: Mapped[str] = mapped_column(String(50))
    destelement: Mapped[str] = mapped_column(String(50))
    sourcerole: Mapped[str] = mapped_column(String(255))
    sourceroletype: Mapped[str] = mapped_column(String(50))
    sourcerolenote: Mapped[str] = mapped_column(Text)
    sourcecontainment: Mapped[str] = mapped_column(String(50))
    sourceisaggregate: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    sourceisordered: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    sourcequalifier: Mapped[str] = mapped_column(String(50))
    destrole: Mapped[str] = mapped_column(String(255))
    destroletype: Mapped[str] = mapped_column(String(50))
    destrolenote: Mapped[str] = mapped_column(Text)
    destcontainment: Mapped[str] = mapped_column(String(50))
    destisaggregate: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    destisordered: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    destqualifier: Mapped[str] = mapped_column(String(50))
    start_object_id: Mapped[int] = mapped_column(Integer, index=True, server_default=text("0"))
    end_object_id: Mapped[int] = mapped_column(Integer, index=True, server_default=text("0"))
    top_start_label: Mapped[str] = mapped_column(String(50))
    top_mid_label: Mapped[str] = mapped_column(String(50))
    top_end_label: Mapped[str] = mapped_column(String(50))
    btm_start_label: Mapped[str] = mapped_column(String(50))
    btm_mid_label: Mapped[str] = mapped_column(String(50))
    btm_end_label: Mapped[str] = mapped_column(String(50))
    start_edge: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    end_edge: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    ptstartx: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    ptstarty: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    ptendx: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    ptendy: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    seqno: Mapped[int] = mapped_column(Integer, index=True, server_default=text("0"))
    headstyle: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    linestyle: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    routestyle: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    isbold: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    linecolor: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    stereotype: Mapped[str] = mapped_column(String(50))
    virtualinheritance: Mapped[str] = mapped_column(CHAR(1))
    linkaccess: Mapped[str] = mapped_column(String(50))
    pdata1: Mapped[str] = mapped_column(String(255), index=True)
    pdata2: Mapped[str] = mapped_column(Text)
    pdata3: Mapped[str] = mapped_column(String(255), index=True)
    pdata4: Mapped[str] = mapped_column(String(255))
    pdata5: Mapped[str] = mapped_column(Text, index=True)
    diagramid: Mapped[int] = mapped_column(Integer, index=True, server_default=text("0"))
    ea_guid: Mapped[str] = mapped_column(String(40), unique=True)
    sourceconstraint: Mapped[str] = mapped_column(String(255))
    destconstraint: Mapped[str] = mapped_column(String(255))
    sourceisnavigable: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    destisnavigable: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    isroot: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    isleaf: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    isspec: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    sourcechangeable: Mapped[str] = mapped_column(String(12))
    destchangeable: Mapped[str] = mapped_column(String(12))
    sourcets: Mapped[str] = mapped_column(String(12))
    destts: Mapped[str] = mapped_column(String(12))
    stateflags: Mapped[str] = mapped_column(Text)
    actionflags: Mapped[str] = mapped_column(String(255))
    issignal: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    isstimulus: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    dispatchaction: Mapped[str] = mapped_column(String(255))
    target2: Mapped[str] = mapped_column(Integer)
    styleex: Mapped[str] = mapped_column(Text, index=True)
    sourcestereotype: Mapped[str] = mapped_column(String(255))
    deststereotype: Mapped[str] = mapped_column(String(255))
    sourcestyle: Mapped[str] = mapped_column(Text)
    deststyle: Mapped[str] = mapped_column(Text)
    eventflags: Mapped[str] = mapped_column(String(255))


class TAttributeconstraint(Base):
    __tablename__ = 't_attributeconstraints'

    object_id: Mapped[int] = mapped_column(Integer, index=True, server_default=text("0"))
    Constraint: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False)
    attname: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    notes: Mapped[str] = mapped_column(Text)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)


class TAttributetag(Base):
    __tablename__ = 't_attributetag'
    __table_args__ = (
        Index('ix_attributetag_elementidprop', 'elementid', 'property'),
    )

    propertyid: Mapped[int] = mapped_column(Integer, primary_key=True, server_default=text("nextval(('propertyid_seq'::text)::regclass)"))
    elementid: Mapped[int] = mapped_column(Integer, index=True)
    property: Mapped[str] = mapped_column(String(255), index=True)
    value: Mapped[str] = mapped_column(String(255), index=True)
    notes: Mapped[str] = mapped_column(Text)
    ea_guid: Mapped[str] = mapped_column(String(40), index=True)
