from django.core.management.base import BaseCommand

from rss.polling import sitepoller

import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):

	def handle(self, *args, **options):

		poller = sitepoller.SitePoller()

		logger.info("--Crawling sites! \n")

		poller.poll(logger)

		return