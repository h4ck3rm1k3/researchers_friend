"""Create the researcher conclusions data models.

Exports:
    Classes:
        Assertion
        AssertionAssertion
        Characteristic
        CharacteristicPart
        CharacteristicPartType
        Event
        EventType
        EventTypeRole
        Group
        GroupType
        GroupTypeRole
        Persona
        Place
        PlacePart
        PlacePartType
"""
from django.db import models


# Conclusions Models
ASSERTION_SUBJECT_TYPES = (
    ('P', 'Persona'),
    ('E', 'Event'),
    ('C', 'Characteristic'),
    ('G', 'Group'),
)

SORT_ORDER_CHOICES = (
    ('A', 'Ascending'),
    ('D', 'Descending'),
    ('N', 'None')
)


class Assertion(models.Model):

    """A conclusion made based on data.

    Contains the lowest level raw conclusional data in a special atomic
    form.  This involves an interpretation by the researcher ranging
    from trivial to complex.  This entity also contains higher level
    conclusional data from lower level assertions, so that all
    assertions can be tracked through layers of reasoning back to their
    original evidential statement forms.  Assertions should not be
    deleted, but an attribute (Disproved) exists to nullify erroneous
    conclusions so that the erroneous reasoning can be preserved and
    marked as believed to be no longer valid.  Everyone's work has
    value, even if it is later proved to be wrong.  Since all assertions
    are tagged according to their origin, it is possible to store
    other's assertions as well and identify that data as such.  While
    most assertions are tied to particular SOURCE excerpts (the Content
    attribute in REPRESENTATION) or previous assertions, an assertion
    can apply to an entire SOURCE.

    Type: Dependent.  Requires numerous other entities including
        RESEARCHER, the GROUP entities,  PERSONA, the EVENT entities,
        CHARACTERISTIC, and SURETY.

    Relationships:
        Each ASSERTION has data about zero to one PLACE.
        Each ASSERTION was written by one RESEARCHER.
        Each ASSSERTION is about two subjects, and each subject is one
            of the following:  PERSONA, EVENT, CHARACTERISTIC, or GROUP.
        Some ASSERTIONs are related to either GROUP-TYPE-ROLE or
            EVENT-TYPE-ROLE (through the Value attribute).
        Each ASSERTION depends on zero to one SURETY-SCHEME-PARTs.
        Each ASSERTION is the direct output of no more than one SOURCE.
            Some ASSERTIONs are not the direct output of any SOURCE, but
            are the output of one to many other ASSERTIONs (through
            ASSERTION-ASSERTION); note that many lower level ASSERTIONs
            are coupled to one higher level ASSERTION by pairing one at
            a time through ASSERTION-ASSERTION.

    Instance Variables:
        surety_scheme_part -- (foreign key) A pointer that indicates how
            sure the researcher is of this particular assertion.
        researcher -- (foreign key) A pointer that identifies the
            researcher who made this assertion.  The person asserting
            can be the researcher, or a compiler from which the
            researcher obtained data.  In group projects, there may be
            many researchers.
        source -- (foreign key) A pointer to the source that gave rise
            to this assertion, if the assertion is the result of a
            direct source and not another assertion.
        subject1_type -- Can be either PERSONA, EVENT, CHARACTERISTIC,
            or GROUP.
        subject1 -- A pointer to the appropriate PERSONA, EVENT,
            CHARACTERISTIC, or GROUP attribute of ID.
        subject2_type -- Can be either PERSONA, EVENT, CHARACTERISTIC,
            or GROUP.
        subject2 -- A pointer to the appropriate PERSONA, EVENT,
            CHARACTERISTIC, or GROUP attribute of ID.
        value_role -- If the statement is of the appropriate type, the
            value of the object in the statement.  Example:  (hair
            color) red; (occupation) teamster; (sex) female.  In some
            instances, value can be thought of as "Role" such as "Groom"
            or "Witness".
        rationale -- Narrative that explains the researcher's basis for
            the assertion.  This can be curt for simple or trivial
            assertions, or very extensive if necessary for more complex
            assertions created from a variety of conflicting sources.
        disproved -- A yes/no indicator that the genealogist no longer
            believes the assertion to be true.  "Yes" or "true" means it
            is no longer true.
    """

    surety_scheme_part = models.ForeignKey(
        'SuretySchemePart',
        verbose_name='assertion surety',
        blank=True
    )
    researcher = models.ForeignKey(
        'Researcher',
        verbose_name='researcher who made assertion'
    )
    source = models.ForeignKey(
        'Source',
        verbose_name='source that prompted assertion',
        blank=True
    )
    subject1_type = models.CharField(
        'type of first assertion subject',
        max_length=1,
        choices=ASSERTION_SUBJECT_TYPES
    ),
    subject1 = models.IntegerField('id of subject 1'),
    subject2_type = models.CharField(
        'type of second assertion subject',
        max_length=1,
        choices=ASSERTION_SUBJECT_TYPES
    ),
    subject2 = models.IntegerField('id of subject 2'),
    value_role = models.CharField(
        'value of object in the assertion',
        max_length=64,
        blank=True
    ),
    rationale = models.TextField('basis for the assertion')
    disproved = models.BooleanField(default=False)


