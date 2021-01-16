import os

URL = os.environ.get('URL')
API_KEY = os.environ.get('API_KEY')
FROM = "Mailgun Sandbox <postmaster@<>.mailgun.org>"
ALERT_TIMEOUT = 1
COLLECTION = "alerts"