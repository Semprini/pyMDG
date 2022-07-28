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


# class TAttribute(Base):
#     __tablename__ = 't_attribute'

#     object_id = Column(Integer, index=True, server_default=text("0"))
#     name = Column(String(255), index=True)
#     scope = Column(String(50))
#     stereotype = Column(String(50))
#     containment = Column(String(50))
#     isstatic = Column(Integer,server_default=text("0"))
#     iscollection = Column(Integer, server_default=text("0"))
#     isordered = Column(Integer, server_default=text("0"))
#     allowduplicates = Column(Integer, server_default=text("0"))
#     lowerbound = Column(String(50))
#     upperbound = Column(String(50))
#     container = Column(String(50))
#     notes = Column(Text)
#     derived = Column(CHAR(1))
#     id = Column(Integer, primary_key=True, server_default=text("nextval(('id_seq'::text)::regclass)"))
#     pos = Column(Integer)
#     genoption = Column(Text)
#     length = Column(Integer)
#     precision = Column(Integer)
#     scale = Column(Integer)
#     const = Column(Integer)
#     style = Column(String(255))
#     classifier = Column(String(50), index=True)
#     Default = Column(Text)
#     type = Column(String(255), index=True)
#     ea_guid = Column(String(50), unique=True)
#     styleex = Column(Text)


# class TAttributeconstraint(Base):
#     __tablename__ = 't_attributeconstraints'

#     object_id = Column(Integer, index=True, server_default=text("0"))
#     Constraint = Column(String(255), primary_key=True, nullable=False)
#     attname = Column(String(255))
#     type = Column(String(255))
#     notes = Column(Text)
#     id = Column(Integer, primary_key=True, nullable=False)


# class TAttributetag(Base):
#     __tablename__ = 't_attributetag'
#     __table_args__ = (
#         Index('ix_attributetag_elementidprop', 'elementid', 'property'),
#     )

#     propertyid = Column(Integer, primary_key=True, server_default=text("nextval(('propertyid_seq'::text)::regclass)"))
#     elementid = Column(Integer, index=True)
#     property = Column(String(255), index=True)
#     value = Column(String(255), index=True)
#     notes = Column(Text)
#     ea_guid = Column(String(40), index=True)


# class TAuthor(Base):
#     __tablename__ = 't_authors'

#     authorname = Column(String(255), primary_key=True)
#     roles = Column(String(255))
#     notes = Column(String(255))


# class TCardinality(Base):
#     __tablename__ = 't_cardinality'

#     cardinality = Column(String(50), primary_key=True)


# class TCategory(Base):
#     __tablename__ = 't_category'

#     categoryid = Column(Integer, primary_key=True, server_default=text("nextval(('categoryid_seq'::text)::regclass)"))
#     name = Column(String(255))
#     type = Column(String(255))
#     notes = Column(Text)


# class TClient(Base):
#     __tablename__ = 't_clients'

#     name = Column(String(255), primary_key=True)
#     organisation = Column(String(255))
#     phone1 = Column(String(50))
#     phone2 = Column(String(50))
#     mobile = Column(String(50))
#     fax = Column(String(50))
#     email = Column(String(50))
#     roles = Column(String(255))
#     notes = Column(String(255))


# class TComplexitytype(Base):
#     __tablename__ = 't_complexitytypes'

#     complexity = Column(String(50), primary_key=True)
#     numericweight = Column(Integer, index=True, server_default=text("0"))


# class TConnector(Base):
#     __tablename__ = 't_connector'
#     __table_args__ = (
#         Index('ix_connector_startobjidconnid', 'start_object_id', 'connector_id'),
#         Index('ix_connector_endobjidconnid', 'end_object_id', 'connector_id')
#     )

