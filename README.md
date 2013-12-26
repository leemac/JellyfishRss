JellyfishRss
============

Jellyfish Rss will be an RSS reader that is 100% open source and self-hostable. It will be optimized for mobile users.

###Install

- Clone Repository
- Install [django-pipeline](https://github.com/cyberdelia/django-pipeline)
- Install [feedparser](https://pypi.python.org/pypi/feedparser)
- Install [south](http://south.readthedocs.org/en/latest/installation.html)
- Install [Celery](http://www.celeryproject.org/install/)
- Install RabbitMQ (sudo apt-get install rabbitmq-server)
- manage.py syncdb
- manage.py migrate

### Running Server

First, bring up the web server:
- python manage.py runserver

Then, bring up Celery which will start polling at intervals of an hour:
- celery -A rss worker -B -l info

###Roadmap
1. Implement basic site pages
	- Home [Done]
	- Login [Done]
	- Feeds View [Done]
	- Settings
2. Implement RSS poller
	- Iterate over sites [Done]
	- Add new items [Done]
	- Add cron job (for now) [In Progress]
3. Authentication [Done]
4. User integration
	- Feeds polled at interval
	- User can login and view feeds [Done]
	- User can login and mark feeds as read [In Progress]
	- etc.
5. Work on UI

###Feature Idea Brain Dump

+ Mark as read for a particular user
+ Mark as favorite for a particular user
+ View the most recently updated entries with # count next to subscription name
+ View all subscriptions with all items (paging)
+ View favorite entries
+ Email/Share
+ Ignore posts with specific terms (Giveaway, Prizes). Choose your own or select pre-crafted filters.
+ Hostable 
+ Tagging
+ Subscription Colors
+ Real Time wall
+ "Apps" which let you connect to Reddit/HN/various sources. 
+ Import your data from Google Reader.
+ Easily export your data.
+ Mobile Friendly 

###License

Jellyfish Rss is licensed under the MIT license. A link back to this project is appreciated but not required.