class AssertionAssertion(models.Model):

    """Facilitates a many-to-many relationship between assertions.

    An associative entity that links ASSERTION to itself so that
    multiple prior ASSERTIONs be brought together into a new ASSERTION.
    As an example, four ASSERTIONs based on individual SOURCEs can be
    brought together to resolve or document discrepancies about the date
    of a person's birth.

    Type: Dependent.  Requires ASSERTION  twice (where it feeds multiple
        ASSERTIONs into a new ASSERTION).

    Relationships:
        An ASSERTION-ASSERTION has one input ASSERTION.
        An ASSERTION-ASSERTION has one output ASSERTION.

    Instance Variables:
        assertion_low -- (foreign key) The unique key in ASSERTION for
            which this instance (i.e., a physical record in a table)
            serves as the input.
        assertion_high -- (foreign key) The unique key in ASSERTION for
            which this instance (i.e., a physical record in a table)
            serves as the output.
        sequence_number -- A value that keeps a series of input and
            output ASSERTIONs in order, so that for example, 4 lower
            level ASSSERTIONs can be brought together into a higher
            level ASSERTION with the order of the low level ASSERTIONs
            preserved.
    """

    assertion_low = models.ForeignKey(
        Assertion,
        verbose_name='input assertion',
        related_name='+'
    )
    assertion_high = models.ForeignKey(
        Assertion,
        verbose_name='output assertion',
        related_name='+'
    )
    sequence_number = models.PositiveSmallIntegerField(
        'order of low level of assertion',
        default=0
    )


class Persona(models.Model):

    """A representation of an individual person.

    Contains the core identification for each individual in genealogical
    data, and allows information about similarly named or identically
    named people to be brought together, after suitable analysis, in the
    same aggregate individual.  Because real human beings leave data
    tracks through time as if they were disparate shadow personas, this
    entity allows the genealogical researcher to tie together data from
    different personas that he or she believes belong to the same real
    person.  The mechanism for this, discussed in the text, is to make
    different PERSONAs part of the same GROUP.

    Type: Dependent.  Requires ASSERTIONs to support the data.

    Relationships:
        One PERSONA is based on one ASSERTION.  However, note that an
            ASSERTION may link one PERSONA to a GROUP, and thus many
            separate PERSONAs can be brought together into a higher
            level constructed PERSONA.
        One ASSERTION can describe zero or one PERSONAs.

    Instance Variables:
        name -- The entire name that this PERSONA is known by.  This can
            be a special instance from a single record (from SOURCE and
            REPRESENTATION) like "John Q. Smith", or it can be a
            composite name built up from many separate instances, such
            as "John Quincy (Butch) Smith", that never actually appear
            in any record, but which reflects the name the way the
            RESEARCHER wishes to tag the individual.
        description_comments -- Any narrative necessary to distinguish
            this person.
    """

    name = models.CharField('name of the person', max_length=256)
    description_comments = models.TextField('about this person')

    def __str__(self):
        """Stringify the persona.

        Arguments:
            self
        Returns: the name of the persona
        """
        return self.name


