JellyfishRss
============

!!! Currently broken as I integrate RequireJS !!!

Jellyfish Rss will be an RSS reader that is 100% open source and self-hostable. It will be optimized for mobile users.

It is currently in the very very very alpha stages. It is by no means ready for public consumption (yet). :)

The subscriptions are pooled together as users add them. The poller polls all the subscriptions one time only (each rss feed is polled once). If more than one user has an RSS feed with the same URL, it is polled one time only (both users will see the feed results).

###Installation
The installation portion is a major work-in-progress. I'll be working on making this easier at some point.

- Install Prerequisites
```
sudo apt-get install python-dev libpq-dev rabbitmq-server libxml2 libxml2-dev libxslt-dev python-lxml postgresql
```

- Optional Prerequisites (helpful if developing)
```
sudo apt-get install pgadmin3
```

- Install the pip requirements
```
pip install -r requirements.txt
```

### Database Setup
Change the "settings.py" to match your database configuration:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'jellyfish',                      # leafreader path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'postgres',
        'PASSWORD': 'test',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                      # Set to empty string for default.
    }
}
```
Add the database 'jellyfish' and build the database (create your admin user here when prompted):
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

### Sample Data
To get started quickly, you can import a couple of RSS feeds.

CrawlFiles to import some basic feed data:
```
manage.py crawlfiles
```

### Polling
Polling will start when you run Celery (see 'Running Server' above). The default interval is set to 1800 seconds or 30 minutes (configurable in settings.py).

You can force a manual polling action by running:
```
manage.py crawlsites 
```

###Basic Roadmap
1. Implement basic site pages
	- Home [Done]
	- Login [Done]
	- Feeds View [Done]
	- Settings
2. Implement RSS poller [Done]
3. Authentication [Done]
4. User integration [Done]
5. Work on UI
	- Download Favicons [Done]
	- Logo
	- UI Colors
	- UI Typography
	- Mobile/Responsive version
6. Other features
	- Auto Load
	- Search
	- Blacklist keywords
	- Import/Export
	- Folders

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