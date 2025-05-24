import asyncpraw
import asyncio
import csv
import os

async def search_and_save_to_csv():
    reddit = asyncpraw.Reddit(
        client_id="eJeDu9okVJ7Bf-7v2HFaeg",
        client_secret="7Gw0fV7lahWaa-RjP-5reZkKmwFZ7Q",
        user_agent="TFM"
    )

    subreddits = ["OpinionesPolemicas", "AskRedditespanol", "Adicciones", "Drogas", "askspain"]
    search_terms = "marihuana OR cocaína OR tabaco OR cafeína OR tusi OR mdma OR cannabis OR cigarro OR porro OR alcohol"

    output_path = os.path.join("data", "reddit_posts.csv")
    os.makedirs("data", exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["subreddit", "title", "url", "author", "comment"])

        for subreddit_name in subreddits:
            subreddit = await reddit.subreddit(subreddit_name)
            print(f"Buscando en r/{subreddit_name}...")

            async for post in subreddit.search(search_terms, sort="new", limit=50):
                await post.load()
                comments_text = []

                await post.comments.replace_more(limit=0)
                for comment in post.comments:
                    if isinstance(comment, asyncpraw.models.Comment) and comment.body:
                        comments_text.append(comment.body)

                if comments_text:
                    for comment in comments_text:
                        writer.writerow([subreddit_name, post.title, post.url, str(post.author), comment])
                else:
                    writer.writerow([subreddit_name, post.title, post.url, str(post.author), ""])

    print(f"Datos guardados en {output_path}")

if __name__ == "__main__":
    asyncio.run(search_and_save_to_csv())
