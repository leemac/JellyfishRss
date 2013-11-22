
from django.contrib.auth.models import Subscription

sites = [
			"http://rss.cnn.com/rss/cnn_topstories.rss"
		]

for site in sites:
	existingItem = obj = Person.objects.get(first_name='John', last_name='Lennon')
	print(site)