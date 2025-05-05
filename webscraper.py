import requests
from bs4 import BeautifulSoup

base = "http://quotes.toscrape.com"
url  = base + "/page/1/"

all_quotes = []
while url:
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")


    for q in soup.select("div.quote"):
        text   = q.select_one("span.text").get_text(strip=True)
        author = q.select_one("small.author").get_text(strip=True)
        tags   = [t.get_text(strip=True) for t in q.select("div.tags a.tag")]
        all_quotes.append({"text": text, "author": author, "tags": tags})


    nxt = soup.select_one("li.next a")
    url = base + nxt["href"] if nxt else None


import json
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(all_quotes, f, ensure_ascii=False, indent=2)