class Event(models.Model):

    """A happening.

    An EVENT is any type of happening such as a particular wedding.

    Type: Dependent.  Requires EVENT-TYPE.

    Relationships:
        One EVENT is of an EVENT-TYPE.
        One EVENT-TYPE is manifested in zero to many EVENTs.
        One EVENT is the subject of one ASSERTION.
        One ASSERTION describes zero to two EVENTs.
        One EVENT happens in one PLACE.
        One PLACE can have zero to many EVENTs.

    Instance Variables:
        event_type -- (foreign key) Unique identifier that indicates to
            which EVENT-TYPE this event belongs.
        place -- (foreign key) Unique identifier in PLACE that indicates
            the place associated with this EVENT.   In short, where did
            this EVENT take place?
        name -- The name of the event, such as "Marriage of John Smith
            and Mary Jones".
        date_start -- The date associated with the start of the event.
        date_end -- The date associated with the end of the event.
    """

    event_type = models.ForeignKey(
        'EventType',
        verbose_name='type of the event'
    )
    place = models.ForeignKey(
        'Place',
        verbose_name='where this event took place'
    )
    name = models.CharField('event name', max_length=256)
    date_start = models.DateField('event start date')
    date_end = models.DateField('event end date')

    def __str__(self):
        """Stringify the event.

        Arguments:
            self
        Returns: the name of the event
        """
        return self.name


class EventType(models.Model):

    """A kind of an event.

    Because many events (e.g., marriages) have quite similar structures,
    it's more efficient to define a type of event in a template
    structure than to keep defining individual events that are the same.
    The EVENT-TYPE contains the name of a standard event while the
    details about the usual roles played in such an event appear as
    individual instances of EVENT-TYPE-ROLE.

    Type: Independent.  Does not require any other entities.

    Relationships:
        One EVENT-TYPE is manifested as zero to many EVENTs.
        One EVENT is of one and only one EVENT-TYPE.
        One EVENT-TYPE has one to many EVENT-TYPE-ROLEs.
        One EVENT-TYPE-ROLE belongs to one and only one EVENT-TYPE.

    Instance Variables:
        name -- The name of this event type.  An example might be
            "Marriage" or "Wedding", or "Battle".
    """

    name = models.CharField('event type name', max_length=64)

    def __str__(self):
        """Stringify the event type.

        Arguments:
            self
        Returns: the name of the event type
        """
        return self.name


class EventTypeRole(models.Model):

    """Roles related to a particular event type.

    The individual roles of a defined event type, such as "Chaplain" for
    a role in a military unit.

    Type: Dependent.  Requires EVENT-TYPE.

    Relationships:
        Each EVENT-TYPE-ROLE belongs to only one EVENT TYPE.
        An EVENT-TYPE can have zero to many EVENT-TYPE-ROLEs.  The zero
            condition is for unity, where there is only one event type
            role in the event type, meaning everyone in the event
            participated in the same capacity, such as "Witness".
        An EVENT-TYPE-ROLE can appear in zero to many ASSERTIONs in the
            Value attribute.
        One ASSERTION is about zero or one EVENT-TYPE-ROLEs.

    Instance Variables:
        event_type -- (foreign key) Unique key that identifies the
            EVENT-TYPE to which these members belong.
        name -- The value that distinguishes the different members of
            the event type, such as role (bride, groom, witness).
    """

    event_type = models.ForeignKey(
        EventType,
        verbose_name='type of event this role belongs to'
    )
    name = models.CharField('role name', max_length=64)

    def __str__(self):
        """Stringify the event type role.

        Arguments:
            self
        Returns: the name of the event type role
        """
        return self.name


class Characteristic(models.Model):

    """Data about a person.

    A CHARACTERISTIC is any data that distinguishes one person from
    another, such as an occupation, hair color, religion, name, and so
    forth.  Most CHARACTERISTIC data consists of a single part value,
    but some data can be more complex and require the sequencing of many
    parts such as a person's name.

    Type: Dependent.  Requires ASSERTION and CHARACTERISTIC-PART.

    Relationships:
        One CHARACTERISTIC has one to many CHARACTERISTIC-PARTs.
        One CHARACTERISTIC-PART is part of only one CHARACTERISTIC.
        One CHARACTERISTIC is the subject of one ASSERTION.
        One ASSERTION describes zero to two CHARACTERISTICs.
        One CHARACTERISTIC happens in one PLACE.
        One PLACE can be the location of zero to many CHARACTERISTICs.

    Instance Variables:
        place -- (foreign key) Unique identifier in PLACE that indicates
            the place associated with this CHARACTERISTIC.  Note that
            this is not a characteristic of a place (such as "nice view
            of the mountains"), but a place where a characteristic was
            noted, e.g., "Tuscon" is the place where John Smith was
            employed as a stagecoach driver, a type of occupation and
            thus a characteristic of John Smith.
        date_start -- The date associated with the start of the
            characteristic.
        date_end -- The date associated with the end of the
            characteristic.
        sort_order -- The sorting order of the attached
            CHARACTERISTIC-PARTs (Ascending, Descending, None)
    """

    place = models.ForeignKey(
        'Place',
        verbose_name='place where characteristic was noted'
    )
    date_start = models.DateField('characteristic start date')
    date_end = models.DateField('characteristic end date')
    sort_order = models.CharField(
        'how to sort characteristics',
        max_length=1,
        choices=SORT_ORDER_CHOICES
    )


