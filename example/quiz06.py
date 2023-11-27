import asyncio
import aiohttp
import pandas as pd

async def fetch_json(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_news_content(session, url, is_pdf):
    if is_pdf:
        return ""
    async with session.get(url) as response:
        return await response.text()

async def main():
    base_url = 'https://www.ditp.go.th'
    posts_url = f'{base_url}/wp-json/ditp/v1/posts?offset=0&limit=20'
    async with aiohttp.ClientSession() as session:
        posts_data = await fetch_json(session, posts_url)
        tasks = []
        for post in posts_data['data']:
            news_url = f'{base_url}/post/{post["ContentID"]}'
            tasks.append( fetch_news_content(session, news_url, post["PDF"]))
        contents = await asyncio.gather(*tasks)

    contents
    data = [{
            'title': post['Title'],
            'publish_date': post['PublishDate'],
            'source_url': f'{base_url}/post/{post["ContentID"]}',
            'is_pdf': post['PDF'],
            'content': content
            } for post, content in zip(posts_data['data'], contents)]

    df = pd.DataFrame(data)
    print(df.info())
    print(df.head())

if __name__ == "__main__":
    asyncio.run(main())