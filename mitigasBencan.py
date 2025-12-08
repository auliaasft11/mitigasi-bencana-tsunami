import tweepy
import csv

# =========================================================
# MASUKKAN KEMBALI API KEY BARU KANDA (JANGAN PAKAI YANG LAMA)
# =========================================================
BEARER = "AAAAAAAAAAAAAAAAAAAAANr95gEAAAAAcCwaPVtJT2aBWOSUxGPnOLvTnkA%3DRK5sNS2fpeOOO4sDSH0uik4olQ7A0YPrW0NB9K6XM4qGkpL6PD"
API_KEY = "HfpsbXa6icyZeLKMKWw3AfBbG"
API_SECRET = "oK2zjmrl4iWubK6PCtDriYJLKhncuL5gM0cYf7lV5eAFMBxDhE"

# =========================================================
# INISIALISASI CLIENT TEEPY (FREE ESSENTIAL → RECENT SEARCH)
# =========================================================
client = tweepy.Client(
    bearer_token=BEARER,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    wait_on_rate_limit=True
)

# =========================================================
# QUERY TSUNAMI (BAHASA INGGRIS)
# =========================================================
query = (
    "(tsunami OR \"tsunami warning\" OR \"earthquake tsunami\" OR "
    "\"tsunami alert\" OR \"seismic sea wave\") "
    "-is:retweet lang:en"
)

# =========================================================
# FILE OUTPUT (CSV)
# =========================================================
output_file = "tsunami_dataset_recent.csv"

# Tulis header hanya sekali
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["tweet_id", "timestamp", "username", "tweet_text"])

# =========================================================
# FUNGSI PENGAMBILAN DATA (RECENT SEARCH)
# =========================================================
def fetch_tsunami_tweets():
    print("Mengambil dataset tsunami (7 hari terakhir)...")

    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=100,
            tweet_fields=["created_at", "author_id"],
            expansions=["author_id"]
        )
    except Exception as e:
        print("Error saat memanggil API:", e)
        return

    if not tweets.data:
        print("Tidak ada data ditemukan untuk query ini.")
        return

    # Mapping user ID → username
    users = {}
    if tweets.includes and "users" in tweets.includes:
        users = {u.id: u.username for u in tweets.includes["users"]}

    # Simpan data ke CSV
    with open(output_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for tweet in tweets.data:
            username = users.get(tweet.author_id, "unknown")
            writer.writerow([
                tweet.id,
                tweet.created_at,
                username,
                tweet.text.replace("\n", " ")  # Hindari baris patah
            ])

    print(f"Data berhasil disimpan → {output_file}")


# =========================================================
# EKSEKUSI PROGRAM
# =========================================================
if __name__ == "__main__":
    fetch_tsunami_tweets()