class CharacteristicPart(models.Model):

    """Discrete elements of a characteristic.

    Most CHARACTERISTICs have a single CHARACTERISTIC-PART.  For
    example, the characteristic "Occupation" typically has a single
    value.  But since the data model defines a person's name as another
    characteristic, and since name is made up of parts such as given
    name, surname, suffix, and so forth, this entity is required to
    collect the parts of a CHARACTERISTIC.

    Type: Dependent.  Requires CHARACTERISTIC and CHARACTERISTIC-PART-TYPE.

    Relationships:
        One CHARACTERISTIC-PART is part of one CHARACTERISTIC.
        One CHARACTERISTIC has one to many CHARACTERISTIC-PARTs.
        One CHARACTERISTIC-PART is of one CHARACTERISTIC-PART-TYPE.
        One CHARACTERISTIC-PART-TYPE is seen in zero to many
            CHARACTERISTIC-PARTs.  For example, the
            Characteristic-Part-Type-Name "Mononame" (in
            CHARACTERISTIC-PART-TYPE) is seen in the
            Characteristic-Part-Name "Sitting Bull", "Geronimo", and
            "Blue Duck" (in CHARACTERISTIC-PART).

    Instance Variables:
        characteristic -- (foreign key) Unique key that identifies the
            characteristic.
        characteristic_part_type -- (foreign key) Unique key that
            identifies a specific characteristic part type.
        name -- The actual name of the characteristic part, such as
            "Stagecoach driver", "Red", or "Mary.
        sequence_number -- The number that keeps the characteristic
            parts sorted in correct order.
    """

    characteristic = models.ForeignKey(
        Characteristic,
        verbose_name='characteristic this is a part of'
    )
    characteristic_part_type = models.ForeignKey(
        'CharacteristicPartType',
        verbose_name='type of characteristic part'
    )
    name = models.CharField('characteristic part name', max_length=64)
    sequence_number = models.PositiveSmallIntegerField(
        'order of characteristic part',
        default=0
    )

    def __str__(self):
        """Stringify the characteristic part.

        Arguments:
            self
        Returns: the name of the characteristic part
        """
        return self.name


class CharacteristicPartType(models.Model):

    """Types of discrete elements of a characteristic.

    In the case of most characteristics, this entity provides a list of
    the one and only part, such as "Occupation", "Hair Color", "Medical
    Condition", and so forth.  In the case of personal names, however,
    this entity provides a list of all the name parts such as "Given
    Name", "Surname", "Mononame", "Prefix", and so forth.

    Type: Independent.

    Relationships:
        One CHARACTERISTIC-PART-TYPE is manifested as zero to many
            CHARACTERISTIC-PARTs.
        One CHARACTERISTIC-PART is of exactly one
            CHARACTERISTIC-PART-TYPE.

    Instance Variables:
        name -- The actual name of the CHARACTERISTIC-PART-TYPE, such as
            "Mononame", "Nickname", or "Occupation".
    """

    name = models.CharField(
        'name of the type of the characteristic part',
        max_length=64
    )

    def __str__(self):
        """Stringify the characteristic part type.

        Arguments:
            self
        Returns: the name of the characteristic part type
        """
        return self.name


