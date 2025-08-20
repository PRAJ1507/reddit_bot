📌 Reddit Bot

A Python bot that scans Reddit posts in specific subreddits for keywords (like AI, technology, climate), generates intelligent replies using Google Gemini, and posts them automatically.
The bot also logs all interactions in a local SQLite database and provides analytics (how many replies, skipped posts, keywords matched, etc.).

🚀 Features

✅ Scans multiple subreddits for keywords & aliases

✅ Generates replies with Google Gemini Pro → fallback to Flash

✅ Filters replies with a safety check before posting

✅ Skips already-replied posts (using SQLite DB)

✅ Analytics dashboard (analytics.py) to view stats

✅ Configurable via config.yaml

📂 Project Structure
reddit_bot/
├── main.py                # Main bot runner
├── analytics.py           # Analytics dashboard
├── config.yaml            # Bot configuration (subreddits, keywords, LLM, etc.)
├── utils/
│   ├── reddit_client.py   # Reddit API client
│   ├── db.py              # SQLite interaction logger
│   ├── llm_client.py      # Google Gemini client (LangChain wrapper)
│   └── safety.py          # Content safety filter
└── interactions.sqlite    # Auto-created DB for logs

🔧 Installation

Clone this repository

```bash

git clone https://github.com/YOUR_USERNAME/reddit_bot.git
cd reddit_bot

```


Install dependencies with uv
```bash

uv sync

```

Set up config.yaml
Edit config.yaml with your keys and settings:

reddit:
  client_id: "YOUR_REDDIT_CLIENT_ID"
  client_secret: "YOUR_REDDIT_CLIENT_SECRET"
  user_agent: "reddit-twitter-bot by u/YOUR_BOT_USERNAME"
  username: "YOUR_BOT_USERNAME"
  password: "YOUR_BOT_PASSWORD"

subreddits:
  - "test"
  - "ChatGPT"

keywords:
  - "AI"
  - "technology"

llm:
  - provider: "google"
  - model: "gemini-1.5-pro" # "gemini-1.5-flash" non pro
  - api_key: "YOUR_GOOGLE_GENAI_API_KEY"



▶️ Running the Bot

Start scanning and replying:

```bash

uv run main.py

```

View analytics (replies, skips, keywords, subreddits):

```bash

uv run analytics.py

```

🛡️ Notes

Test the bot in r/test before using it on real subreddits.

Respect Reddit’s API rules — don’t spam.

It’s best to create a separate bot account instead of using your main Reddit account.
