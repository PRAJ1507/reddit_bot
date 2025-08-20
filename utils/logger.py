import sqlite3

def init_db(path="db/interactions.sqlite"):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Table for replies
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id TEXT PRIMARY KEY,
            subreddit TEXT,
            keyword TEXT,
            reply TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table for scanned posts (replied or skipped)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id TEXT,
            subreddit TEXT,
            matched_keyword TEXT,
            action TEXT, -- "replied" or "skipped"
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def log_interaction(post_id, subreddit, keyword, reply, path="db/interactions.sqlite"):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # log into interactions table
    cursor.execute("""
        INSERT OR REPLACE INTO interactions (id, subreddit, keyword, reply)
        VALUES (?, ?, ?, ?)
    """, (post_id, subreddit, keyword, reply))

    # also log into scans table as "replied"
    cursor.execute("""
        INSERT INTO scans (id, subreddit, matched_keyword, action)
        VALUES (?, ?, ?, ?)
    """, (post_id, subreddit, keyword, "replied"))

    conn.commit()
    conn.close()

def log_skip(post_id, subreddit, keyword, path="db/interactions.sqlite"):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scans (id, subreddit, matched_keyword, action)
        VALUES (?, ?, ?, ?)
    """, (post_id, subreddit, keyword, "skipped"))
    conn.commit()
    conn.close()

def has_replied(post_id, path="db/interactions.sqlite") -> bool:
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM interactions WHERE id = ?", (post_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
