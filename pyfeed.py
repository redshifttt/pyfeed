import datetime
import sys
from bs4 import BeautifulSoup
import requests
import views

# def generate_datetimes(time_struct):
#     published = time_struct
#
#     year_published = published.tm_year
#     month_published = published.tm_mon
#     day_published = published.tm_mday
#     hour_published = published.tm_hour
#     minute_published = published.tm_min
#     sec_published = published.tm_sec
#     published_is_dst = published.tm_isdst
#     published_timezone = published.tm_zone
#
#     return datetime.datetime(year_published, month_published, day_published, hour_published, minute_published, sec_published)

def get_all_feeds_data():
    feeds_data = []

    with open("urls", "r") as urls:
        feed_urls = [url.strip("\n") for url in urls]

        for n, url in enumerate(feed_urls):
            sys.stdout.write(f"parsing {url}\n")
            with requests.get(url) as r:
                parsed_feed = BeautifulSoup(r.text, 'lxml-xml')
                feed_items = parsed_feed.find_all("item")
                feeds_data.append({
                    "feed_title": parsed_feed.title.string,
                    "feed_description": parsed_feed.description.string,
                    "feed_items": []
                })
                for item in feed_items:
                    feeds_data[n]["feed_items"].append(
                        {
                            "title": item.title.string,
                            "date_published": item.pubDate.string,
                            "link": item.guid.string,
                            "content": BeautifulSoup(item.description.string, 'html.parser').get_text(),
                        }
                    )
    return feeds_data

def read_article(article):
    sys.stdout.write(f'Title: {article["title"]}\n')
    sys.stdout.write(f'Published on: {article["date_published"]}\n\n')
    sys.stdout.write(article["content"])

feeds = get_all_feeds_data()
print(views.feed_list_view(feeds))

# Default context
context = "feeds"
current_feed = 0

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
                    print(views.article_list_view(feeds, index))
                    context = "articles"
                    current_feed = index
                case "articles":
                    if len(values) > 1:
                        print("error: more than 1 value; only takes in an index (int)")
                        break
                    index = int(values[0])
                    read_article(feeds[current_feed]["feed_items"][index])
        case "back":
            match context:
                case "articles":
                    print(views.feed_list_view(feeds))
                    context = "feeds"
        case "ls":
            match context:
                case "articles":
                    print(views.article_list_view(feeds, current_feed))
                case "feeds":
                    print(views.feed_list_view(feeds))
        case "quit":
            print("Quitting...")
            sys.exit(0)
        case "help":
            sys.stdout.write("help:\nopen <n> - open index <n> in the list\nback - moves backwards through the different views\nls - list the contents of the current view\nquit - exit the program\nhelp - show this help dialog\n")
        case _:
            print(f"error: '{command}' is not a command")
