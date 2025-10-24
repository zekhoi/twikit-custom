import asyncio
from twikit import Client
import os

USERNAME = 'username'
EMAIL = 'email@gmail.com'
PASSWORD = 'password'
PROXY = 'http://user:pass@proxyserver:port'  # Optional proxy configuration

# Initialize client
# client = Client('en-US')
client = Client('en-US', proxy=PROXY)

current_path = __file__.rsplit('/', 1)[0]

async def main(): 
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file=f'{current_path}/cookies.json'
    )

    tweet = await client.create_tweet("hello world from twikit!")
    print(tweet)

asyncio.run(main())