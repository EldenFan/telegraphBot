import aiohttp
import asyncio
from telegraph import Telegraph
from bs4 import BeautifulSoup
from config import AUTHOR, HTML_PATTERN
import re

async def fetch_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            return await response.text()


async def copy_telegraph(url: str) -> str:
    html = await fetch_html(url)
    if not html:
        return "Не удалось загрузить статью."

    soup = BeautifulSoup(html, "html.parser")

    title = str(soup.find("h1"))
    title = title[title.find(">") + 1:title.rfind("<")]
    print(title)

    content = soup.find("article")
    if not content:
        return "Не удалось найти содержимое статьи."
    
    clean_content = re.sub(HTML_PATTERN, '', str(content), flags=re.DOTALL)
    clean_content = re.sub('</article>\s*$', '', clean_content)
    print(clean_content)

    telegraph = Telegraph()
    await asyncio.to_thread(telegraph.create_account, short_name="copier_bot")
    response = await asyncio.to_thread(
        telegraph.create_page,
        title=title,
        author_name=AUTHOR,
        html_content=clean_content
    )

    return f"Скопированная статья: https://telegra.ph/{response['path']}"