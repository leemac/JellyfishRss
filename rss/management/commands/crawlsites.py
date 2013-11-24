from django.core.management.base import BaseCommand
import feedparser
from rss.models import Subscription
from rss.models import User
# This is used for loading local RSS files for testing
class Command(BaseCommand):

	def handle(self, *args, **options):
		filepath = "rss/dummyfiles/google.xml"

		try:
			with open(filepath):
				d = feedparser.parse(filepath)

				user = User.objects.all()[0];

				for item in d.entries:

					existingItem = Subscription.objects.filter(user_id=user.id).filter(url=item.link).count()

					if(existingItem != 0):
						continue

					self.stdout.write("Found item: "  + item.title + "\n")


					object = Subscription()
					object.title=item.title
					object.url=item.link
					object.user_id = user.id
					object.save()

				
		except IOError:
			self.stdout.write("The file does not exist!")
			return

		
