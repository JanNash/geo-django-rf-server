import json
from django.http import QueryDict
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.parsers import (
    MultiPartParser,
    DataAndFiles,
    ParseError
)


class MultiPartWithJSONParser(MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )

        try:
            data = result.data['data']
        except MultiValueDictKeyError:
            raise ParseError('Could not parse request, key "data" does not exist')

        qdict = QueryDict('', mutable=True)
        qdict.update(json.loads(data))

        return DataAndFiles(qdict, result.files)
