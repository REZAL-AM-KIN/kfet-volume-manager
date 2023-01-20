from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
DEBUG = environ.get('DEBUG')

# Setup LDAP Configuration Variables. Change these to your own settings.
# All configuration directives can be found in the documentation.

# Hostname of your LDAP Server
LDAP_HOST = environ.get('LDAP_HOST')

# Base DN of your directory
LDAP_BASE_DN = environ.get('LDAP_BASE_DN')

# Users DN to be prepended to the Base DN
LDAP_USER_DN = environ.get('LDAP_USER_DN')

# Groups DN to be prepended to the Base DN
LDAP_GROUP_DN = environ.get('LDAP_GROUP_DN')

# The RDN attribute for your user schema on LDAP
LDAP_USER_RDN_ATTR = environ.get('SECRET_KEY')

# The Attribute you want users to authenticate to LDAP with.
LDAP_USER_LOGIN_ATTR = environ.get('LDAP_USER_LOGIN_ATTR')

# The Username to bind to LDAP with
LDAP_BIND_USER_DN = environ.get('LDAP_BIND_USER_DN')

# The Password to bind to LDAP with
LDAP_BIND_USER_PASSWORD = environ.get('LDAP_BIND_USER_PASSWORD')

LDAP_GROUP_OBJECT_FILTER = environ.get('LDAP_GROUP_OBJECT_FILTER')
