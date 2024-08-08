import aiohttp
import hashlib
import time
import asyncio
import sys
import json
'''
Headers should be generated like this and no other way.
I was being banned over and over, so i was changing proxy, but semaphore was more important.

Here i'm gathering more data about each podcast collected from podtail:
- description (main source of info for recommendations)
- language (to seperate eng from others)
- categories or genres 
- number of episodes
- podcast_index db id
'''

config = {
    "api_key": "ITUNES_API",
    "api_secret": "API_SECRET"
}

api_key = config["api_key"]
api_secret = config["api_secret"]

def generate_headers():
    epoch_time = int(time.time())
    data_to_hash = api_key + api_secret + str(epoch_time)
    sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()

    headers = {
        'X-Auth-Date': str(epoch_time),
        'X-Auth-Key': api_key,
        'Authorization': sha_1,
        'User-Agent': 'podcast_scrapping4dataset/1.2'
    }
    return headers

def extract_data_from_feed(feed):
    # Extract the desired information from the feed
    data = [
        feed["id"],
        feed["description"].replace(';', ' ').replace('\n',''),
        feed["originalUrl"],
        feed["language"],
        feed["categories"],
        feed["episodeCount"]
    ]
    return data

def write_to_csv(file_name, data):
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(';'.join(map(str, data)) + '\n')


sem = asyncio.Semaphore(3)  # Semaphore for limiting requests

current_proxy_index = 0
request_count = 0
PROXY_LIST = ["http://20.205.61.143:8123","http://161.35.39.82:3128","http://89.43.31.134:3128",
              "http://194.62.98.172","http://195.154.184.80","http://159.65.209.73"]
async def fetch_and_save(query: str, line):
    global current_proxy_index, request_count
    # Use the current proxy.
    proxy = PROXY_LIST[current_proxy_index]

    url = f"https://api.podcastindex.org/api/1.0/podcasts/byitunesid?id={query}&pretty"
    headers = generate_headers()

    async with sem:  # Using the semaphore here
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers,) as response:
                    request_count += 1

                    #Switching different proxies, that i've found on internet
                    if request_count >= 500:
                        request_count = 0
                        

                    response_data = await response.json()
                    feed = response_data.get('feed', {})
                    print(line)
                    if feed:
                        extracted_data = extract_data_from_feed(feed)
                        language = extracted_data[3]
                        if '-' in language:
                            language = language.split('-')
                            language = str(language[0])
                        new_row = list(line) + extracted_data
                        write_to_csv(f'podcasts_{language}.csv', new_row)
                        await asyncio.sleep(0.1)
            except Exception as e:
                # Log the exception and continue.
                print(f"Error for query {query}: {e}")
                sys.exit()

async def main():
    with open('new.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = lines[34309:]#already prepared, just turn on
        name, url, itunes_id = [list(map(str, group)) for group in zip(*[item.split(';') for item in lines])]
        itunes_id = [id[:-1] for id in itunes_id]
        lines = list(zip(name, url, itunes_id))

    # Combined fetching and saving
    await asyncio.gather(*(fetch_and_save(line[2], line) for line in lines))

# Run the test
if __name__ == "__main__":
    asyncio.run(main())