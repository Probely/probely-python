
import environ

env = environ.Env()

PROBELY_API_TOKEN = env("PROBELY_API_TOKEN")

PROBELY_API_URL_BASE = env("PROBELY_API_URL_BASE", default="https://api.qa.eu.probely.com/")

# URLs
PROBELY_API_TARGETS_URL = PROBELY_API_URL_BASE + "targets/"
