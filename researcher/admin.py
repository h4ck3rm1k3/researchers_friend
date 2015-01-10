"""Display the model editing dashboard."""
from django.contrib import admin
from researcher import models


class ResearcherAdminSite(admin.AdminSite):

    """ Custom Admin Site."""

    site_header = 'Researcher\'s Friend'
    site_title = 'Site Admin | Researcher\'s Friend'
    index_title = 'Administration'

ADMIN_SITE = ResearcherAdminSite(name='admin')


# Administrative


class ResearcherProjectInline(admin.TabularInline):

    """ Inline ResearcherProject for Researcher/Project Admin."""

    model = models.ResearcherProject
    extra = 0


class ResearcherAdmin(admin.ModelAdmin):

    """ Custom Researcher Admin."""

    inlines = [ResearcherProjectInline]


class ProjectAdmin(admin.ModelAdmin):

    """ Custom Project Admin."""

    inlines = [ResearcherProjectInline]


class SuretySchemePartInline(admin.TabularInline):

    """ Inline SuretySchemePart for SuretyScheme Admin."""

    model = models.SuretySchemePart
    extra = 1


class SuretySchemeAdmin(admin.ModelAdmin):

    """ Custom Surety Scheme Admin."""

    inlines = [SuretySchemePartInline]


class ResearchObjectiveAdmin(admin.ModelAdmin):

    """ Custom Research Objective Admin."""

    filter_horizontal = ['activities']

ADMIN_SITE.register(models.Researcher, ResearcherAdmin)
ADMIN_SITE.register(models.Project, ProjectAdmin)
ADMIN_SITE.register(models.SuretyScheme, SuretySchemeAdmin)
ADMIN_SITE.register(models.AdministrativeTask)
ADMIN_SITE.register(models.Search)
ADMIN_SITE.register(models.ResearchObjective, ResearchObjectiveAdmin)
ADMIN_SITE.register(models.SourceGroup)

# Evidence


class RepositorySourceInline(admin.TabularInline):

    """ Inline RepositorySource for Repository/Source Admin."""

    model = models.RepositorySource
    extra = 0


class RepositoryAdmin(admin.ModelAdmin):

    """ Custom Repository Admin."""

    inlines = [RepositorySourceInline]


class CitationPartInline(admin.TabularInline):

    """ Inline CitationPart for Source Admin."""

    model = models.CitationPart
    extra = 0


class SourceAdmin(admin.ModelAdmin):

    """ Custom Source Admin."""

    inlines = [RepositorySourceInline, CitationPartInline]

ADMIN_SITE.register(models.Source, SourceAdmin)
ADMIN_SITE.register(models.Repository, RepositoryAdmin)
ADMIN_SITE.register(models.Representation)
ADMIN_SITE.register(models.RepresentationType)
ADMIN_SITE.register(models.CitationPartType)

# Conclusions


class AssertionAssertionInline(admin.TabularInline):

    """ Inline AssertionAssertion for Assertion Admin."""

    model = models.AssertionAssertion
    fk_name = 'assertion_high'
    extra = 0


class AssertionAdmin(admin.ModelAdmin):

    """ Custom Assertion Admin."""

    inlines = [AssertionAssertionInline]


class CharacteristicPartInline(admin.TabularInline):

    """ Inline CharacteristicPart for Characteristic Admin."""

    model = models.CharacteristicPart
    extra = 0


class CharacteristicAdmin(admin.ModelAdmin):

    """ Custom Characteristic Admin."""

    inlines = [CharacteristicPartInline]


class EventTypeRoleInline(admin.TabularInline):

    """ Inline EventTypeRole for EventType Admin."""

    model = models.EventTypeRole
    extra = 0


class EventTypeAdmin(admin.ModelAdmin):

    """ Custom EventType Admin."""

    inlines = [EventTypeRoleInline]


class GroupTypeRoleInline(admin.TabularInline):

    """ Inline GroupTypeRole for GroupType Admin."""

    model = models.GroupTypeRole
    extra = 0


class GroupTypeAdmin(admin.ModelAdmin):

    """ Custom GroupType Admin."""

    inlines = [GroupTypeRoleInline]


class PlacePartInline(admin.TabularInline):

    """ Inline PlacePart for Place Admin."""

    model = models.PlacePart
    extra = 0


class PlaceAdmin(admin.ModelAdmin):

    """ Custom Place Admin."""

    inlines = [PlacePartInline]

ADMIN_SITE.register(models.Assertion, AssertionAdmin)
ADMIN_SITE.register(models.Characteristic, CharacteristicAdmin)
ADMIN_SITE.register(models.CharacteristicPartType)
ADMIN_SITE.register(models.Event)
ADMIN_SITE.register(models.EventType, EventTypeAdmin)
ADMIN_SITE.register(models.Group)
ADMIN_SITE.register(models.GroupType, GroupTypeAdmin)
ADMIN_SITE.register(models.Persona)
ADMIN_SITE.register(models.Place, PlaceAdmin)
ADMIN_SITE.register(models.PlacePartType)
