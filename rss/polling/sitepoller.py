from datetime import datetime
from time import mktime

from urlparse import urlparse

from rss.models import Subscription
from rss.models import SubscriptionItem
from bs4 import BeautifulSoup
from PIL import Image

import logging
import cStringIO

logger = logging.getLogger(__name__)

import lxml.html as lh
import urllib2
import feedparser


class SitePoller:
    def add_site_and_poll(self, rss_url):
        self.add_site(rss_url)

        subscription = Subscription.objects.get(url=rss_url)
        self.poll_site(subscription)

    def add_site(self, rss_url):
        try:
            subscription = Subscription.objects.get(url=rss_url)
        except Subscription.DoesNotExist:
            d = feedparser.parse(rss_url)

            subscription = Subscription()
            subscription.title = d.feed.title
            subscription.url = rss_url
            subscription.color = "#333"
            subscription.save()

    def poll_site(self, subscription):
        d = feedparser.parse(subscription.url)

        link = d.feed.link

        hostname = urlparse(d.feed.link).hostname
        link = "http://" + hostname

        if not subscription.favicon_url:

            doc = lh.parse(link)

            favicons = doc.xpath('//link[@rel="Shortcut Icon"]/@href')

            if len(favicons) == 0:
                favicons = doc.xpath('//link[@rel="shortcut icon"]/@href')

            if len(favicons) > 0:
                favicon = favicons[0]
            else:
                favicon = link + "/favicon.ico"

            if favicon:
                fav_url = favicon

                if not fav_url.startswith("http"):
                    fav_url = link + favicon

                subscription.favicon_url = fav_url
                subscription.save()

        for item in d.entries:

            existingItem = SubscriptionItem.objects.filter(url=item.link).filter(url=item.link).count()

            if (existingItem != 0):
                continue

            print "Adding: " + item.link

            object = SubscriptionItem()
            object.title = item.title
            object.url = item.link
            object.subscription_id = subscription.id
            object.thumbnail_url = ""
            # Published may/may not be where we'd like
            try:
                object.published = datetime.fromtimestamp(mktime(item.published_parsed))
            except AttributeError:
                object.published = datetime.fromtimestamp(mktime(item.date_parsed))

            # Content may/may not be where we'd like
            try:
                object.content = item.content[0].value
            except AttributeError:
                try:
                    object.content = item.description
                except AttributeError:
                    object.content = ""

            object.save()

    def poll_thumb(self, subscription):

        for object in SubscriptionItem.objects.filter(subscription_id=subscription.id, thumbnail_processed=False):
            object.thumbnail_url = self.get_story_thumbnail(object.url)
            object.thumbnail_processed = True
            object.save()

    def get_story_thumbnail(self, url):

        hostname = urlparse(url).hostname
        rootUrl = "http://" + hostname

        print "Locating story image: " + url

        try:
            page = BeautifulSoup(urllib2.urlopen(url))
        except urllib2.URLError:
            return ""

        print "Page loaded...parsing images..."
        images = page.findAll('img')

        largest_image_size = 0
        largest_image_src = ""

        # Locate story image
        for img in images:

            imageSource = img.get("src")

            if (imageSource is None):
                continue;

            if not "http" in imageSource:
                image_url = str(rootUrl + "/" + imageSource)
            else:
                image_url = imageSource


            # Skip blacklisted keywords in image path
            if ("css" in imageSource or
                        "arrow" in imageSource or
                        "advert" in imageSource or
                        "bttn" in imageSource or
                        "php" in imageSource or
                        "gif" in imageSource or
                        "footer" in imageSource or
                        "logo" in imageSource):
                print "SKipping Image"
                continue

            print "Processing Image: " + image_url

            try:
                file = cStringIO.StringIO(urllib2.urlopen(image_url).read())
                image = Image.open(file)
            except IOError:
                print "No image found: " + imageSource
                continue

            height, width = image.size

            # skip icons or avatars
            if (height < 75) or (width < 75):
                continue;

            #  Store product of height/width for comparison
            size = height * width

            # Compare product with largest found thus far
            # and make note of it if it is the largest
            if largest_image_size < size:
                largest_image_size = size
                largest_image_src = image_url

                # Stop searching if big enough image is found
                if (size > 70000):
                    print "Large image found, stop searching"
                    break

        return image_url

    def poll(self):

        for subscription in Subscription.objects.all():
            self.poll_site(subscription)

        self.poll_thumbs()

    def poll_thumbs(self):

        for subscription in Subscription.objects.all():
            self.poll_thumb(subscription)