#     connector_id = Column(Integer, primary_key=True, server_default=text("nextval(('connector_id_seq'::text)::regclass)"))
#     name = Column(String(255))
#     direction = Column(String(50))
#     notes = Column(Text)
#     connector_type = Column(String(50), index=True)
#     subtype = Column(String(50), index=True)
#     sourcecard = Column(String(50))
#     sourceaccess = Column(String(50))
#     sourceelement = Column(String(50))
#     destcard = Column(String(50))
#     destaccess = Column(String(50))
#     destelement = Column(String(50))
#     sourcerole = Column(String(255))
#     sourceroletype = Column(String(50))
#     sourcerolenote = Column(Text)
#     sourcecontainment = Column(String(50))
#     sourceisaggregate = Column(Integer, server_default=text("0"))
#     sourceisordered = Column(Integer, server_default=text("0"))
#     sourcequalifier = Column(String(50))
#     destrole = Column(String(255))
#     destroletype = Column(String(50))
#     destrolenote = Column(Text)
#     destcontainment = Column(String(50))
#     destisaggregate = Column(Integer, server_default=text("0"))
#     destisordered = Column(Integer, server_default=text("0"))
#     destqualifier = Column(String(50))
#     start_object_id = Column(Integer, index=True, server_default=text("0"))
#     end_object_id = Column(Integer, index=True, server_default=text("0"))
#     top_start_label = Column(String(50))
#     top_mid_label = Column(String(50))
#     top_end_label = Column(String(50))
#     btm_start_label = Column(String(50))
#     btm_mid_label = Column(String(50))
#     btm_end_label = Column(String(50))
#     start_edge = Column(Integer, server_default=text("0"))
#     end_edge = Column(Integer, server_default=text("0"))
#     ptstartx = Column(Integer, server_default=text("0"))
#     ptstarty = Column(Integer, server_default=text("0"))
#     ptendx = Column(Integer, server_default=text("0"))
#     ptendy = Column(Integer, server_default=text("0"))
#     seqno = Column(Integer, index=True, server_default=text("0"))
#     headstyle = Column(Integer, server_default=text("0"))
#     linestyle = Column(Integer, server_default=text("0"))
#     routestyle = Column(Integer, server_default=text("0"))
#     isbold = Column(Integer, server_default=text("0"))
#     linecolor = Column(Integer, server_default=text("0"))
#     stereotype = Column(String(50))
#     virtualinheritance = Column(CHAR(1))
#     linkaccess = Column(String(50))
#     pdata1 = Column(String(255), index=True)
#     pdata2 = Column(Text)
#     pdata3 = Column(String(255), index=True)
#     pdata4 = Column(String(255))
#     pdata5 = Column(Text, index=True)
#     diagramid = Column(Integer, index=True, server_default=text("0"))
#     ea_guid = Column(String(40), unique=True)
#     sourceconstraint = Column(String(255))
#     destconstraint = Column(String(255))
#     sourceisnavigable = Column(Integer, server_default=text("0"))
#     destisnavigable = Column(Integer, server_default=text("0"))
#     isroot = Column(Integer, server_default=text("0"))
#     isleaf = Column(Integer, server_default=text("0"))
#     isspec = Column(Integer, server_default=text("0"))
#     sourcechangeable = Column(String(12))
#     destchangeable = Column(String(12))
#     sourcets = Column(String(12))
#     destts = Column(String(12))
#     stateflags = Column(Text)
#     actionflags = Column(String(255))
#     issignal = Column(Integer, server_default=text("0"))
#     isstimulus = Column(Integer, server_default=text("0"))
#     dispatchaction = Column(String(255))
#     target2 = Column(Integer)
#     styleex = Column(Text, index=True)
#     sourcestereotype = Column(String(255))
#     deststereotype = Column(String(255))
#     sourcestyle = Column(Text)
#     deststyle = Column(Text)
#     eventflags = Column(String(255))


# class TConnectorconstraint(Base):
#     __tablename__ = 't_connectorconstraint'

#     connectorid = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     Constraint = Column(String(255), primary_key=True, nullable=False, index=True)
#     constrainttype = Column(String(50))
#     notes = Column(Text)


# class TConnectortag(Base):
#     __tablename__ = 't_connectortag'

#     propertyid = Column(Integer, primary_key=True, server_default=text("nextval(('propertyid_seq'::text)::regclass)"))
#     elementid = Column(Integer, index=True)
#     property = Column(String(255), index=True)
#     value = Column(String(255), index=True)
#     notes = Column(Text)
#     ea_guid = Column(String(40), index=True)


# class TConnectortype(Base):
#     __tablename__ = 't_connectortypes'

#     connector_type = Column(String(50), primary_key=True)
#     description = Column(String(50))


# class TConstant(Base):
#     __tablename__ = 't_constants'

#     constantname = Column(String(50), primary_key=True)
#     constantvalue = Column(String(255))


# class TConstrainttype(Base):
#     __tablename__ = 't_constrainttypes'

#     Constraint = Column(String(16), primary_key=True)
#     description = Column(String(50))
#     notes = Column(Text)


# class TDatatype(Base):
#     __tablename__ = 't_datatypes'

#     type = Column(String(50))
#     productname = Column(String(50), index=True)
#     datatype = Column(String(50), index=True)
#     size = Column(Integer)
#     maxlen = Column(Integer)
#     maxprec = Column(Integer)
#     maxscale = Column(Integer, server_default=text("0"))
#     defaultlen = Column(Integer)
#     defaultprec = Column(Integer)
#     defaultscale = Column(Integer)
#     User = Column(Integer)
#     pdata1 = Column(String(255))
#     pdata2 = Column(String(255))
#     pdata3 = Column(String(255))
#     pdata4 = Column(String(255))
#     haslength = Column(String(50))
#     generictype = Column(String(255))
#     datatypeid = Column(Integer, primary_key=True, server_default=text("nextval(('datatypeid_seq'::text)::regclass)"))


# class TDiagram(Base):
#     __tablename__ = 't_diagram'

