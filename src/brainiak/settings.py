import logging
import os

DEBUG = False
ENVIRONMENT = 'dev'

SPARQL_ENDPOINT = 'http://dev.virtuoso.globoi.com:8890/sparql-auth'
SPARQL_ENDPOINT_USER = os.environ['GLB_API_SEMANTICA_VIRTUOSO_USR']
SPARQL_ENDPOINT_PASSWORD = os.environ['GLB_API_SEMANTICA_VIRTUOSO_PWD']
SPARQL_ENDPOINT_AUTH_MODE = "digest"
SPARQL_ENDPOINT_REALM = "SPARQL"

DEFAULT_LANG = "pt"

LOG_FILEPATH = "/opt/logs/brainiak/gunicorn-be/gunicorn-be.log"
LOG_LEVEL = logging.DEBUG
LOG_NAME = "brainiak"

URI_PREFIX = "http://semantica.globo.com/"
