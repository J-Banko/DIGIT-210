import requests
from bs4 import BeautifulSoup

base = "http://quotes.toscrape.com"
url  = base + "/page/1/"

all_quotes = []
while url:
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # extract each quote block
    for q in soup.select("div.quote"):
        text   = q.select_one("span.text").get_text(strip=True)
        author = q.select_one("small.author").get_text(strip=True)
        tags   = [t.get_text(strip=True) for t in q.select("div.tags a.tag")]
        all_quotes.append({"text": text, "author": author, "tags": tags})

    # find the “next” page link
    nxt = soup.select_one("li.next a")
    url = base + nxt["href"] if nxt else None

# e.g. write out to JSON or CSV
import json
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(all_quotes, f, ensure_ascii=False, indent=2)
