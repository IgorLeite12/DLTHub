"""Salesforce source settings and constants"""

import os

# set to false to limit query to 100 records for testing
IS_PRODUCTION = os.getenv("IS_PRODUCTION", "true").lower() in {"1", "true", "yes", "y"}
