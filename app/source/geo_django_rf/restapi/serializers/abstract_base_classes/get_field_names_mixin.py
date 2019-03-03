from rest_framework import serializers


class GetFieldNamesMixin:
    def get_field_names(self, declared_fields, info):
        assert isinstance(self, serializers.Serializer), \
            'To use GetFieldNameMixin, {} also has to inherit from ' \
            'rest_framework.serializers.Serializer'.format(type(self))

        expanded_fields = super(GetFieldNamesMixin, self).get_field_names(declared_fields, info)

        # Note that the excluded_fields are processed before the extra_fields are added
        if getattr(self.Meta, 'excluded_fields', None):
            expanded_fields = tuple(f for f in expanded_fields if f not in self.Meta.excluded_fields)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
