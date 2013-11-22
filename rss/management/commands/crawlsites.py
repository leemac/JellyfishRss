from django.core.management.base import BaseCommand
import feedparser

# This is used for loading local RSS files for testing
class Command(BaseCommand):

	def handle(self, *args, **options):
		filepath = "rss/dummyfiles/google.xml"

		try:
			with open(filepath):
				d = feedparser.parse(filepath)

				for item in d.entries:
					self.stdout.write("+ " + item.title)

		except IOError:
			self.stdout.write("The file does not exist!")
			return

		
