from .base import env

ENV_TYPE = env("ENV_TYPE")

if ENV_TYPE == 'PRODUCTION':
    from .production import *
else:
    from .development import *