from brainiak.utils.i18n import _
from jsonschema import validate, ValidationError

from tornado.web import HTTPError


def validate_json_schema(request_json, schema):
    try:
        validate(request_json, schema)
    except ValidationError as ex:
        raise HTTPError(400, log_message=_(u"JSON not according to JSON schema definition.\n {0:s}").format(ex))