#     diagram_id = Column(Integer, primary_key=True, server_default=text("nextval(('diagram_id_seq'::text)::regclass)"))
#     package_id = Column(Integer, index=True, server_default=text("1"))
#     parentid = Column(Integer, index=True, server_default=text("0"))
#     diagram_type = Column(String(50), index=True)
#     name = Column(String(255))
#     version = Column(String(50), server_default=text("'1.0'::character varying"))
#     author = Column(String(255))
#     showdetails = Column(Integer, server_default=text("0"))
#     notes = Column(Text)
#     stereotype = Column(String(50))
#     attpub = Column(Integer, nullable=False, server_default=text("1"))
#     attpri = Column(Integer, nullable=False, server_default=text("1"))
#     attpro = Column(Integer, nullable=False, server_default=text("1"))
#     orientation = Column(CHAR(1), server_default=text("'P'::bpchar"))
#     cx = Column(Integer, server_default=text("0"))
#     cy = Column(Integer, server_default=text("0"))
#     scale = Column(Integer, server_default=text("100"))
#     createddate = Column(DateTime, server_default=text("now()"))
#     modifieddate = Column(DateTime, server_default=text("now()"))
#     htmlpath = Column(String(255))
#     showforeign = Column(Integer, nullable=False, server_default=text("1"))
#     showborder = Column(Integer, nullable=False, server_default=text("1"))
#     showpackagecontents = Column(Integer, nullable=False, server_default=text("1"))
#     pdata = Column(String(255))
#     locked = Column(Integer, nullable=False, server_default=text("0"))
#     ea_guid = Column(String(40), unique=True)
#     tpos = Column(Integer)
#     swimlanes = Column(String(255))
#     styleex = Column(Text)


# class TDiagramlink(Base):
#     __tablename__ = 't_diagramlinks'

#     diagramid = Column(Integer, index=True)
#     connectorid = Column(Integer, index=True)
#     geometry = Column(Text)
#     style = Column(String(255))
#     hidden = Column(Integer, nullable=False, server_default=text("0"))
#     path = Column(String(255))
#     instance_id = Column(Integer, primary_key=True, server_default=text("nextval(('instance_id_seq'::text)::regclass)"))


# class TDiagramobject(Base):
#     __tablename__ = 't_diagramobjects'

#     diagram_id = Column(Integer, index=True, server_default=text("0"))
#     object_id = Column(Integer, index=True, server_default=text("0"))
#     recttop = Column(Integer, server_default=text("0"))
#     rectleft = Column(Integer, server_default=text("0"))
#     rectright = Column(Integer, server_default=text("0"))
#     rectbottom = Column(Integer, server_default=text("0"))
#     sequence = Column(Integer, index=True, server_default=text("0"))
#     objectstyle = Column(String(255))
#     instance_id = Column(Integer, primary_key=True, server_default=text("nextval(('instance_id_seq'::text)::regclass)"))


# class TDiagramtype(Base):
#     __tablename__ = 't_diagramtypes'

#     diagram_type = Column(String(50), primary_key=True)
#     name = Column(String(255))
#     package_id = Column(Integer, index=True, server_default=text("0"))


# class TDocument(Base):
#     __tablename__ = 't_document'

#     docid = Column(String(40), primary_key=True)
#     docname = Column(String(100))
#     notes = Column(String(255))
#     style = Column(String(255), index=True)
#     elementid = Column(String(40), nullable=False, index=True)
#     elementtype = Column(String(50), nullable=False)
#     strcontent = Column(Text)
#     bincontent = Column(LargeBinary)
#     doctype = Column(String(100), index=True)
#     author = Column(String(255), index=True)
#     version = Column(String(50), index=True)
#     isactive = Column(Integer, server_default=text("1"))
#     sequence = Column(Integer, server_default=text("0"))
#     docdate = Column(DateTime)


# class TEcf(Base):
#     __tablename__ = 't_ecf'

#     ecfid = Column(String(12), primary_key=True)
#     description = Column(String(50))
#     weight = Column(Float, index=True, server_default=text("1"))
#     value = Column(Float, server_default=text("0"))
#     notes = Column(String(255))


# class TEfforttype(Base):
#     __tablename__ = 't_efforttypes'

#     efforttype = Column(String(12), primary_key=True)
#     description = Column(String(255))
#     numericweight = Column(Float, index=True, server_default=text("0"))
#     notes = Column(String(255))


# class TFile(Base):
#     __tablename__ = 't_files'
#     __table_args__ = (
#         Index('ix_files_appliestoname', 'appliesto', 'name'),
#         Index('ix_files_appliestonamedatesize', 'appliesto', 'name', 'filedate', 'filesize'),
#         Index('ix_files_appliestonamesize', 'appliesto', 'name', 'filesize')
#     )

#     fileid = Column(String(50), primary_key=True)
#     appliesto = Column(String(50), nullable=False, index=True)
#     category = Column(String(100), nullable=False, index=True)
#     name = Column(String(150), nullable=False, index=True)
#     file = Column(String(255))
#     notes = Column(Text)
#     filedate = Column(DateTime)
#     filesize = Column(Integer, index=True)


# t_t_genopt = Table(
#     't_genopt', metadata,
#     Column('appliesto', String(12)),
#     Column('option', Text)
# )


# class TGlossary(Base):
#     __tablename__ = 't_glossary'

#     term = Column(String(255), index=True)
#     type = Column(String(255), index=True)
#     meaning = Column(Text)
#     glossaryid = Column(Integer, primary_key=True, server_default=text("nextval(('glossaryid_seq'::text)::regclass)"))


# t_t_html = Table(
#     't_html', metadata,
#     Column('type', String(50)),
#     Column('template', Text)
# )


# class TImage(Base):
#     __tablename__ = 't_image'

#     imageid = Column(Integer, primary_key=True, server_default=text("nextval(('imageid_seq'::text)::regclass)"))
#     name = Column(String(255))
#     type = Column(String(255))
#     image = Column(LargeBinary)


