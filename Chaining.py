# Chaining.py  –  crawl "next" pages, then multipage-scrape every article
import os, json, time
from typing import List, Optional
from pydantic import BaseModel
from scrapegraphai.graphs import SmartScraperGraph, SmartScraperMultiGraph

# ---------------------------------------------------------------------
# 1. Graph-wide settings  (Groq model, headless Playwright)
# ---------------------------------------------------------------------
cfg = {
    "llm": {
        "model":      "groq/llama3-70b-8192",
        "api_key":    os.environ["GROQ_API_KEY"],
        "temperature": 0.0
    },
    "headless": True,      # flip False to watch the browser
    "verbose":  True       # prints each node’s actions
}

# ---------------------------------------------------------------------
# 2. Hard schema  (Pydantic model guarantees keys exist)
# ---------------------------------------------------------------------
class PageSchema(BaseModel):
    links: List[str]
    next:  Optional[str] = None     # null or URL

# ---------------------------------------------------------------------
# 3. Crawl through paginated section, collect article URLs
# ---------------------------------------------------------------------
start_url     = "https://example.com/blog/page/1"
article_links = []

while start_url:
    print(f"\n▶ processing {start_url}")
    graph = SmartScraperGraph(
        prompt=(
            "Return JSON with exactly two keys:\n"
            "  links – array of full article URLs on this page\n"
            "  next  – URL of the next page, or null if this is the last page"
        ),
        source=start_url,
        config=cfg,
        schema=PageSchema           # <- **pass the *class*, not a string**
    )
    page = graph.run()              # guaranteed to be PageSchema instance / dict
    print("links found:", len(page["links"]))

    article_links.extend(page["links"])
    start_url = page["next"]        # None stops the loop

print(f"\nTotal article links collected: {len(article_links)}")

# ---------------------------------------------------------------------
# 4. Deep-scrape every collected article in parallel
# ---------------------------------------------------------------------
if article_links:
    scraper = SmartScraperMultiGraph(
        prompt="Extract title, author, published_date, and full body.",
        source=article_links,
        config=cfg
    )
    articles = scraper.run()
    print(json.dumps(articles, indent=2))
else:
    print("No article links collected – skipping article scrape.")
