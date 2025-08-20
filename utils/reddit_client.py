import praw

def get_reddit_client(config):
    return praw.Reddit(
        client_id=config["reddit"]["client_id"],
        client_secret=config["reddit"]["client_secret"],
        user_agent=config["reddit"]["user_agent"],
        username=config["reddit"]["username"],
        password=config["reddit"]["password"],
    )

def fetch_posts(reddit, subreddits, limit=10):
    posts = []
    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        for post in subreddit.new(limit=limit):
            posts.append({
                "id": post.id,
                "subreddit": sub,
                "title": post.title,
                "body": post.selftext,
                "url": post.url
            })
    return posts

def already_replied(reddit, post_id, username: str) -> bool:
    """
    Check if the given username has already replied to this post.
    """
    try:
        submission = reddit.submission(id=post_id)
        submission.comments.replace_more(limit=0)  # flatten comment tree
        for comment in submission.comments.list():
            if comment.author and comment.author.name.lower() == username.lower():
                return True
    except Exception as e:
        print(f"⚠️ Error checking comments for post {post_id}: {e}")
    return False
