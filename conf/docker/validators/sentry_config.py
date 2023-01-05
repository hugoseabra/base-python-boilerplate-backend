import logging
import sys

from decouple import config

logger = logging.getLogger()

SENTRY_PRIVATE_DSN = config('SENTRY_PRIVATE_DSN')

if not SENTRY_PRIVATE_DSN:
    logger.error("SENTRY_PRIVATE_DSN not provided or misconfigured.")
    sys.exit(1)

logger.debug(f'SENTRY Private DSN configured {SENTRY_PRIVATE_DSN[5]}***')