# t_t_implement = Table(
#     't_implement', metadata,
#     Column('type', String(50))
# )


# class TIssue(Base):
#     __tablename__ = 't_issues'

#     issue = Column(String(255))
#     issuedate = Column(DateTime)
#     owner = Column(String(255))
#     status = Column(String(50))
#     notes = Column(Text)
#     resolver = Column(String(255))
#     dateresolved = Column(DateTime)
#     resolution = Column(Text)
#     issueid = Column(Integer, primary_key=True, server_default=text("nextval(('issueid_seq'::text)::regclass)"))
#     category = Column(String(255))
#     priority = Column(String(50))
#     severity = Column(String(50))
#     issuetype = Column(String(100))


# class TList(Base):
#     __tablename__ = 't_lists'

#     listid = Column(String(50), primary_key=True)
#     category = Column(String(100), nullable=False)
#     name = Column(String(150), nullable=False)
#     nval = Column(Integer)
#     notes = Column(Text)


# class TMainttype(Base):
#     __tablename__ = 't_mainttypes'

#     mainttype = Column(String(12), primary_key=True)
#     description = Column(String(50))
#     numericweight = Column(Float, index=True, server_default=text("1"))
#     notes = Column(String(255))


# class TMethod(Base):
#     __tablename__ = 't_method'

#     object_id = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     name = Column(String(255), primary_key=True, nullable=False)
#     scope = Column(String(50))
#     type = Column(String(50))


# class TMetrictype(Base):
#     __tablename__ = 't_metrictypes'

#     metric = Column(String(12), primary_key=True)
#     description = Column(String(50))
#     numericweight = Column(Float, index=True, server_default=text("1"))
#     notes = Column(String(255))


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


# class TObjectconstraint(Base):
#     __tablename__ = 't_objectconstraint'

#     object_id = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     Constraint = Column(String(255), primary_key=True, nullable=False, index=True)
#     constrainttype = Column(String(30), primary_key=True, nullable=False)
#     weight = Column(Float, server_default=text("0"))
#     notes = Column(Text)
#     status = Column(String(50))


# class TObjecteffort(Base):
#     __tablename__ = 't_objecteffort'

#     object_id = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     effort = Column(String(255), primary_key=True, nullable=False)
#     efforttype = Column(String(12))
#     evalue = Column(Float, server_default=text("0"))
#     notes = Column(Text)


# class TObjectfile(Base):
#     __tablename__ = 't_objectfiles'

#     object_id = Column(Integer, primary_key=True, nullable=False, server_default=text("0"))
#     filename = Column(String(255), primary_key=True, nullable=False)
#     type = Column(String(50))
#     note = Column(Text)
#     filesize = Column(String(255))
#     filedate = Column(String(255))


# class TObjectmetric(Base):
#     __tablename__ = 't_objectmetrics'

#     object_id = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     metric = Column(String(255), primary_key=True, nullable=False, index=True)
#     metrictype = Column(String(12), index=True)
#     evalue = Column(Float, server_default=text("1"))
#     notes = Column(Text)


# class TObjectproblem(Base):
#     __tablename__ = 't_objectproblems'

#     object_id = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     problem = Column(String(255), primary_key=True, nullable=False, index=True)
#     problemtype = Column(String(255), primary_key=True, nullable=False)
#     datereported = Column(Date)
#     status = Column(String(50))
#     problemnotes = Column(Text)
#     reportedby = Column(String(255))
#     resolvedby = Column(String(255))
#     dateresolved = Column(Date)
#     version = Column(String(50))
#     resolvernotes = Column(Text)
#     priority = Column(String(50))
#     severity = Column(String(50))


# class TObjectproperty(Base):
#     __tablename__ = 't_objectproperties'
#     __table_args__ = (
#         Index('ix_objectproperties_objidprop', 'object_id', 'property'),
#     )

#     propertyid = Column(Integer, primary_key=True, server_default=text("nextval(('propertyid_seq'::text)::regclass)"))
#     object_id = Column(Integer, index=True, server_default=text("0"))
#     property = Column(String(255), index=True)
#     value = Column(String(255), index=True)
#     notes = Column(Text)
#     ea_guid = Column(String(40), index=True)


# class TObjectrequire(Base):
#     __tablename__ = 't_objectrequires'

#     reqid = Column(Integer, primary_key=True, server_default=text("nextval(('reqid_seq'::text)::regclass)"))
#     object_id = Column(Integer, index=True, server_default=text("0"))
#     requirement = Column(String(255), index=True)
#     reqtype = Column(String(255))
#     status = Column(String(50))
#     notes = Column(Text)
#     stability = Column(String(50))
#     difficulty = Column(String(50))
#     priority = Column(String(50))
#     lastupdate = Column(DateTime, server_default=text("now()"))


# class TObjectresource(Base):
#     __tablename__ = 't_objectresource'

#     object_id = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     resource = Column(String(255), primary_key=True, nullable=False)
#     role = Column(String(255), primary_key=True, nullable=False)
#     time = Column(Float, server_default=text("0"))
#     notes = Column(Text)
#     percentcomplete = Column(SmallInteger, server_default=text("0"))
#     datestart = Column(Date)
#     dateend = Column(Date)
#     history = Column(Text)
#     expectedhours = Column(Integer)
#     actualhours = Column(Integer)


