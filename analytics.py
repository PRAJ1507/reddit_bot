import sqlite3
from tabulate import tabulate

DB_PATH = "db/interactions.sqlite"

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Total replies
    cursor.execute("SELECT COUNT(*) FROM interactions")
    total_replies = cursor.fetchone()[0]

    # Replies per keyword
    cursor.execute("""
        SELECT keyword, COUNT(*) as count
        FROM interactions
        GROUP BY keyword
        ORDER BY count DESC
    """)
    replies_by_keyword = cursor.fetchall()

    # Skipped posts
    cursor.execute("SELECT COUNT(*) FROM scans WHERE action='skipped'")
    total_skipped = cursor.fetchone()[0]

    # Latest scans (both replied + skipped)
    cursor.execute("""
        SELECT subreddit, matched_keyword, action, timestamp
        FROM scans
        ORDER BY timestamp DESC
        LIMIT 10
    """)
    recent_scans = cursor.fetchall()

    conn.close()

    print("\n📊 BOT ANALYTICS REPORT\n")
    print(f"🔹 Total replies made: {total_replies}")
    print(f"🔹 Total posts skipped: {total_skipped}\n")

    print("🔹 Replies by keyword:")
    print(tabulate(replies_by_keyword, headers=["Keyword", "Count"], tablefmt="grid"))

    print("\n🔹 Latest 10 scans (replied or skipped):")
    print(tabulate(recent_scans, headers=["Subreddit", "Keyword", "Action", "Timestamp"], tablefmt="grid"))

if __name__ == "__main__":
    get_stats()
