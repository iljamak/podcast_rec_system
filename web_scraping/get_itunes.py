import asyncio
import logging
import re
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import sys
import aiohttp
'''
Inspired by Real Python tutorial
'''
ID_REGEX = re.compile(r'id(\d+)')

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

# Define a semaphore
SEMAPHORE = asyncio.Semaphore(10)  # Change 10 to any other number to adjust the concurrency level.

async def fetch_html(url: str, session: ClientSession) -> str:
    resp = await session.request(method="GET", url=url)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    return await resp.text()

async def parse(url: str, session: ClientSession):
    try:
        html = await fetch_html(url=url, session=session)
        soup = BeautifulSoup(html, 'html.parser')
        id_element = soup.find('a', title='Apple Podcasts')
        id_match = ID_REGEX.search(id_element.get('href'))
        return id_match.group(1) if id_match else 0

    except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError) as e:
        logger.error(f"asyncio exception has occurred: {e}. Id was not found for URL: {url}")
        return None

    except Exception as e:
        logger.error(f"Unexpected error: {e}. Id was not found for URL: {url}")
        return None

async def find_and_save(line: str, session: ClientSession):
    async with SEMAPHORE:  # Use the semaphore here
        name, url = line.rstrip().split(';')
        id = await parse(url, session)
        if id:
            with open('new.csv', 'a', encoding='utf-8') as f:
                f.write(f"{name};{url};{id}\n")
                print(id)

async def process_csv(file_path: str):
    async with ClientSession() as session:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        await asyncio.gather(*(find_and_save(line, session) for line in lines))

if __name__ == "__main__":
    asyncio.run(process_csv('podcasts_copy.csv'))
