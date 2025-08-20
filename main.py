import time
import re
from utils.config_loader import load_config
from utils.reddit_client import get_reddit_client, fetch_posts, already_replied
from utils.llm_client import generate_reply
from utils.logger import init_db, log_interaction, has_replied, log_skip
from utils.safety_filter import is_safe_reply

def contains_keyword(text: str, keyword: str, aliases: dict = None):
    """
    Match keyword or any of its aliases as whole words (case-insensitive).
    Returns (bool, matched_word).
    """
    text = text.lower()
    words_to_check = [keyword.lower()]

    if aliases and keyword in aliases:
        words_to_check.extend([a.lower() for a in aliases[keyword]])

    for word in words_to_check:
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, text):
            return True, word

    return False, None

def main():
    config = load_config()
    reddit = get_reddit_client(config)
    init_db()

    username = config["reddit"]["username"]

    while True:
        print("🔍 Scanning subreddits...")
        posts = fetch_posts(reddit, config["subreddits"], limit=10)

        for post in posts:
            for kw in config["keywords"]:
                matched, word = contains_keyword(
                    post["title"] + " " + post["body"],
                    kw,
                    config.get("keyword_aliases", {})
                )
                if matched:
                    # ✅ Skip if already replied before (DB)
                    if has_replied(post["id"]):
                        print(f"⏩ Skipping post {post['id']} (already in replied)")
                        log_skip(post["id"], post["subreddit"], kw)
                        continue

                    # ✅ Skip if bot username already commented
                    if already_replied(reddit, post["id"], username):
                        print(f"⏩ Skipping post {post['id']} (already replied by {username})")
                        log_skip(post["id"], post["subreddit"], kw)
                        continue

                    print(f"✅ Found keyword '{kw}' (matched on '{word}') in post: {post['title']}")

                    reply = generate_reply(post["title"] + "\n" + post["body"], config)

                    if is_safe_reply(reply):
                        print("💬 Reply PASSED safety check:", reply)
                        log_interaction(post["id"], post["subreddit"], kw, reply)

                        # 🚨 Uncomment when ready to post live on Reddit
                        # reddit.submission(id=post["id"]).reply(reply)

                        time.sleep(config["bot"]["reply_delay"])
                    else:
                        print("⛔ Reply BLOCKED by safety filter:", reply)
                        log_skip(post["id"], post["subreddit"], kw)

        # Wait before next scan
        time.sleep(config["bot"]["scan_interval"])

if __name__ == "__main__":
    main()