# class TObjectrisk(Base):
#     __tablename__ = 't_objectrisks'

#     object_id = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     risk = Column(String(255), primary_key=True, nullable=False)
#     risktype = Column(String(12))
#     evalue = Column(Float, server_default=text("0"))
#     notes = Column(Text)


# class TObjectscenario(Base):
#     __tablename__ = 't_objectscenarios'
#     __table_args__ = (
#         Index('ix_objectscenarios_oidevalscen', 'object_id', 'evalue', 'scenario'),
#     )

#     object_id = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     scenario = Column(String(255), primary_key=True, nullable=False)
#     scenariotype = Column(String(12))
#     evalue = Column(Float, server_default=text("0"))
#     notes = Column(Text)
#     ea_guid = Column(String(40), nullable=False)
#     xmlcontent = Column(Text)


# class TObjecttest(Base):
#     __tablename__ = 't_objecttests'
#     __table_args__ = (
#         Index('ix_objecttexts_objidtclassstat', 'object_id', 'testclass', 'status'),
#     )

#     object_id = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     test = Column(String(255), primary_key=True, nullable=False)
#     testclass = Column(Integer, primary_key=True, nullable=False, server_default=text("0"))
#     testtype = Column(String(50))
#     notes = Column(Text)
#     inputdata = Column(Text)
#     acceptancecriteria = Column(Text)
#     status = Column(String(32))
#     daterun = Column(Date, server_default=text("now()"))
#     results = Column(Text)
#     runby = Column(String(255))
#     checkby = Column(String(255))


# class TObjecttrx(Base):
#     __tablename__ = 't_objecttrx'

#     object_id = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     trx = Column(String(255), primary_key=True, nullable=False, index=True)
#     trxtype = Column(String(12), primary_key=True, nullable=False)
#     weight = Column(Float, server_default=text("0"))
#     notes = Column(Text)


# class TObjecttype(Base):
#     __tablename__ = 't_objecttypes'

#     object_type = Column(String(50), primary_key=True)
#     description = Column(String(255))
#     designobject = Column(Integer, nullable=False, server_default=text("0"))
#     imageid = Column(SmallInteger, index=True, server_default=text("0"))


# t_t_ocf = Table(
#     't_ocf', metadata,
#     Column('objecttype', String(50)),
#     Column('complexityweight', Float, server_default=text("0"))
# )


# class TOperation(Base):
#     __tablename__ = 't_operation'
#     __table_args__ = (
#         Index('ix_operation_objectidopid', 'object_id', 'operationid'),
#     )

#     operationid = Column(Integer, primary_key=True, server_default=text("nextval(('operationid_seq'::text)::regclass)"))
#     object_id = Column(Integer, index=True, server_default=text("0"))
#     name = Column(String(255), index=True)
#     scope = Column(String(50))
#     type = Column(String(255))
#     returnarray = Column(CHAR(1))
#     stereotype = Column(String(50))
#     isstatic = Column(CHAR(1))
#     concurrency = Column(String(50))
#     notes = Column(Text)
#     behaviour = Column(Text)
#     abstract = Column(CHAR(1))
#     genoption = Column(Text)
#     synchronized = Column(CHAR(1))
#     pos = Column(Integer)
#     const = Column(Integer)
#     style = Column(String(255))
#     pure = Column(Integer, nullable=False, server_default=text("0"))
#     throws = Column(String(255))
#     classifier = Column(String(50), index=True)
#     code = Column(Text)
#     isroot = Column(Integer, server_default=text("0"))
#     isleaf = Column(Integer, server_default=text("0"))
#     isquery = Column(Integer, server_default=text("0"))
#     stateflags = Column(String(255))
#     ea_guid = Column(String(50), unique=True)
#     styleex = Column(Text)


# class TOperationparam(Base):
#     __tablename__ = 't_operationparams'
#     __table_args__ = (
#         Index('ix_operationparams_opidpos', 'operationid', 'pos'),
#     )

#     operationid = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     name = Column(String(255), primary_key=True, nullable=False)
#     type = Column(String(255))
#     Default = Column(String(255))
#     notes = Column(Text)
#     pos = Column(Integer)
#     const = Column(Integer, server_default=text("0"))
#     style = Column(String(255))
#     kind = Column(String(12))
#     classifier = Column(String(50), index=True)
#     ea_guid = Column(String(50), unique=True)
#     styleex = Column(Text)


# class TOperationpost(Base):
#     __tablename__ = 't_operationposts'

#     operationid = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     postcondition = Column(String(255), primary_key=True, nullable=False)
#     type = Column(String(255))
#     notes = Column(Text)


# class TOperationpre(Base):
#     __tablename__ = 't_operationpres'

#     operationid = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     precondition = Column(String(255), primary_key=True, nullable=False)
#     type = Column(String(50))
#     notes = Column(Text)


# class TOperationtag(Base):
#     __tablename__ = 't_operationtag'
#     __table_args__ = (
#         Index('ix_operationtag_elementidprop', 'elementid', 'property'),
#     )

#     propertyid = Column(Integer, primary_key=True, server_default=text("nextval(('propertyid_seq'::text)::regclass)"))
#     elementid = Column(Integer, index=True)
#     property = Column(String(255), index=True)
#     value = Column(String(255), index=True)
#     notes = Column(Text)
#     ea_guid = Column(String(40), index=True)


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


