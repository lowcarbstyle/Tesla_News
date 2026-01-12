import feedparser

query = "Tesla"
encoded_query = query.replace(" ", "+")
rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
feed = feedparser.parse(rss_url)

if feed.entries:
    print(f"Total entries: {len(feed.entries)}")
    for i, entry in enumerate(feed.entries[:10]):
        print(f"--- Entry {i} ---")
        if 'summary' in entry:
            if '<img' in entry.summary:
                print("Image found in summary!")
                print(entry.summary[:1000])
            else:
                print("No image in summary.")
else:
    print("No entries found")
