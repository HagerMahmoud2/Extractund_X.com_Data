# X.com Tweet Extraction Project

## Overview

The **X.com Tweet Extraction Project** is designed to extract and store tweets related to specific topics 
(e.g., technology, AI, innovation, and science) using asynchronous requests. The project scrapes tweets based on a search query 
while handling rate-limiting scenarios. Extracted tweet data is saved in a CSV file for further analysis.

## Features

- **Search Query**: Extracts tweets related to "technology", "innovation", "AI", and "science", excluding links and replies.
- **Asynchronous Processing**: Utilizes Python's `asyncio` for non-blocking operations, enabling efficient tweet extraction.
- **Rate-Limiting Handling**: Gracefully handles rate-limiting by waiting for the reset time when the API limit is reached.
- **Text Normalization**: Ensures tweet text is sanitized by removing problematic non-ASCII characters.
- **CSV Storage**: Saves tweet data such as tweet count, username, text, creation time, retweet count, and like count into a CSV file.

## Tools and Technologies

- **Python**: Programming language used for the project.
- **Twikit**: A Python client for interacting with X.com.
- **asyncio**: Used for handling asynchronous tasks and non-blocking I/O operations.
- **ConfigParser**: For reading configuration files containing login credentials.
- **CSV**: Used to save the extracted tweet data in a structured format.
- **unicodedata**: For normalizing and handling non-ASCII characters in tweet text.

## How It Works

1. **Credentials Loading**: The project loads login credentials (e.g., username, email, password) from a configuration file (`config.ini`) to authenticate with X.com.
2. **Client Initialization**: Initializes the `twikit.Client` and loads necessary cookies from a file (`cookies.json`) for authentication.
3. **Tweet Extraction**: Tweets are fetched asynchronously based on the specified search query. The program waits for the rate limit to reset when the limit is reached.
4. **Text Normalization**: Non-ASCII characters in tweet text are removed or replaced to ensure compatibility and clean data.
5. **CSV Output**: Extracted tweet details, including tweet count, username, tweet text, creation time, retweets, and likes, are written to a CSV file (`tweets.csv`).

