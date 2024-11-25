import asyncio
from twikit import Client, TooManyRequests
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import unicodedata

MINIMUM_TWEETS = 10
QUERY = 'technology OR innovation OR AI OR science -filter:links -filter:replies'


def normalize_text(text):
    """
    Normalize the text to remove problematic characters.
    Replace non-ASCII characters with their closest equivalents or remove them.
    """
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')


async def get_tweets(client, tweets):
    if tweets is None:
        # Get initial tweets
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top')  # Await the coroutine
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds...')
        await asyncio.sleep(wait_time)  # Non-blocking sleep
        tweets = await tweets.next()  # Await the coroutine

    return tweets


async def main():
    # Load login credentials
    print("Loading credentials...")
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    # Authenticate to X.com
    print("Initializing client...")
    client = Client(language='en-US')
    # await client.login(auth_info_1=username, auth_info_2=email, password=password)  # Uncomment if login is required
    print("Loading cookies...")
    client.load_cookies('cookies.json')

    # Create a CSV file
    with open('tweets.csv', 'w', encoding="utf-8-sig", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])

    print("Starting tweet extraction...")
    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(client, tweets)  # Await the asynchronous function
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())  # Non-blocking sleep
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = [
                tweet_count,
                normalize_text(tweet.user.name),
                normalize_text(tweet.text),
                tweet.created_at,
                tweet.retweet_count,
                tweet.favorite_count,
            ]

            # Append tweet data to CSV file
            print(f"Saving tweet {tweet_count}: {tweet.text}")
            with open('tweets.csv', 'a', newline='', encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')


# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