# class TPalette(Base):
#     __tablename__ = 't_palette'

#     paletteid = Column(Integer, primary_key=True, server_default=text("nextval(('paletteid_seq'::text)::regclass)"))
#     name = Column(String(255))
#     type = Column(String(255))


# t_t_paletteitem = Table(
#     't_paletteitem', metadata,
#     Column('paletteid', Integer),
#     Column('itemid', Integer)
# )


# class TPhase(Base):
#     __tablename__ = 't_phase'

#     phaseid = Column(String(40), primary_key=True)
#     phasename = Column(String(100), nullable=False)
#     phasenotes = Column(Text)
#     phasestyle = Column(String(255))
#     startdate = Column(DateTime)
#     enddate = Column(DateTime)
#     phasecontent = Column(Text)


# class TPrimitive(Base):
#     __tablename__ = 't_primitives'

#     datatype = Column(String(50), primary_key=True)
#     description = Column(String(50))


# class TProblemtype(Base):
#     __tablename__ = 't_problemtypes'

#     problemtype = Column(String(12), primary_key=True)
#     description = Column(String(255))
#     numericweight = Column(Float, index=True, server_default=text("1"))
#     notes = Column(String(255))


# class TProjectrole(Base):
#     __tablename__ = 't_projectroles'

#     role = Column(String(255), primary_key=True)
#     description = Column(String(255))
#     notes = Column(Text)


# class TPropertytype(Base):
#     __tablename__ = 't_propertytypes'

#     property = Column(String(50), primary_key=True)
#     description = Column(String(50))
#     notes = Column(Text)


# class TRequiretype(Base):
#     __tablename__ = 't_requiretypes'

#     requirement = Column(String(12), primary_key=True)
#     description = Column(String(50))
#     numericweight = Column(Float, index=True, server_default=text("1"))
#     notes = Column(String(255))


# class TResource(Base):
#     __tablename__ = 't_resources'

#     name = Column(String(255), primary_key=True)
#     organisation = Column(String(255))
#     phone1 = Column(String(50))
#     phone2 = Column(String(50))
#     mobile = Column(String(50))
#     fax = Column(String(50))
#     email = Column(String(255))
#     roles = Column(String(255))
#     notes = Column(String(255))


# class TRisktype(Base):
#     __tablename__ = 't_risktypes'

#     risk = Column(String(12), primary_key=True)
#     description = Column(String(50))
#     numericweight = Column(Float, index=True, server_default=text("0"))
#     notes = Column(String(255))


# class TRoleconstraint(Base):
#     __tablename__ = 't_roleconstraint'

#     connectorid = Column(Integer, primary_key=True, nullable=False, index=True, server_default=text("0"))
#     Constraint = Column(String(255), primary_key=True, nullable=False, index=True)
#     connectorend = Column(String(50), primary_key=True, nullable=False)
#     constrainttype = Column(String(12), primary_key=True, nullable=False)
#     notes = Column(Text)


# t_t_rtf = Table(
#     't_rtf', metadata,
#     Column('type', String(50)),
#     Column('template', Text)
# )


# class TRtfreport(Base):
#     __tablename__ = 't_rtfreport'

#     templateid = Column(String(200), primary_key=True)
#     rootpackage = Column(Integer, server_default=text("0"))
#     filename = Column(String(255))
#     details = Column(Integer, server_default=text("0"))
#     processchildren = Column(Integer, server_default=text("0"))
#     showdiagrams = Column(Integer, server_default=text("0"))
#     heading = Column(String(255))
#     requirements = Column(Integer, server_default=text("0"))
#     associations = Column(Integer, server_default=text("0"))
#     scenarios = Column(Integer, server_default=text("0"))
#     childdiagrams = Column(Integer, server_default=text("0"))
#     attributes = Column(Integer, server_default=text("0"))
#     methods = Column(Integer, server_default=text("0"))
#     imagetype = Column(Integer, server_default=text("0"))
#     paging = Column(Integer, server_default=text("0"))
#     intro = Column(Text)
#     resources = Column(Integer, server_default=text("1"))
#     constraints = Column(Integer, server_default=text("1"))
#     tagged = Column(Integer, server_default=text("0"))
#     showtag = Column(Integer, server_default=text("0"))
#     showalias = Column(Integer, server_default=text("0"))
#     pdata1 = Column(String(255))
#     pdata2 = Column(String(255))
#     pdata3 = Column(String(255))
#     pdata4 = Column(Text)


# class TRule(Base):
#     __tablename__ = 't_rules'

#     ruleid = Column(String(50), primary_key=True)
#     rulename = Column(String(255), nullable=False)
#     ruletype = Column(String(255), nullable=False)
#     ruleactive = Column(Integer)
#     errormsg = Column(String(255))
#     flags = Column(String(255))
#     ruleocl = Column(Text)
#     rulexml = Column(Text)
#     notes = Column(Text)


# class TScenariotype(Base):
#     __tablename__ = 't_scenariotypes'

#     scenariotype = Column(String(12), primary_key=True)
#     description = Column(String(50))
#     numericweight = Column(Float, index=True, server_default=text("1"))
#     notes = Column(String(255))


