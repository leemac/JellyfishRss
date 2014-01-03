from __future__ import absolute_import

from celery import task
from celery.utils.log import get_task_logger

from rss.polling import sitepoller

logger = get_task_logger(__name__)

@task(name='rss.tasks.poll')
def poll():
	poller = sitepoller.SitePoller()

	logger.info("Crawling sites! \n")

	poller.poll(logger)

	return
