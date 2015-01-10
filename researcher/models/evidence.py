"""Create the researcher evidence data models.

Exports:
    Classes:
        Source
        Repository
        RepositorySource
        Representation
        RepresentationType
        CitationPart
        CitationPartType
"""
from django.db import models


# Evidence Models
class Source(models.Model):

    """A genealogical source.

    A collection of data useful for genealogical research such as a will
    book, a deed book, a compiled genealogy in book pr periodical form,
    an electronic database, or similar collection.  SOURCEs include both
    primary and secondary works.  Generally a SOURCE will have one or
    more documents such as specific wills inside the will book; in many
    cases there will be additional levels of SOURCE.  In some cases, the
    SOURCE has only one level; what we might think of as a document is
    conceptually the same as the SOURCE.  Thus, SOURCE is
    self-referential and can handle data of any reasonable number of
    hierarchical levels.

    Note that SOURCE is self-referential.  Each high level SOURCE may
    have zero to many lower level SOURCEs.  This concept is best seen in
    the following chart showing a hierarchy of SOURCEs in the records of
    one particular court.

    Initially, it is tempting to break SOURCE up into perhaps DOCUMENT
    and RECORD or some similar scheme until the actual EXCERPT level is
    reached.1  However, an example like this one quickly shows that we
    cannot count on a particular number of levels in SOURCE for all
    records.  This example has four levels above the excerpt level; many
    examples with fewer levels come to mind, and there are probably
    examples with even more levels.  Thus, the only logical way to model
    SOURCE data is as a self-referential hierarchy with an unknown
    number of levels.

    SOURCEs include both primary and secondary works.  There are a large
    number of possible genealogical SOURCEs such as will books, deed
    books, compiled genealogies in book or periodical form, and
    electronic databases.  If there are multiple copies of a SOURCE,
    break them out at the lower level of the SOURCE hierarchy, and draw
    the ASSERTION from that level or lower.

    If a SEARCH is a repository-wide search for particular types of
    records, for example, there will be zero SOURCEs associated with the
    SEARCH.  If the SEARCH takes place in a particular document, there
    will be one SEARCH for one SOURCE.

    In reversing this situation, however, it is possible to note a
    SOURCE without actually searching it, or we might search for one or
    more items in the source.  Consequently one SOURCE has zero to many
    SEARCHs, and one SEARCH has zero to one SOURCE.

    We also have a SOURCE-GROUP entity (in the Administration submodel)
    that allows us to group different kinds of records together, so that
    we can search our database for records from certain kinds of
    sources, such as only wills, or only census records.

    The SOURCE entity contains none of the information required in the
    citation such as the title and author, or any of the other
    'book-level' data associated with the many kinds of sources.

    Type: Independent.  Does not require any other entities.

    Relationships:
        One high level SOURCE has zero to many lower level SOURCEs.
        One low level SOURCE can belong to zero to one higher level
            SOURCE.
        One SOURCE is part of zero to many SOURCE-GROUPs (through
            SOURCE-GROUP-SOURCE).
        One SOURCE-GROUP contains zero to many SOURCEs (through
            SOURCE-GROUP-SOURCE).
        One SOURCE is the object of zero to many SEARCHs  (through
            REPOSITORY-SOURCE).
        One SEARCH takes place in zero to one SOURCEs (through
            REPOSITORY-SOURCE).  A SEARCH either takes place in a
            RESPOSITORY (general SEARCH) or it takes place in a SOURCE
            (specific SEARCH).
        One SOURCE is found in zero to many REPOSITORYs  (through
            REPOSITORY-SOURCE).  The zero condition indicates a SOURCE
            that cannot presently be associated with a particular
            REPOSITORY, i.e., the RESEARCHER knows it exists, but does
            not know where to find it.
        One REPOSITORY contains zero to many SOURCEs (through
            REPOSITORY-SOURCE).
        One SOURCE was originally compiled about one jurisdiction PLACE
            and one SOURCE is about a person from one PLACE (which may
            not be the same as the jurisdiction PLACE).  (Thus one
            SOURCE is about exactly two PLACEs.)
        One PLACE is associated with zero to many SOURCE jurisdictions
            and zero to many SOURCE persons.
        One SOURCE has zero to many REPRESENTATIONs, meaning that we
            might have text representing the SOURCE as well as a
            photocopy or a photograph, or some other multimedia
            REPRESENTATION.
        A REPRESENTATION applies to only one SOURCE.  (In an example
            like a photocopy that contains two small wills, the
            RESEARCHER can simply list the same Physical-File-Code for
            both REPRESENTATIONs.)
        One SOURCE has many CITATION-PARTs.  For example, at the book
            level, a SOURCE has a title, author, place of publication,
            and many other parts.
        One CITATION-PART cites one SOURCE.

    Instance Variables:
        higher_source -- (foreign key) Unique key that identifies the
            next higher level SOURCE associated with this SOURCE.
        subject_place -- (foreign key) Unique key that identifies the
            PLACE of the subject of this SOURCE.  Example:  A record in
            North Carolina describes a person and their activities in
            Georgia. Georgia is the subject place, and North Carolina is
            the record jurisdiction place.
        jurisdiction_place -- (foreign key) Unique key that identifies
            the PLACE of the jurisdiction of the record.
        researcher -- (foreign key) Unique key in RESEARCHER that
            identifies the person who gathered this SOURCE record.
        subject_date -- The date associated with the subject of this
            SOURCE.  Note that there can be a somewhat different date
            associated with each level of a multi level SOURCE, such as
            a date range for a will book, and a more specific date for
            the will itself, and then perhaps other dates associated
            with small pieces of information in the will.
        comments -- Any comments about the SOURCE that are required.  If
            the SOURCE is at the level of a whole 'book' for example,
            such as a will book, the comments may describe the poor
            condition and the difficulty in reading most entries.
        repositories -- The repositories in which the source can be
            found
    """

    higher_source = models.ForeignKey(
        'self',
        verbose_name='higher-level source that contains this source',
        blank=True
    )
    subject_place = models.ForeignKey(
        'Place',
        verbose_name='place described by the source',
        related_name='subject_sources'
    )
    jurisdiction_place = models.ForeignKey(
        'Place',
        verbose_name='place where source was created or stored',
        related_name='jurisdiction_sources'
    )
    researcher = models.ForeignKey(
        'Researcher',
        verbose_name='person who gathered this source record'
    )
    subject_date_start = models.DateField('beginning of source date range')
    subject_date_end = models.DateField('ending of source date range')
    comment = models.TextField('comments about the source', blank=True)
    source_group = models.ManyToManyField(
        'SourceGroup',
        verbose_name='groups or categories this source belongs to',
        blank=True
    )
    repositories = models.ManyToManyField(
        'Repository',
        through='RepositorySource',
        verbose_name='repositories in which this source can be found',
        blank=True
    )


