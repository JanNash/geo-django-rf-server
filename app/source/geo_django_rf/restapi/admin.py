import copy
from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# This import is only needed for the ProfileInline-hack
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS

from .models import Profile


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ProfileInline(gisadmin.OSMGeoAdmin, admin.StackedInline):
    """
    Define an admin descriptor for Profile which is inlined in User
    """
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # This is a hack to make it possible to use OSMGeoAdmin in an admin.StackedInline #
    # I found the idea for it in this SO question:                                    #
    # https://stackoverflow.com/q/32037375/3406709 and updated it to Django 1.11      #
    # (only the BaseModelAdmin init changed compared to 1.9)                          #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # InlineModelAdmin.__init__() implementation as of Django 1.11        # #
    def __init__(self, parent_model, admin_site):
        self.admin_site = admin_site
        self.parent_model = parent_model
        self.opts = self.model._meta
        self.has_registered_model = admin_site.is_registered(self.model)
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # BaseModelAdmin.__init__() implementation as of Django 1.11  # #
        # #                                                             # #
        # # This replaces the super(InlineModelAdmin, self).__init__()  # #
        # # which is here in the original InlineModelAdmin.__init__()   # #

        # Merge FORMFIELD_FOR_DBFIELD_DEFAULTS with the formfield_overrides
        # rather than simply overwriting.
        overrides = copy.deepcopy(FORMFIELD_FOR_DBFIELD_DEFAULTS)
        for k, v in self.formfield_overrides.items():
            overrides.setdefault(k, {}).update(v)
        self.formfield_overrides = overrides

        # # End of BaseModelAdmin.__init__() implementation             # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        if self.verbose_name is None:
            self.verbose_name = self.model._meta.verbose_name
        if self.verbose_name_plural is None:
            self.verbose_name_plural = self.model._meta.verbose_name_plural
    # # End of InlineModelAdmin.__init__() implementation                   # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# Define a new User admin with the ProfileInline added to inlines
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


# Re-register UserAdmin
admin.site.register(get_user_model(), UserAdmin)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
