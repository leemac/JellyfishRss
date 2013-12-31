JellyfishRss
============

Jellyfish Rss will be an RSS reader that is 100% open source and self-hostable. It will be optimized for mobile users.

###Install
The installation portion is a work-in-progress. I'll publish a proper requirements.txt from pip soon. Until then, it's manual.

- Install [Django-Pipeline](https://github.com/cyberdelia/django-pipeline)
```
pip install django-pipeline
```

- Install [FeedParser](https://pypi.python.org/pypi/feedparser)
``` 
pip install feedparser
```

- Install [South](http://south.readthedocs.org/en/latest/installation.html)
```
pip install south
```

- Install [Celery](http://www.celeryproject.org/install/)
``` 
pip install celery
```

- Install [RabbitMQ](http://www.rabbitmq.com/) 
```
sudo apt-get install rabbitmq-server
```
- Install [lxml](http://lxml.de/3.0/installation.html) 
```
sudo apt-get install libxml2 libxml2-dev libxslt-dev && pip install lxml
```

### Database Setup
```
manage.py syncdb
manage.py migrate
```

### Running Server
First, bring up the web server:
```
python manage.py runserver
```

Then, bring up Celery:
```
celery -A rss worker -B -l info
```

Polling is set to one hour (3600s) and can be configured in settings.py:
```
CELERYBEAT_SCHEDULE = {
    'poll-every-hour': {
        'task': 'rss.tasks.poll',
        'schedule': timedelta(seconds=3600)
    },
}
```

###Basic Roadmap
1. Implement basic site pages
	- Home [Done]
	- Login [Done]
	- Feeds View [Done]
	- Settings
2. Implement RSS poller
	- Iterate over sites [Done]
	- Add new items [Done]
	- Add Poller (Celery) [Done]
3. Authentication [Done]
4. User integration
	- User can login and view feeds [Done]
	- User can login and mark feeds as read [Done]
5. Work on UI
	- Download Favicons [In Progress]
	- Colors
	- Typography
	- Mobile/Responsive version
6. Other features
	- Search
	- Blacklist keywords
	- Import/Export

###Feature Idea Brain Dump
+ Feeds are shared. Polled once. Users actually subscribe to feeds to improve performance/scalability.
+ Management of favorite articles.
+ View the most recently updated entries with # count next to subscription name
+ View all subscriptions with all items (paging)
+ Infinite Scrolling
+ Email/Share
+ Ignore posts with specific terms (Giveaway, Prizes). Choose your own or select pre-crafted filters.
+ Tagging
+ Subscription Colors
+ Real Time wall
+ "Apps" which let you connect to Reddit/HN/various sources. 
+ Import your data from Google Reader.
+ Easily export your data.
+ Mobile Friendly 

###License
Jellyfish Rss is licensed under the MIT license. A link back to this project is appreciated but not required.