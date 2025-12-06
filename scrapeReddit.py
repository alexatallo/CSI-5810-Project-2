import requests
import pandas as pd
import time

subreddits = [
    "capitalism",
    "capitalismvsocialism",
    "socialism",
    "economics"
]

keywords = ["capitalism", "capitalist", "anti-capitalist", "market economy", "free market"]
limit = 200  #max posts per subreddit
all_posts = []

print("starting")

for sub in subreddits:
    print(f"\nScraping r/{sub}...")
    url = f"https://www.reddit.com/r/{sub}/new.json?limit=100"

    after = None
    collected = 0

    while collected < limit:
        full_url = url + (f"&after={after}" if after else "")
        headers = {"User-Agent": "script:reddit-data-collector:v1.0 (by u/alexatallo)"}

        r = requests.get(full_url, headers=headers)

        if r.status_code != 200:
            print(f"Error {r.status_code} — sleeping.")
            time.sleep(15)
            continue

        data = r.json()
        posts = data["data"]["children"]

        if not posts:
            break

        for p in posts:
            post = p["data"]
            text = post.get("selftext", "")

            #keep posts with body text and matching keywords
            if text and any(k.lower() in (text + post.get("title", "")).lower() for k in keywords):
                all_posts.append([
                    post["id"],
                    post["created_utc"],
                    post.get("title", ""),
                    text,
                    post.get("score", 0),
                    sub
                ])
                collected += 1
                if collected >= limit:
                    break

        after = data["data"].get("after")
        if not after:
            break

        time.sleep(3)

    print(f"Collected {collected} posts from r/{sub}")

df = pd.DataFrame(all_posts, columns=["ID", "Timestamp", "Title", "Text", "Score", "Subreddit"])
df.to_csv("reddit_capitalism_filtered_posts2.csv", index=False)
print("Saved")