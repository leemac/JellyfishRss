from __future__ import absolute_import

from celery import task
from celery.utils.log import get_task_logger

from datetime import datetime
from time import mktime

from urlparse import urlparse

from rss.models import Subscription
from rss.models import SubscriptionItem
from rss.models import User

import lxml.html as lh
import urllib2
import feedparser

logger = get_task_logger(__name__)

@task(name='rss.tasks.poll')
def poll():
	logger.info("Crawling sites!")