class Group(models.Model):

    """A category for otherwise uncategorizable people.

    In genealogical data, there are group members for which we can't
    identify query conditions to return the set.  In other words,
    membership in a group such as "men who worked on the Davison Road in
    August, 1851" may be important genealogically, but no other
    attributes will sufficiently code for this.  Thus, those members
    need to be tagged as explicit members of one or more groups.  Groups
    are also used in this data model for concepts such as a group of
    children for a union of a man and woman.

    Type: Dependent.  Requires GROUP-TYPE.

    Relationships:
        One GROUP is of a GROUP-TYPE.
        One GROUP-TYPE is manifested in zero to many GROUPs.
        One GROUP is the subject of one ASSERTION.
        One ASSERTION describes zero to two GROUPs.
        One GROUP was brought together in one PLACE.
        One PLACE can have zero to many GROUPs.

    Instance Variables:
        group_type -- (foreign key) Unique identifier that indicates to
            which GROUP-TYPE this group belongs.
        place -- (foreign key) Unique identifier in PLACE that indicates
            the place associated with this GROUP.  In the example of a
            group of neighbors, it would be the small area where they
            lived.  In the case of the Titanic passengers and crew, it
            might be the city that they sailed from, or it might be the
            location in the ocean of the disaster as appropriate to the
            researcher's genealogical needs.  Some groups may not be
            associated with a place.
        name -- The name of the group.
        date_start -- The date associated with the start of the group
        date_end -- The date associated with the end of the group
        criteria -- The criteria for admission to the group.  For
            example, one group might be all the neighbors listed in a
            particular document, while a second group is a similar group
            of neighbors listed in a second document, or the same
            document at a different time.
    """

    group_type = models.ForeignKey(
        'GroupType',
        verbose_name='group type'
    )
    place = models.ForeignKey(
        'Place',
        verbose_name='place associated with this group',
        blank=True
    )
    name = models.CharField('group name', max_length=128)
    date_start = models.DateField('group start date')
    date_end = models.DateField('group end date')
    criteria = models.TextField('criteria for admission to group')

    def __str__(self):
        """Stringify the group.

        Arguments:
            self
        Returns: the name of the group
        """
        return self.name


class GroupType(models.Model):

    """The generalized type of the group.

    Because many groups (e.g., military groups) have quite similar
    structures, it's more efficient to define a type of group in a
    template structure than to keep defining individual groups that are
    the same.  The GROUP-TYPE contains the name and the ordering
    characteristics of a standard group while the details about the
    standard group appear as individual instances of GROUP-TYPE-ROLE.

    Type: Independent.  Does not require any other entities.

    Relationships:
        One GROUP-TYPE is manifested as zero to many GROUPs.
        One GROUP is of one and only one GROUP-TYPE.
        One GROUP-TYPE has one to many GROUP-TYPE-ROLEs.
        One GROUP-TYPE-ROLE belongs to one and only one GROUP-TYPE.

    Instance Variables:
        name -- The name of this group type.  An example might be "U.S.
            Army grades and ranks, 1810-1830" (or whatever).  Another
            group might be "Neighbors Occupying Contiguous Property"
        sort_order -- What is the ordering scheme of this group?
            (Ascending, Descending, or None)
    """

    name = models.CharField('group type name', max_length=128)
    sort_order = models.CharField(
        'group type sort order',
        max_length=1,
        choices=SORT_ORDER_CHOICES,
        default='A'
    )

    def __str__(self):
        """Stringify the group type.

        Arguments:
            self
        Returns: the name of the group type
        """
        return self.name


class GroupTypeRole(models.Model):

    """Roles in a particular group type.

    The standard individual members of a defined group type, such as
    "Private, Corporal, Sergeant", "Bride, Groom, Witness", or "Miner,
    Pit Boss, Superintendent".

    Type: Dependent.  Requires GROUP-TYPE.

    Relationships:
        Each GROUP-TYPE-ROLE belongs to only one GROUP TYPE.
        A GROUP-TYPE can have zero to many GROUP-TYPE-ROLEs.  The zero
            condition is for unity, where there is only one group type
            role in the group type, meaning everyone in the group is of
            the same rank or type, such as a group of neighbors.
        A GROUP-TYPE-ROLE can appear in zero to many ASSERTIONs in the
            Value attribute.
        One ASSERTION is about zero or one GROUP-TYPE-ROLEs.

    Instance Variables:
        group_type -- (foreign key) Unique key that identifies the
            GROUP-TYPE to which these members belong.
        name -- The value that distinguishes the different members of
            the group type, such as role (bride, groom, witness) or rank
            (captain, major, colonel).
        sequence_number -- The alphanumeric sequence number that causes
            the highest ranked group type member to be sorted high.  For
            example, if the group consisted of (in this short example)
            "Colonel, General", Colonel might be assigned a sequence
            number of 2 and General a 1 to indicated that General ranks
            above Colonel.  In the case of roles, sequence number may be
            irrelevant and may only serve to order the list for
            presentation so that "bride, groom, minister, witness,
            flower girl, ring bearer" appear in that order and not
            alphabetically.
    """

    group_type = models.ForeignKey(
        GroupType,
        verbose_name='type of group this role pertains to'
    )
    name = models.CharField('role name', max_length=64)
    sequence_number = models.PositiveSmallIntegerField(
        'order in which this should appear in list of roles',
        default=0
    )

    def __str__(self):
        """Stringify the group type role.

        Arguments:
            self
        Returns: the name of the group type role
        """
        return self.name


