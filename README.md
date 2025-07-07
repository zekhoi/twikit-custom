# phin/twikit

A Simple Twitter API Scraper. 

This repo is forked off https://github.com/d60/twikit, credit to d60 for the initial development.
this library intends to make an up-to-date fork of Twikit, as the original Twikit library is prone to Twitter's detection.

You can use functions such as posting or searching for tweets without an API key using this library.

- [Documentation (English)](https://twikit.readthedocs.io/en/latest/twikit.html)



## Features

### No API Key Required

This library uses scraping and does not require an API key.

### Free

This library is free to use.


## Functionality

By using Twikit, you can access functionalities such as the following:

-  Create tweets

-  Search tweets

-  Retrieve trending topics

- etc...



## Installing

```bash

pip install git+https://codeberg.org/phin/twikit

```



## Quick Example

**Define a client and log in to the account.**

```python
import asyncio
from twikit import Client

USERNAME = 'example_user'
EMAIL = 'email@example.com'
PASSWORD = 'password0000'

# Initialize client
client = Client('en-US')

async def main():
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json'
    )

asyncio.run(main())
```

**Create a tweet with media attached.**

```python
# Upload media files and obtain media_ids
media_ids = [
    await client.upload_media('media1.jpg'),
    await client.upload_media('media2.jpg')
]

# Create a tweet with the provided text and attached media
await client.create_tweet(
    text='Example Tweet',
    media_ids=media_ids
)

```

**Search the latest tweets based on a keyword**
```python
tweets = await client.search_tweet('python', 'Latest')

for tweet in tweets:
    print(
        tweet.user.name,
        tweet.text,
        tweet.created_at
    )
```

**Retrieve user tweets**
```python
tweets = await client.get_user_tweets('123456', 'Tweets')

for tweet in tweets:
    print(tweet.text)
```

**Send a dm**
```python
await client.send_dm('123456789', 'Hello')
```

**Get trends**
```python
await client.get_trends('trending')
```

More Examples: [examples](https://github.com/d60/twikit/tree/main/examples) <br>

## Contributing

If you encounter any bugs or issues, please report them on [issues](https://github.com/d60/twikit/issues).


If you find this library useful, consider starring this repository⭐️