class Repository(models.Model):

    """ A repository of sources.

    Contains information about the place where data is found.  While
    this typically would be information about a library or archives, it
    can also be information about a private citizen who holds
    genealogical material of interest, such as a diary, family bible,
    and so forth.  Data in this entity is sometimes part of a citation;
    it is required if the reader of the output of the data must know
    specifically where to find the data.

    The REPOSITORY entity contains data that identifies the repository
    such as name and address.  Note that a repository need not be a
    public library or archives; the entity can contain data about an
    individual who provided genealogical information.  Conceptually,
    this individual is the repository.

    Type: Independent.  Requires no other entities.

    Relationships:
        One REPOSITORY exists in one PLACE.
        One PLACE has zero to many REPOSITORYs.
        One REPOSITORY has zero to many SOURCEs (through
            REPOSITORY-SOURCE).
        One SOURCE is found in zero to many REPOSITORYs.  (The zero
            condition is when we have data about a SOURCE but do not
            know where it can be found.)

    Instance Variables:
        place -- (foreign key) Unique key that identifies the specific
            PLACE that this REPOSITORY is located.
        name -- The full name of the REPOSITORY.  If it is an individual
            instead of an institution, substitute the individual's data
            throughout.
        address -- The address of the REPOSITORY.
        phone -- The phone number of the REPOSITORY.
        hours -- The hours that the REPOSITORY is open to the public.
        comments -- Any pertinent comments about the repository, such as
            the need to obtain a researcher's card, restrictions on the
            use of laptops, etc.
    """

    place = models.ForeignKey(
        'Place',
        verbose_name='location of repository'
    )
    name = models.CharField('repository name', max_length=128)
    address = models.TextField('repository address', blank=True)
    phone = models.CharField(
        'repository phone number',
        max_length=64,
        blank=True
    )
    hours = models.TextField('repository hours', blank=True)
    comments = models.TextField('comments about the repository', blank=True)

    def __str__(self):
        """Stringify the repository.

        Arguments:
            self
        Returns: the name of the repository
        """
        return self.name

    class Meta:

        """Metadata for the model."""

        verbose_name_plural = "repositories"


