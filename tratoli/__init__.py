from __future__ import absolute_import, unicode_literals

# This will ensure the app is always imported when Django starts
# so that shared_task will use this app.
from .celery_config import app as app