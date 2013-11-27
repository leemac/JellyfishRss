JellyfishRss
============

Jellyfish Rss will be an RSS reader that is 100% open source and self-hostable. It will be optimized for mobile users.

###Install

1. Clone Repository
2. Install [django-pipeline](https://github.com/cyberdelia/django-pipeline)
3. Install [feedparser](https://pypi.python.org/pypi/feedparser)
4. Install [south](http://south.readthedocs.org/en/latest/installation.html)
5. manage.py syncdb
6. manage.py migrate

###Roadmap
1. Implement basic site pages
	- Home
	- Login
	- Feeds View
	- Settings
2. Implement RSS poller
	- Iterate over sites
	- Add new items
3. Authentication
4. User integration
	- Feeds polled at interval
	- User can login and view feeds
	- User can login and mark feeds as read
	- etc.

###Feature Idea Brain Dump

+ Mark as read for a particular user
+ Mark as favorite for a particular user
+ Add/Remove feeds
+ Read entries for a feed
+ User Authentication
+ View the most recently updated entries with # count next to subscription name
+ View all subscriptions with all items (paging)
+ View favorite entries
+ Email/Share
+ 100% Open Source
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