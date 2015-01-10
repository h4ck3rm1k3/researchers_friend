"""Create the researcher administrative data models.

Exports:
    Classes:
        Researcher
        Project
        ResearcherProject
        SuretyScheme
        SuretySchemePart
        Activity
        AdministrativeTask
        Search
        ResearchObjective
        SourceGroup
"""
from django.conf import settings
from django.db import models


# Administrative Submodel
class Researcher(models.Model):

    """The person gathering data.

    Information about a genealogical researcher that identifies who is
    responsible for any particular piece of data in the system.

    The RESEARCHER entity allows genealogical data to be linked to
    the particular person who gathered that data, whether raw evidence
    or conclusions based on evidence (or based on nothing at all in the
    case of poor research).  Although the RESEARCHER entity is very
    useful for group efforts such as one-name studies, it is also
    necessary so that data that enters or leaves the system can be
    attributed to a researcher.

    Type: Independent.  Data about RESEARCHER can be entered without
        regard to any other entity.

    Relationships:
        One RESEARCHER participates in zero to many PROJECTs (through
            RESEARCHER-PROJECT).
        The data for one PROJECT comes from one to many RESEARCHERs
            (through RESEARCHER-PROJECT).
        A RESEARCHER lives in one PLACE.
        A RESEARCHER performs zero to many SEARCHs.
        A SEARCH is made by one and only one RESEARCHER.
        A RESEARCHER makes zero to many ASSERTIONs.
        An ASSERTION is made by one and only one RESEARCHER.

    Instance Variables:
        name -- The full name of the researcher, suitable for reports.
        address -- (foreign key) The address of the researcher. Part of
            the address is connected to Place-ID in PLACE.
        comments -- Comments about the researcher, if necessary.
    """

    name = models.CharField('researcher\'s full name', max_length=128)
    address = models.ForeignKey(
        'Place',
        blank=True,
        verbose_name='researcher\'s address place'
    )
    comments = models.TextField('comments about the researcher', blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        """Stringify the researcher.

        Arguments:
            self
        Returns: the name of the researcher
        """
        return self.name


class Project(models.Model):

    """Projects worked on by researchers.

    Information about the genealogical research project. One project
    might consist of all information about a person's ancestors, both on
    the researcher's father's side, and on the researcher's mother's
    side.  Another project is all the ancestors on only one side of the
    researcher's family, such as the mother's side; this researcher
    might have another project for the father's side.  Another project
    is a one-name study. Other types of genealogical projects include a
    study of the descendants of a particular person or couple, and the
    descendants of a particular group of people.  Finally, a project can
    be undertaken for another person, in which case there is a client
    associated with the project.  Note that client data is shown as an
    undefined attribute on the model, but would actually be a model
    extension for professional genealogists.

    The PROJECT entity identifies one or more projects that the
    researcher is interested in. It is linked to the RESEARCHER entity
    with an associative RESEARCHER-PROJECT entity required because one
    researcher may work on zero to many projects and one project can
    have zero to many researchers. After data becomes available, of
    course, a project must have at least one researcher.
    entities.

    PROJECT is associated with zero to many RESEARCH-OBJECTIVEs as shown
    in the rest of the Administration Submodel

    Type: Independent.  Does not depend on any other entities.

    Relationships:
        One PROJECT is worked on by one to many RESEARCHERs (through
            RESEARCHER-PROJECT).
        One PROJECT has zero to many RESEARCH-OBJECTIVEs.
        One PROJECT relies on zero or one SURETY-SCHEME.
        One SURETY-SCHEME can be used for zero to many PROJECTs.

    Instance Variables:
        name -- The name of the project, such as "John F. Kennedy
            Ancestors", or "Mayflower Descendants".
        description -- A text description of the project that provides
            additional information about the scope of the project, or
            any other necessary supporting information.
        client_data -- If the project is undertaken for a client, the
            client name and address is included.  An actual
            implementation for commercial genealogical purposes might
            have one or more separate entities for client information
            so that, for example, one client could commission one or
            more projects.  Other information such as billing rates,
            expense logs, hour logs, and invoicing could be part of that
            system, but is not included in this basic genealogical data
            model.
        surety_scheme -- The optional surety scheme used with this
            project.
        researchers -- (many-to-many) The researchers working on this project
    """

    name = models.CharField('project name', max_length=128)
    description = models.TextField('project description', blank=True)
    client_data = models.TextField('project client information', blank=True)
    surety_scheme = models.ForeignKey(
        'SuretyScheme',
        blank=True,
        null=True,
        verbose_name='surety scheme used by the project'
    )
    researchers = models.ManyToManyField(
        Researcher,
        through='ResearcherProject',
        verbose_name='researchers working on the project',
        blank=True
    )

    def __str__(self):
        """Stringify the project.

        Arguments:
            self
        Returns: the name of the project
        """
        return self.name


class ResearcherProject(models.Model):

    """ Intermediate model for Researcher and Project.

    Associative entity that ties together RESEARCHER and PROJECT so that
    one RESEARCHER can work on zero to many PROJECTs and one PROJECT can
    have one to many RESEARCHERs.

    Type: Dependent.  Requires RESEARCHER and PROJECT.

    Relationships:
        One RESEARCHER-PROJECT describes one PROJECT.
        One PROJECT has one to many RESEARCHER-PROJECTs.
        One RESEARCHER-PROJECT is worked on by one RESEARCHER.
        One RESEARCHER works on zero to many RESEARCHER-PROJECTs.

    Instance Variables:
        researcher -- (foreign key) Unique key that indicates which
            RESEARCHER.
        project -- (foreign key) Unique key that indicates which
            PROJECT.
        role -- If it is necessary to describe the role that a
            particular RESEARCHER played, this field can differentiate
            different people on a group effort.
    """

    researcher = models.ForeignKey(Researcher)
    project = models.ForeignKey(Project)
    role = models.CharField(
        'researcher\'s role on project',
        max_length=64,
        blank=True
    )


class SuretyScheme(models.Model):

    """ Scheme representing how sure a researcher is of data gathered.

    The scheme used to establish the surety level of assertions made for
    a particular project.  Different researchers may use different
    schemes such as "1 to 3" or "1 to 5" or "E, F, P", and in order to
    understand the researcher's evaluations, it is necessary to
    understand the particular scheme in use. Our standard requires that
    the scheme sort high as the most reliable.

    Every PROJECT has associated with it a SURETY scheme used to express
    how certain the researcher is of the data gathered.  Although many
    people use the same scheme, as implemented in certain software or
    elsewhere, the data model allows different schemes to be used.
    Note, however, that the scheme used with a particular project is
    attached to the data that it describes; this means that an export
    specification can send the surety scheme along with the data.

    Type: Independent.  Requires no other entities.

    Relationships:
        One SURETY-SCHEME is used in zero to many PROJECTs.
        One PROJECT uses zero to one SURETY-SCHEMEs.
        One SURETY-SCHEME has one to many SURETY-SCHEME-PARTs.
        One SURETY-SCHEME-PART belongs to one SURETY-SCHEME.

    Instance Variables:
        name -- The name of the surety scheme.
        description -- A general description of the
            SURETY-SCHEME, if necessary.
    """

    name = models.CharField('surety scheme name', max_length=64)
    description = models.TextField(
        'surety scheme description',
        blank=True
    )

    def __str__(self):
        """Stringify the surety scheme.

        Arguments:
            self
        Returns: the name of the surety scheme
        """
        return self.name


class SuretySchemePart(models.Model):

    """ The different levels of surety in the scheme.

    Contains information about the individual parts of the
    SURETY-SCHEME.  For example, if the scheme is simply 1 to 5, then
    this entity lists the 5 levels and no further information may be
    required, other than a sequencer to determine what order the parts
    are in.  However, the RESEARCHER may (and really should) choose to
    more fully explain what each surety level means.

    Type: Dependent.  Requires SURETY-SCHEME.

    Relationships:
        One SURETY-SCHEME-PART is part of one SURETY-SCHEME.
        One SURETY-SCHEME has one to many SURETY-SCHEME-PARTs.  The one
            condition is unusual, but is useful if a researcher chooses
            to treat all evidence as the same surety level.
        One SURETY-SCHEME-PART describes zero to many ASSERTIONs.
        One ASSERTION is categorized by zero to one SURETY-SCHEME-PARTs.
            Note that in this model the RESEARCHER assigns surety levels
            to the ASSERTIONs made from the direct evidence, not to the
            evidence itself, but functionally this amounts to the same
            thing since the ASSERTIONs are closely coupled to the
            various levels of SOURCE.

    Instance Variables:
        surety_scheme -- (foreign key) Unique identifier that determines
            to what SURETY-SCHEME this part belongs.
        name -- The name of the SURETY-SCHEME-PART such as "1" or "G".
        description -- An explanation of what the SURETY-SCHEME-PART
            means.  If "2" in one scheme or "G" in another stands for
            "Good", for example, how does the RESEARCHER define "good"?
            What kinds of data would routinely be assigned a level of
            "good" instead of some other category?
        sequence_number -- An alphanumeric sequencer that sorts the most
            reliable SURETY-SCHEME-PART high. For example, if "1, 2, 3"
            is used by one researcher, and "1" is the most sure, then
            the corresponding ranks might also be 1, 2, and 3.  If
            another researcher uses the same "1, 2, 3" but 3 is the most
            sure, then the corresponding ranks might be C, B, and A to
            force the list to come out 3, 2, 1.
    """

    surety_scheme = models.ForeignKey(
        SuretyScheme,
        verbose_name='surety scheme this part belongs to'
    )
    name = models.CharField('surety scheme part name', max_length=1)
    description = models.TextField(
        'surety scheme part description',
        blank=True
    )
    sequence_number = models.PositiveSmallIntegerField(
        'surety part sequence number',
        default=0
    )

    def __str__(self):
        """Stringify the surety scheme part.

        Arguments:
            self
        Returns: the name of the surety scheme part
        """
        return self.name


class Activity(models.Model):

    """Some activity related to a project: either search or admin task.

    Contains information about an activity such as a SEARCH or an
    ADMINISTRATIVE-TASK that must be, or was, accomplished. ACTIVITY
    allows the researcher to translate RESEARCH-OBJECTIVEs into specific
    action items.  Note that ACTIVITY has two sub-entities:
    ADMINISTRATIVE-TASK and SEARCH.  It contains the attributes that are
    common to both sub-entity.

    The RESEARCH-OBJECTIVEs are linked to specific ACTIVITYs such as a
    SEARCH or an ADMIN-TASK, planned or already executed.

    Type: Dependent.  Requires RESEARCH-OBJECTIVE through
        RESEARCH-OBJECTIVE-ACTIVITY.

    Relationships:
        One ACTIVITY is the result of zero to many RESEARCH-OBJECTIVEs
            (through RESEARCH-OBJECTIVE-ACTIVITY).  The zero condition
            addresses random or spontaneous activities that are not part
            of a pre-planned RESEARCH-OBJECTIVE.
        One RESEARCH-OBJECTIVE results in zero to many ACTIVITYs.
        One RESEARCHER undertakes zero to many ACTIVITYs.
        One ACTIVITY is performed by one RESEARCHER.
        One ACTIVITY is about either an ADMINSTRATIVE-TASK or a SEARCH.
        An ADMINSTRATIVE-TASK is a type of ACTIVITY.
        A SEARCH is a type of ACTIVITY.

    Instance Variables:
        researcher -- (foreign key) The unique key in RESEARCHER that
            identifies the person who either did or will do this
            ACTIVITY.
        scheduled_date -- The date that the researcher plans to conduct
            this ACTIVITY.
        completed_date -- The date that the researcher completed this
            ACTIVITY.  If this is blank, then the ACTIVITY has not been
            completed.
        typecode -- This indicates whether the ACTIVITY is an
            ADMINISTRATIVE-TASK or a SEARCH.
        status -- This describes the status of the ACTIVITY.  Besides
            the obvious category of "Completed" which is redundant with
            Completed-Date having a value, other status indicators might
            be "waiting", "on hold", or some other value.
        description -- A short description of the ACTIVITY.
        priority -- A code indicating the priority the researcher sets
            on this activity.
        comments -- Any comments that are required about this ACTIVITY.
    """
    researcher = models.ForeignKey(
        Researcher,
        verbose_name='researcher'
    )
    scheduled_date = models.DateField('date scheduled')
    completed_date = models.DateField('date completed')
    typecode = models.CharField(
        max_length=1,
        choices=(('A', 'Administrative Task'), ('S', 'Search')),
        editable=False
    )
    status = models.CharField('status', max_length=64)
    description = models.TextField('description')
    priority = models.PositiveSmallIntegerField('priority')
    comments = models.TextField('comments', blank=True)

    def __str__(self):
        """Stringify the activity.

        Arguments:
            self
        Returns: the description of the activity
        """
        return self.description

    class Meta:

        """Metadata for the model."""

        verbose_name_plural = "activities"


class AdministrativeTask(Activity):

    """Some administrative task related to a research objective.

    A sub-entity of ACTIVITY that holds information related to various
    administrative chores other than conducting a genealogical SEARCH.
    Currently this is a rather bland entity, and mostly serves to
    indicate that an ACTIVITY is not a SEARCH and thus does not have the
    additional attributes required of a genealogical SEARCH.

    Type: Dependent.  Requires ACTIVITY because it is a sub-entity.

    Relationships: An ADMINISTRATIVE-TASK is a sub-entity of ACTIVITY.
        Each ACTIVITY has either an ADMINISTRATIVE-TASK or a SEARCH.

    Instance Variables:
        activity -- (primary/foreign key) Unique key that identifies a
            SEARCH as a subtype of an ACTIVITY.
    """

    activity = models.OneToOneField(
        Activity,
        primary_key=True,
        verbose_name='activity this task inherits from',
        parent_link=True,
        editable=False
    )

    def __init__(self, *args, **kwargs):
        """Override init to set activity typecode."""
        self.typecode = 'A'
        super(AdministrativeTask, self).__init__(*args, **kwargs)


class Search(Activity):

    """An examination of a source for particular data.

    A specific examination of a SOURCE to find information, usually
    based on a RESEARCH-OBJECTIVE, although a SEARCH can be conducted
    with no RESEARCH-OBJECTIVE in mind, particularly where it is a
    casual search based on an unplanned or unexpected opportunity.

    The concept of SEARCH is heavily influenced by the need to record
    what data the RESEARCHER looked for in a particular SOURCE on a
    particular research trip, to avoid having to look up that data
    again.  A SEARCH can return specific data, or a SEARCH can result in
    not finding the data searched for, which is, of course, significant
    in itself.

    A SEARCH takes place at a particular repository, on a date, using a
    SOURCE (like a will book), and consists of examining the SOURCE for
    a particular person name or names, a particular place name or names,
    or other data.  Thus, the SEARCH is the end of this particular chain
    of entities in the Administration Submodel, and links to the
    Evidence Submodel.

    Type: Dependent.  Requires SOURCE or REPOSITORY.  Also requires
        RESEARCHER.  Also a subtype of ACTIVITY (along with
        ADMINISTRATION-TASK) and thus usually but not always requires a
        RESEARCH-OBJECTIVE as well.

    Relationships:
        One SOURCE takes place in one REPOSITORY-SOURCE.
        One SEARCH is conducted in zero to one REPOSITORYs (through
            REPOSITORY-SOURCE).
        One REPOSITORY is the scene of zero to many SEARCHs (through
            REPOSITORY-SOURCE).
        One SEARCH is conducted in zero to one SOURCEs (through
            REPOSITORY-SOURCE).
        One SOURCE provides data for zero to many SEARCHs (through
            REPOSITORY-SOURCE).

    Instance Variables:
    activity -- (primary/foreign key) Unique key that identifies a
        SEARCH as a subtype of an ACTIVITY.
    source -- Unique key that identifies a SOURCE that this SEARCH took
        place in.  If the SEARCH was a general SEARCH in a REPOSITORY,
        for example to determine what suitable materials the REPOSITORY
        contains, this may be blank.
    repository -- (foreign key) Unique key that identifies a REPOSITORY.
        This is a required attribute and cannot be blank.
    searched_for -- The text, such as a surname and certain variations,
        searched for.

    """

    activity = models.OneToOneField(
        Activity,
        primary_key=True,
        verbose_name='activity this search inherits from',
        parent_link=True,
        editable=False
    )
    source = models.ForeignKey(
        'RepositorySource',
        verbose_name='source searched',
        related_name='source_searches'
    )
    repository = models.ForeignKey(
        'RepositorySource',
        verbose_name='repository searched',
        related_name='repository_searches'
    )
    searched_for = models.TextField('text searched for')

    def __init__(self, *args, **kwargs):
        """Override init to set activity typecode."""
        self.typecode = 'S'
        super(Search, self).__init__(*args, **kwargs)

    def __str__(self):
        """Stringify the search.

        Arguments:
            self
        Returns: the text searched for
        """
        return self.searched_for

    class Meta:

        """Metadata for the model."""

        verbose_name_plural = "searches"


class ResearchObjective(models.Model):

    """ The problem the researcher is trying to solve.

    Contains information about the RESEARCH-OBJECTIVEs that the
    RESEARCHER has determined are appropriate for the specific PROJECT.
    For example, one objective might be to "Find the father of John
    Smith."

    Researchers can specify their goals in RESEARCH-OBJECTIVE.  The data
    in RESEARCH-OBJECTIVE explains what research problem the genealogist
    is attempting to solve.

    Type: Dependent.  Requires PROJECT.

    Relationships:
        One PROJECT has zero to many RESEARCH-OBJECTIVEs.
        One RESEARCH-OBJECTIVE applies to one PROJECT.
        One RESEARCH-OBJECTIVE results in zero to many ACTIVITYs
            (through RESEARCH-OBJECTIVE-ACTIVITY).
        One ACTIVITY is associated with zero to many RESEARCH-OBJECTIVEs
            (through RESEARCH-OBJECTIVE-ACTIVITY).

    Instance Variables:
        project -- (foreign key) Unique key that identifies the PROJECT
            that this RESEARCH-OBJECTIVE belongs to.
        name -- The name of the RESEARCH-OBJECTIVE.
        description -- A more detailed description of the
            RESEARCH-OBJECTIVE.
        sequence_number -- A value that keeps the RESEARCH-OBJECTIVEs
            sorted in any order that the RESEARCHER wants.
        priority -- The priority assigned to this RESEARCH-OBJECTIVE by
            the RESEARCHER.
        status -- The status of this RESEARCH-OBJECTIVE such as "Open"
            or "Closed".
        activities -- (many-to-many) The activities undertaken to
            further this objective.
    """

    project = models.ForeignKey(
        Project,
        verbose_name='project this objective belongs to'
    )
    name = models.CharField('research objective name', max_length=128)
    description = models.TextField('research objective descriptin', blank=True)
    sequence_number = models.PositiveSmallIntegerField(
        'research objective sequence number',
        default=0
    )
    priority = models.PositiveSmallIntegerField(
        'research objective priority'
    )
    status = models.CharField('research objective status', max_length=64)
    activities = models.ManyToManyField(
        Activity,
        verbose_name='activities undertaken to further this objective',
        blank=True
    )

    def __str__(self):
        """Stringify the research objective.

        Arguments:
            self
        Returns: the name of the research objective
        """
        return self.name


class SourceGroup(models.Model):

    """ Groups of related sources.

    Contains a list of groups of SOURCEs such as "Federal Census",
    "Will", "Deed", and so forth.  This is necessary in some cases so
    that data can be searched, selected, sorted, and grouped by type of
    SOURCE; without an explicit SOURCE-GROUP it may not be clear what
    type of record is represented by the SOURCE, although in most cases
    the title is explicit enough. However, some researchers may wish to
    group SOURCEs of particular interest such as "New England Sources",
    "Massachusetts Sources", or "Boston Sources".  Consequently, a
    SOURCE can be in more than one group and in the examples above more
    than one group scheme.

    At the higher levels of SOURCE, for example, one might want to
    create a SOURCE-GROUP which includes all those sources which one
    would search for a certain county in which one frequently works.
    At a lower level in the SOURCE hierarchy, one might create a
    SOURCE-GROUP for a set of records which are related in some way,
    perhaps a series of tax lists for one town or county.

    Type: Independent.  Does not require any other entities.

    Relationships:
        One SOURCE-GROUP represents the type of source for zero to many
            SOURCEs (through SOURCE-SOURCE-GROUP).
        One SOURCE belongs to zero to many SOURCE-GROUPs (through
            SOURCE-SOURCE-GROUP).  (Although zero to one is the normal
            condition, this allows the RESEARCHER to use multiple
            grouping concepts for the same SOURCEs.)

    Instance Variables:
        name -- The name of the SOURCE-GROUP such as "Will", "Deed", or
            "Tombstone"
    """

    name = models.CharField('category of sources', max_length=128)

    def __str__(self):
        """Stringify the source group.

        Arguments:
            self
        Returns: the name of the source group
        """
        return self.name
