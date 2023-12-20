from prettytable import PrettyTable, PLAIN_COLUMNS

def get_new_table():
    table = PrettyTable()
    table.align = "l"
    table.border = False

    return table

def article_list_view(feeds, selected_feed):
    table = get_new_table()
    table.field_names = ["i", "Published on", "Article name"]
    # In future user can select this
    feed = feeds[selected_feed]

    feed_title = feed["feed_title"]

    print(f"Articles for {feed_title}")

    entries = feed["feed_items"]

    for index, entry in enumerate(entries):
        dt_published = entry["date_published"]
        article_title = entry["title"]

        table.add_row([index, dt_published, article_title])

    return table

def feed_list_view(feeds):
    table = get_new_table()
    table.field_names = ["i", "Articles", "Feed Title"]

    for index, feed in enumerate(feeds):
        feed_title = feed["feed_title"]
        article_count = len(feed["feed_items"])

        table.add_row([index, article_count, feed_title])

    return table