# class TScript(Base):
#     __tablename__ = 't_script'

#     scriptid = Column(Integer, primary_key=True, server_default=text("nextval(('scriptid_seq'::text)::regclass)"))
#     scriptcategory = Column(String(100), index=True)
#     scriptname = Column(String(150))
#     scriptauthor = Column(String(255))
#     notes = Column(Text)
#     script = Column(Text)


# class TSecgroup(Base):
#     __tablename__ = 't_secgroup'

#     groupid = Column(String(40), primary_key=True)
#     groupname = Column(String(32), nullable=False)
#     description = Column(String(100))


# class TSecgrouppermission(Base):
#     __tablename__ = 't_secgrouppermission'

#     groupid = Column(String(40), primary_key=True, nullable=False)
#     permissionid = Column(Integer, primary_key=True, nullable=False)


# class TSeclock(Base):
#     __tablename__ = 't_seclocks'
#     __table_args__ = (
#         Index('ix_seclocks_entityidusrtype', 'entityid', 'userid', 'entitytype'),
#         Index('ix_seclocks_entityiduserid', 'entityid', 'userid'),
#         Index('ix_seclocks_entityidtype', 'entityid', 'entitytype'),
#         Index('ix_seclocks_groupiduserid', 'groupid', 'userid')
#     )

#     userid = Column(String(40), nullable=False)
#     groupid = Column(String(40), index=True)
#     entitytype = Column(String(32), nullable=False)
#     entityid = Column(String(40), primary_key=True)
#     timestamp = Column(DateTime, nullable=False)
#     locktype = Column(String(255))


# class TSecpermission(Base):
#     __tablename__ = 't_secpermission'

#     permissionid = Column(Integer, primary_key=True)
#     permissionname = Column(String(50), nullable=False)


# class TSecpolicy(Base):
#     __tablename__ = 't_secpolicies'

#     property = Column(String(100), primary_key=True)
#     value = Column(String(255), nullable=False)


# class TSecuser(Base):
#     __tablename__ = 't_secuser'

#     userid = Column(String(40), primary_key=True)
#     userlogin = Column(String(255), nullable=False)
#     firstname = Column(String(50), nullable=False)
#     surname = Column(String(50), nullable=False)
#     department = Column(String(50))
#     password = Column(String(12))


# class TSecusergroup(Base):
#     __tablename__ = 't_secusergroup'

#     userid = Column(String(40), primary_key=True, nullable=False)
#     groupid = Column(String(40), primary_key=True, nullable=False)


# class TSecuserpermission(Base):
#     __tablename__ = 't_secuserpermission'

#     userid = Column(String(40), primary_key=True, nullable=False)
#     permissionid = Column(Integer, primary_key=True, nullable=False)


# class TSnapshot(Base):
#     __tablename__ = 't_snapshot'

#     snapshotid = Column(String(40), primary_key=True)
#     seriesid = Column(String(40), nullable=False, index=True)
#     position = Column(Integer, index=True)
#     snapshotname = Column(String(100))
#     notes = Column(Text)
#     style = Column(String(255))
#     elementid = Column(String(40), nullable=False)
#     elementtype = Column(String(50), nullable=False)
#     strcontent = Column(Text)
#     bincontent1 = Column(LargeBinary)
#     bincontent2 = Column(LargeBinary)


# class TStatustype(Base):
#     __tablename__ = 't_statustypes'

#     status = Column(String(50), primary_key=True)
#     description = Column(String(50))


# class TStereotype(Base):
#     __tablename__ = 't_stereotypes'

#     stereotype = Column(String(255), primary_key=True, nullable=False, index=True)
#     appliesto = Column(String(255), primary_key=True, nullable=False)
#     description = Column(String(255))
#     mfenabled = Column(Integer, server_default=text("0"))
#     mfpath = Column(String(255))
#     metafile = Column(LargeBinary)
#     style = Column(Text)
#     ea_guid = Column(String(50), index=True)
#     visualtype = Column(String(100))


# class TTaggedvalue(Base):
#     __tablename__ = 't_taggedvalue'

#     propertyid = Column(String(40), primary_key=True)
#     elementid = Column(String(40), nullable=False, index=True)
#     baseclass = Column(String(100), nullable=False)
#     tagvalue = Column(Text)
#     notes = Column(Text)


# class TTask(Base):
#     __tablename__ = 't_tasks'

#     taskid = Column(Integer, primary_key=True, server_default=text("nextval(('taskid_seq'::text)::regclass)"))
#     name = Column(String(255))
#     tasktype = Column(String(255))
#     notes = Column(Text)
#     priority = Column(String(255))
#     status = Column(String(255))
#     owner = Column(String(255))
#     startdate = Column(Date)
#     enddate = Column(Date)
#     phase = Column(String(50))
#     history = Column(Text)
#     percent = Column(Integer)
#     totaltime = Column(Integer)
#     actualtime = Column(Integer)
#     assignedto = Column(String(100))


# class TTcf(Base):
#     __tablename__ = 't_tcf'

#     tcfid = Column(String(12), primary_key=True)
#     description = Column(String(50))
#     weight = Column(Float, index=True, server_default=text("1"))
#     value = Column(Float, server_default=text("0"))
#     notes = Column(String(255))


