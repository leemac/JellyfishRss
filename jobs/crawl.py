import feedparser

d = feedparser.parse("http://rss.cnn.com/rss/cnn_topstories.rss")

print("The title is" + d['feed']['title'])