class RepositorySource(models.Model):

    """ A connection of a repository and a source.

    An associative entity that ties together REPOSITORY and SOURCE in a
    many to many relationship.  Each instance in this entity represents
    a particular SOURCE in a specific REPOSITORY.

    Consider the relationship between REPOSITORY and SOURCE.  Clearly,
    one REPOSITORY has potentially many SOURCEs, meaning that if we go
    to the National Archives, an instance of REPOSITORY, we will
    potentially find many census records, instances of SOURCE.  On the
    other hand, a particular SOURCE (e.g., a microfilm reel with the
    Prince George's County, MD 1870 federal census on it) will be found
    in one to many REPOSITORYs.  It must be in at least one repository,
    but it may be in more.

    An exception occurs, however, when the researcher is aware of a
    particular SOURCE, but does not know where to find it.  Often this
    is a primary or secondary work mentioned in a secondary source; the
    existence is known, but not the physical whereabouts.  Consequently,
    the model indicates that one SOURCE is found in zero to many
    REPOSITORYs and not one to many REPOSITORYs as might otherwise be
    supposed.

    SOURCE-REPOSITORY is a convenient place to hold the call number for
    a SOURCE because the call number for the same source may be
    different at different REPOSITORYs.

    The notation 'At least one' indicates that every instance of
    REPOSITORY-SOURCE must be connected to at least SOURCE or REPOSITORY
    or both.  In a normal SEARCH it will be connected to both.

    Type: Dependent.  Requires SEARCH, REPOSITORY, and SOURCE.

    Relationships:
        One REPOSITORY-SOURCE describes either one SOURCE or one
            REPOSITORY or one of each.
        One SEARCH is conducted in zero to one REPOSITORYs (through
            REPOSITORY-SOURCE).
        One REPOSITORY is the scene of zero to many SEARCHs (through
            REPOSITORY-SOURCE).
        One SEARCH is conducted in zero to one SOURCEs (through
            REPOSITORY-SOURCE).
        One SOURCE provides data for zero to many SEARCHs (through
            REPOSITORY-SOURCE).
        One SOURCE is found in zero to many REPOSITORYs (through
            REPOSITORY-SOURCE).
        One REPOSITORY has zero to many SOURCEs (through
            REPOSITORY-SOURCE) that can be searched.

    Instance Variables:
        repository -- (foreign key) Unique key that identifies a
            specific REPOSITORY.
        source -- (foreign key) Unique key that identifies a specific
            SOURCE.
        activity -- (foreign key) Unique key that identifies a specific
            SEARCH.
        call_number -- The unique call number for a particular SOURCE in
            a particular REPOSITORY.  Some REPOSITORYs use the same call
            number for the same SOURCE such as a federal censuses, but
            most materials have different call numbers.  In some cases,
            there are multiple copies of a SOURCE in a REPOSITORY, and
            the researcher may wish to record which copy was the object
            of the SEARCH, particularly if the copy was not in good
            condition, and thus if the researcher wishes to SEARCH
            another copy.
        description -- Any pertinent notes about the particular SOURCE
            in the REPOSITORY, such as notes describing the condition of
            the copy represented by the particular call number.
    """

    repository = models.ForeignKey(
        Repository,
        verbose_name='repository that holds source',
        blank=True
    )
    source = models.ForeignKey(
        Source,
        verbose_name='source in repository',
        blank=True
    )
    activity = models.ForeignKey(
        'Search',
        verbose_name='specific search done in this combination'
    )
    call_number = models.CharField(
        'call number for this particular sounce in this repository',
        max_length=64,
        blank=True
    )
    description = models.TextField(
        'notes about this source in this repository',
        blank=True
    )