# class TTemplate(Base):
#     __tablename__ = 't_template'

#     templateid = Column(String(40), primary_key=True)
#     templatetype = Column(String(50), nullable=False)
#     templatename = Column(String(100), nullable=False)
#     notes = Column(String(255))
#     style = Column(String(255))
#     template = Column(Text)


# class TTestclas(Base):
#     __tablename__ = 't_testclass'

#     testclass = Column(String(50), primary_key=True)
#     description = Column(String(50))


# class TTestplan(Base):
#     __tablename__ = 't_testplans'

#     planid = Column(String(50), primary_key=True)
#     category = Column(String(100))
#     name = Column(String(150), nullable=False)
#     author = Column(String(255))
#     notes = Column(Text)
#     testplan = Column(Text, nullable=False)


# class TTesttype(Base):
#     __tablename__ = 't_testtypes'

#     testtype = Column(String(12), primary_key=True)
#     description = Column(String(50))
#     numericweight = Column(Float, index=True, server_default=text("1"))
#     notes = Column(String(255))


# class TTrxtype(Base):
#     __tablename__ = 't_trxtypes'

#     description = Column(String(50), index=True)
#     numericweight = Column(Float, index=True, server_default=text("1"))
#     notes = Column(Text)
#     trx = Column(String(255), index=True)
#     trx_id = Column(Integer, primary_key=True, server_default=text("nextval(('trx_id_seq'::text)::regclass)"))
#     style = Column(Text)


# class TUmlpattern(Base):
#     __tablename__ = 't_umlpattern'

#     patternid = Column(Integer, primary_key=True, server_default=text("nextval(('patternid_seq'::text)::regclass)"))
#     patterncategory = Column(String(100))
#     patternname = Column(String(150))
#     style = Column(String(255))
#     notes = Column(Text)
#     patternxml = Column(Text)
#     version = Column(String(50))


# class TVersion(Base):
#     __tablename__ = 't_version'

#     elementid = Column(String(50), primary_key=True, nullable=False, index=True)
#     versionid = Column(String(255), primary_key=True, nullable=False)
#     elementtype = Column(String(100), nullable=False)
#     flags = Column(String(255))
#     externalfile = Column(String(255))
#     notes = Column(String(255))
#     owner = Column(String(255))
#     versiondate = Column(DateTime)
#     branch = Column(String(255))
#     elementxml = Column(Text)


# class TXref(Base):
#     __tablename__ = 't_xref'
#     __table_args__ = (
#         Index('ix_xref_nametype', 'name', 'type'),
#     )

#     xrefid = Column(String(255), primary_key=True)
#     name = Column(String(255), index=True)
#     type = Column(String(255), index=True)
#     visibility = Column(String(255))
#     namespace = Column(String(255))
#     requirement = Column(String(255))
#     Constraint = Column(String(255))
#     behavior = Column(String(255))
#     partition = Column(String(255))
#     description = Column(Text)
#     client = Column(String(255), index=True)
#     supplier = Column(String(255), index=True)
#     link = Column(String(255))


# class TXrefsystem(Base):
#     __tablename__ = 't_xrefsystem'

#     xrefid = Column(String(255), primary_key=True)
#     name = Column(String(255))
#     type = Column(String(255), index=True)
#     visibility = Column(String(255))
#     namespace = Column(String(255))
#     requirement = Column(String(255))
#     Constraint = Column(String(255))
#     behavior = Column(String(255))
#     partition = Column(String(255))
#     description = Column(Text)
#     client = Column(String(255), index=True)
#     supplier = Column(String(255), index=True)
#     link = Column(String(255))
#     toolid = Column(String(50))


# class TXrefuser(Base):
#     __tablename__ = 't_xrefuser'

#     xrefid = Column(String(255), primary_key=True)
#     name = Column(String(255))
#     type = Column(String(255), index=True)
#     namespace = Column(String(255))
#     requirement = Column(String(255))
#     Constraint = Column(String(255))
#     behavior = Column(String(255))
#     partition = Column(String(255))
#     description = Column(Text)
#     client = Column(String(255), index=True)
#     supplier = Column(String(255), index=True)
#     link = Column(String(255))
#     toolid = Column(String(50))
#     visibility = Column(String(255))


# class UsysSchema(Base):
#     __tablename__ = 'usys_schema'

#     V1558 = Column(String(255), primary_key=True)


# class UsysSystem(Base):
#     __tablename__ = 'usys_system'

#     property = Column(String(50), primary_key=True)
#     value = Column(String(50))


# t_usysoldtables = Table(
#     'usysoldtables', metadata,
#     Column('tablename', String(50)),
#     Column('newname', String(50)),
#     Column('relorder', Integer, server_default=text("0")),
#     Column('fixcode', Integer, nullable=False, server_default=text("0"))
# )


# t_usysqueries = Table(
#     'usysqueries', metadata,
#     Column('queryname', String(50)),
#     Column('newname', String(50)),
#     Column('fixcode', Integer, nullable=False)
# )


# class Usystable(Base):
#     __tablename__ = 'usystables'

#     tablename = Column(String(50), primary_key=True)
#     relorder = Column(Integer, server_default=text("0"))
#     displayname = Column(String(50))
#     fromver = Column(String(50))
#     tover = Column(String(50))