class Place(models.Model):

    """A place entity.

    Contains the core information about a PLACE, but does not include
    the subparts that make up the hierarchical name of a PLACE.

    Type: Dependent.  Requires PLACE-PART-TYPE.

    Relationships:
        One PLACE has one to many PLACE-PARTs.
        One PLACE-PART belongs to one PLACE.
        PLACE also has numerous one to zero-to-many relationships with
            entities like ASSERTION, GROUP, EVENT, CHARACTERISTIC,
            RESEARCHER, and REPOSITORY.

    Instance Variables:
        existence_date_start -- A start date describing when this place
            was in existence.
        existence_date_end -- An end date describing when this place was
            in existence.
        sort_order -- Describes the order of the PLACE-PARTs (Ascending,
            Descending, or None)
    """

    existence_date_start = models.DateField(
        'date this place was founded',
        blank=True
    )
    existence_date_end = models.DateField(
        'date this place ceased to be',
        blank=True
    )
    sort_order = models.CharField(
        'sort direction',
        max_length=1,
        choices=SORT_ORDER_CHOICES,
        default='A'
    )

    def __str__(self):
        """Stringify the place part.

        Arguments:
            self
        Returns: the name of the place part
        """
        # pylint: disable=E1101
        orderby = 'sequence_number'

        if self.sort_order == 'D':
            orderby = '-' + orderby

        ordered_place_parts = self.placepart_set.order_by(orderby)

        return ", ".join([p.name for p in ordered_place_parts])


class PlacePart(models.Model):

    """A discrete part of the complete place entity.

    Contains information about a specific place, but in a way that the
    hierarchical relationship of that place to other places is
    preserved.  One instance of PLACE-PART might be Maryland, while
    another is Virginia.  Through association with PLACE-PART-TYPE we
    would know that both instances are called a "State".

    Note that a PLACE-PART like "Montgomery" is part of many different
    PLACEs.  It is a county in several different states, and it is also
    a city in Alabama.  But each of these Montgomerys would appear as a
    different instance in PLACE-PART and be attached to a different
    PLACE as would be expected.

    Type: Dependent.  Requires PLACE-PART-TYPE.

    Foreign Keys:
        Place-Part-Type-ID (in PLACE-PART-TYPE)
        Place-ID (in PLACE)

    Relationships:
        An example of one PLACE-PART-TYPE (such as "State") is found in
            zero to many actual PLACE-PARTs (such as "Colorado").
        One PLACE-PART is of one PLACE-PART-TYPE.
        One PLACE-PART appears in one PLACE.
        One PLACE is made up of one to many PLACE-PARTs.

    Instance Variables:
        place_part_type -- (foreign key) Unique key that identifies the
            type of place part that this is, e.g., "State" or "Country"
            or "County", etc.
        place -- (foreign key) Unique key that identifies the PLACE of
            which this is a part.
        name -- The actual name of this place part, such as "Prince
            George's".
        sequence_number -- The number that keeps the PLACE-PARTs in
            order, either ascending or descending (or in no order).
    """

    place_part_type = models.ForeignKey(
        'PlacePartType',
        verbose_name='place type'
    )
    place = models.ForeignKey(
        Place,
        verbose_name='place entity this part belongs to'
    )
    name = models.CharField('place name', max_length=128)
    sequence_number = models.PositiveSmallIntegerField(
        'sort order',
        default=0
    )

    def __str__(self):
        """Stringify the place part.

        Arguments:
            self
        Returns: the name of the place part
        """
        return self.name


class PlacePartType(models.Model):

    """The type of a discrete part of a place entity.

    Contains information about various schemes of organizing place data
    in a hierarchical or other fashion.  Parts might include "Country",
    "State", "Province", "County", and "City/Town/Village".

    Type: Independent.  Does not require any other entities.

    Relationships:
        One PLACE-PART-TYPE has zero to many PLACE-PARTs.

    Instance Variables
        name -- The name of this PLACE-PART-TYPE, such as "State",
            "County", "Country", "Ocean", or "Hospital".
    """

    name = models.CharField('place part type name', max_length=64)

    def __str__(self):
        """Stringify the place part type.

        Arguments:
            self
        Returns: the name of the place part type
        """
        return self.name
