from scrapegraphai.graphs import SmartScraperMultiGraph
import os, json

graph_cfg = {
    "llm": {
        # Any Groq-served chat model will do; gemma-7b-it is fast & cheap
        "model": "groq/llama3-70b-8192",          # other options: groq/llama3-70b-8192 …
        "api_key": os.environ["GROQ_API_KEY"],
        "temperature": 0.0,
        # optional rate-limit if you hammer the API
        # "rate_limit": {"requests_per_second": 1}
    }
}

urls = [f"https://news.ycombinator.com/?p={i}" for i in range(1, 6)]
prompt = "Return rank, title, link and points for every story."

scraper = SmartScraperMultiGraph(prompt=prompt,
                                 source=urls,
                                 config=graph_cfg)
data = scraper.run()
print(json.dumps(data, indent=2))