class RepresentationType(models.Model):

    """Type of the evidence representation.

    Contains a list of the types of representations of evidence, such as
    text, a TIF bitmap, a GIF bitmap, a WAV file, or other forms.

    Type: Independent.

    Relationships:
        One REPRESENTATION-TYPE describes zero to many REPRESENTATIONs.
        One REPRESENTATION is of one REPRESENTATION-TYPE.

    Instance Variables:
        name -- The name of the REPRESENTATION-TYPE such as 'Text', 'PCX
            Bitmap', and so forth.
    """

    name = models.CharField('type of representation', max_length=64)

    def __str__(self):
        """Stringify the representation type.

        Arguments:
            self
        Returns: the name of the representation type
        """
        return self.name


class Representation(models.Model):

    """Exerpts of sources.

    Contains the representation of a SOURCE in a variety of multimedia
    formats as needed, including old fashioned text, plus it contains a
    pointer to a physical file if the representation cannot be stored
    within the data model.

    The actual content of the citation is stored in REPRESENTATION.
    This is where the excerpts from our New London example are stored.
    In addition, REPRESENTATION can hold multi-media content such as a
    voice recording or an electronic image.  The type of REPRESENTATION,
    such as 'Bitmapped Image' or perhaps 'TIF File' in a different
    scheme, is referenced in REPRESENTATION-TYPE.

    Type: Dependent.  Requires SOURCE and REPRESENTATION-TYPE.

    Relationships:
        One REPRESENTATION is a manifestation of one SOURCE.
        One SOURCE has zero to many REPRESENTATIONs.  The zero condition
            is useful for a SOURCE in which the researcher found
            nothing.  The SEARCH in the SOURCE was significant and was
            recorded, but there is no REPRESENTATION, i.e., no
            photocopy, no text extract, no photo.
        One REPRESENTATION is of one REPRESENTATION-TYPE.
        One REPRESENTATION-TYPE is manifested in zero to many
            REPRESENTATIONs.

    Instance Variables:
        source -- (foreign key) Unique key that identifies the specific
            SOURCE.
        representation_type -- (foreign key) Unique key that identifies
            the type of representation, such as text, TIF bitmap, or
            other type.
        physical_file_code -- If the REPRESENTATION is external to the
            data model, such as a stored photograph that is not scanned
            into a computer system, this code tells the researcher where
            the REPRESENTATION is physically filed or stored.
        medium -- Often the SOURCE medium is paper, but it can be
            electronic, stone in the case of a tombstone, or other
            exotic media.
        content -- The actual content of the REPRESENTATION.  This can
            be text in the case of an abstract, extract, or
            transcription, or it can be other REPRESENTATIONs that can
            be stored within the confines of the actual implementation
            of the logical data model such as a bitmap that is stored in
            a computer application, or a sound file.  If the content
            cannot be stored in the model, this is empty.  An example
            would be a physical artifact like a souvenir glass from the
            World's Fair with the bride and groom's name and the
            marriage date; clearly we cannot store this electronically,
            but we could store a photograph of it electronically.
        comments -- Any comments that are required to describe this
            REPRESENTATION.
    """

    source = models.ForeignKey(
        Source,
        verbose_name='source that this represents'
    )
    representation_type = models.ForeignKey(
        RepresentationType,
        verbose_name='type of document this representation is'
    )
    physical_file_code = models.CharField(
        'location of the physical representation',
        max_length=256,
        blank=True
    )
    medium = models.CharField('representation medium', max_length=64)
    content = models.FileField('contents of the representation'),
    comments = models.TextField(
        'comments describing the representation',
        blank=True
    )


