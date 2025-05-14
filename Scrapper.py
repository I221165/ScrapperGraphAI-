"""
Scrape https://scrapegraphai.com/ using Groq’s Llama-3/Gemma model
and Playwright for JS rendering.
---------------------------------------------------------------
Prerequisites:
  pip install scrapegraphai playwright python-dotenv
  playwright install            # downloads the headless browsers
  setx GROQ_API_KEY "sk-…"      # Windows PowerShell; or export on *nix
  (optionally) run Ollama if you need embeddings
"""

import os
from dotenv import load_dotenv
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info

load_dotenv()                       # picks up GROQ_API_KEY from .env or the shell

# ────────────────── Graph / LLM configuration ──────────────────
graph_config = {
    "llm": {
        # Any Groq-served chat model will do; gemma-7b-it is fast & cheap
        "model": "groq/llama3-70b-8192",          # other options: groq/llama3-70b-8192 …
        "api_key": os.environ["GROQ_API_KEY"],
        "temperature": 0.0,
        # optional rate-limit if you hammer the API
        # "rate_limit": {"requests_per_second": 1}
    },

    # Groq doesn't supply embeddings; use a local Ollama model
    "embeddings": {
        "model": "ollama/nomic-embed-text"
        # if Ollama runs on another host/port: "base_url": "http://localhost:11434"
    },

    # Playwright settings
    "headless": False,              # flip to True on a server
}

# ────────────────────── Build & run the graph ──────────────────
smart_scraper_graph = SmartScraperGraph(
    prompt="What is this about?",
    source="https://charanhu.medium.com/revolutionizing-web-scraping-with-scrapegraphai-a-comprehensive-guide-d2ca20800952",
    config=graph_config,
)

result = smart_scraper_graph.run()
print("=== RESULT ===")
print(result)

print("\n=== EXECUTION INFO ===")
print(prettify_exec_info(smart_scraper_graph.get_execution_info()))
