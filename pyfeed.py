import feedparser
import datetime
import sys
from prettytable import PrettyTable, PLAIN_COLUMNS
import fileinput

def generate_datetimes(time_struct):
    published = time_struct
    year_published = published.tm_year
    month_published = published.tm_mon
    day_published = published.tm_mday
    hour_published = published.tm_hour
    minute_published = published.tm_min
    sec_published = published.tm_sec
    published_is_dst = published.tm_isdst
    published_timezone = published.tm_zone

    return datetime.datetime(year_published, month_published, day_published, hour_published, minute_published, sec_published)

def get_all_feeds_data():
    feeds_data = []

    with open("urls", "r") as urls:
        feed_urls = [url.strip("\n") for url in urls]

        for url in feed_urls:
            print(f"parsing {url}")
            feed = feedparser.parse(url)
            feeds_data.append(feed)

    return feeds_data

def article_list_view(feeds, selected_feed):
    table = PrettyTable()
    table.align = "l"
    table.border = False
    table.field_names = ["", "Published on", "Article Title"]

    # In future user can select this
    feed = feeds[selected_feed]

    feed_title = feed["feed"]["title"]

    print(f"Articles for {feed_title}")

    entries = feed["entries"]

    for index, entry in enumerate(entries):
        dt_published = generate_datetimes(entry['published_parsed']).strftime("%d %b %Y")
        article_title = entry["title"]

        table.add_row([index, dt_published, article_title])

    print(table)

def feed_list_view(feeds):
    table = PrettyTable()
    table.align = "l"
    table.border = False
    table.field_names = ["", "Articles", "Feed Title"]

    for index, feed in enumerate(feeds):
        feed_title = feed["feed"]["title"]
        article_count = len(feed["entries"])

        table.add_row([index, article_count, feed_title])

    print(table)

def read_article(article):
    article_title = article["title"]
    article_link = article["link"]
    article_published = generate_datetimes(article["published_parsed"])
    article_content = article["description"]
    sys.stdout.write(f"\x1b[1mTitle:\x1b[0m {article_title}\n\x1b[1mLink:\x1b[0m {article_link}\n\x1b[1mPublished:\x1b[0m {article_published}\n\n{article_content}\n")

feeds = get_all_feeds_data()

# Default context
context = "feeds"
current_feed = 0
feed_list_view(feeds)

while True:
    stdin = input(f"\x1b[1m[pyfeed view: \x1b[4m{context}\x1b[0m \x1b[1m]\x1b[0m ")
    command, *values = stdin.split(" ")
    match command:
        case "open":
            match context:
                case "feeds":
                    if len(values) > 1:
                        print("error: more than 1 value; only takes in an index (int)")
                        break
                    index = int(values[0])
                    article_list_view(feeds, index)
                    context = "articles"
                    current_feed = index
                case "articles":
                    if len(values) > 1:
                        print("error: more than 1 value; only takes in an index (int)")
                        break
                    index = int(values[0])
                    read_article(feeds[current_feed]["entries"][index])
        case "back":
            match context:
                case "articles":
                    feed_list_view(feeds)
                    context = "feeds"
        case "quit":
            print("Quitting...")
            sys.exit(0)
