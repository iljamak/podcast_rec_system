import requests
from bs4 import BeautifulSoup
import re
import sys
from collections import deque
import asyncio
import aiohttp
'''
That's my original function with which i scrapped Podtail. Structure of html file is recurrent -->>> BFS-search.

Firstly, it goes to a first page with top-100 podcasts. And saves to a deque all of them.
Then it pops from the beginning and go to podcast page, where there are other 100 or so related and popular. So it 
adds them to deque. I also added a depth, because it needs to stop somewhere, and number of podcasts is growing 
exponentially. Also similar podcasts will appear, that's why added_podcasts is a set and not a list.

In overall, that's the main way of gathering names of popular podcasts. At the beginning there were about 35k-40k, but
i was working only with english, i have seperate datasets for each of languages. More than 3k of german podcasts 
and so on. In case you'll need them for some purposes, feel free to mail me and i'll send them to you.
(Illia Makovoz makovoz.ilja@gmail.com)
'''

added_podcasts = set()


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()



async def process_page(url, session):
    html = await fetch(url, session)
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find('ul', class_='feed podcasts clearfix')

    related_urls = []

    if ul:
        lis = ul.find_all('li')
        for li in lis:
            podcast = li.find('div', class_='information')
            link = li.find('a', href=True)
            if link:
                link = link.get('href')  # link for podcast
            if podcast and link:
                podc = podcast.find('h2')
                if podc:
                    podc = re.match(r'<h2>(.*)</h2>', str(podc))
                    if podc:
                        podc = podc.group(1)
                full_link = url_main + link
                if full_link in added_podcasts:
                    continue
                added_podcasts.add(full_link)
                print(podc)
                print(full_link)
                file.write(f'{podc};{full_link}\n')
                
                # Collect related podcast URLs
                related_url = url_main + link + 'related/'
                related_urls.append(related_url)

    return related_urls


async def bfs(url, file, depth=5):
    queue = deque([(url, depth)])  
    async with aiohttp.ClientSession() as session:  
        while queue:
            current_url, current_depth = queue.popleft()
            if current_depth <= 0:
                continue  # Skip if max depth reached

            related_urls = await process_page(current_url, session)  
            if related_urls:
                for related_url in related_urls:
                    queue.append((related_url, current_depth - 1))  


if __name__ == "__main__":
    url_main = 'https://podtail.com'
    url = 'https://podtail.com/top-podcasts/'
    
    with open('podcasts.csv', 'a', encoding='utf-8') as file:
        asyncio.run(bfs(url, file))  