class CitationPartType(models.Model):

    """Names of the parts of a citation.

    Contains a list of citation parts, the names of the pieces of data
    found in citations of all types, such as author, editor, title, and
    place of publication.  Note that this entity does not contain the
    actual citation values such as 'Baltimore'.

    Type: Independent.  Data about CITATION-PART-TYPE can be entered
        without regard to any other entity.

    Relationships:
        One CITATION-PART-TYPE can be found in zero to many
            CITATION-PARTs.
        One CITATION-PART belongs to one and only one
            CITATION-PART-TYPE.

    Instance Variables:
        name -- The actual name of the citation part, such as author,
            compiler, editor, transcriber, or place of publication.
            There are more than a hundred different citation parts.
    """

    name = models.CharField('citation party name', max_length=64)

    def __str__(self):
        """Stringify the citation party type.

        Arguments:
            self
        Returns: the name of the citation part type
        """
        return self.name


class CitationPart(models.Model):

    """Part of a source citation.

    Provides a place to store the actual citation part for a particular
    SOURCE, such as author, title, and publication place  (in
    Citation-Part-Value).  There are a large number of
    CITATION-PART-TYPEs since there are a large number of types of
    genealogical records.

    The citation associated with each level of SOURCE is stored in
    CITATION-PART.  For example, Citation-Part-Value holds 'New London,
    CT Probate Records' as the top level CITATION-PART.  The type of
    citation that this information represents is stored in
    CITATION-PART-TYPE; in this example it might be 'Probate
    Jurisdiction'.

    Type: Dependent.  Requires CITATION-PART-TYPE and SOURCE.

    Relationships:
        One CITATION-PART-TYPE appears in zero to many CITATION-PARTs,
            e.g., there are a lot of citations for different authors.
        One CITATION-PART is of one and only one CITATION-PART-TYPE.
        One SOURCE can have zero to many CITATION-PARTs, e.g., a
            particular SOURCE might have an author, an editor, a
            compiler, a translator, a place of publication, and many
            other citation parts.
        One CITATION-PART refers to only one SOURCE.  For example,
            'Baltimore' refers to the place of publication for a single
            SOURCE; if another SOURCE was also published in Baltimore,
            there would be another instance in CITATION-PART.

    Instance Variables:
        source -- (foreign key) The unique key in SOURCE for which this
            is a citation part.
        citation_part_type -- (foreign key) The unique key in
            CITATION-PART-TYPE that identifies the type of citation part
            that this is, such as 'Publication City', 'Author', or
            'Title'.  Note that this is merely the ID and not the actual
            words.
        value -- The actual value of this citation part,
            such as 'Baltimore', 'Thomas Smith', or 'Wills of Prince
            George's County, Maryland 1695-1710'
    """

    source = models.ForeignKey(
        Source,
        verbose_name='source that this citation part refers to'
    )
    citation_part_type = models.ForeignKey(
        CitationPartType,
        verbose_name='type that corresponds to this citation part'
    )
    value = models.CharField('citation part value', max_length=256)

    def __str__(self):
        """Stringify the citation party type.

        Arguments:
            self
        Returns: the value of the citation part type
        """
        return self.value
