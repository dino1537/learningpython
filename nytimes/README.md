1. **Fetch News Articles**: By default, the script fetches news articles from
   the 'home' section. You can specify a different section by using the
   `--section` option followed by the section name. For example:

   ```
   python nytimes_news.py --section world
   ```

2. **Fetch Popular Articles**: If you want to get the most popular articles, use
   the `--popular` option. For example:

   ```
   python nytimes_news.py --popular
   ```

3. In addition to the `--list hardcover-fiction` option, you have several other
   options to use with the `nytimes_news.py` script:

   ```
   python nytimes_news.py --list hardcover-fiction
   ```

- **`--list <list-name>`**: Fetch and display the top sellers list for books
  from a specific best sellers list. Replace `<list-name>` with the name of the
  list you're interested in. The script uses `hardcover-fiction` as the default
  list, but you can specify other lists such as `paperback-nonfiction`,
  `childrens-middle-grade`, `young-adult`, etc. For example:
  ```
  python nytimes_news.py --list paperback-nonfiction
  ```

If you want to see a list of all available best sellers lists, you can use the
`/lists/names.json` endpoint of the New York Times API to retrieve them.
However, this functionality would need to be added to the script as a new
feature.

Remember, you can only use one option at a time when running the script. If you
run the script without any options, it will default to fetching news articles
from the 'home' section.
