import pandas as pd
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
from PIL import Image
import io
import time

#loop is made to make periodical savings in case it will crash
#after crash or being banned, i can continue later
#Semaphor is also used for this purpose. It limits number or requests and helps not ot gather too much attention
#i've also tried to use sleep, changing proxies and different headers when sending requests,
#somtimes it helps, sometimes not, so best option is to make it fast, but not too fast


# Load dataset
dataset = pd.read_csv("../../PodRec/final_podcasts_en_processed2.csv")
itunes_ids = dataset['itunes_id'][6850:] # was doing in parts
last_index = len(itunes_ids) -1

sem = asyncio.Semaphore(10)


async def fetch(session, id):
    async with sem:  # acquire semaphore
        itunes_id = f"https://podcasts.apple.com/podcast/id{id}"
        try:
            async with session.get(itunes_id) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                res = soup.find(class_="we-artwork we-artwork--downloaded product-artwork product-artwork--bottom-separator product-artwork--captioned we-artwork--fullwidth")
                srcset = res.find('source')['srcset']
                match = re.search(r'https://[^\s,]+?\.webp', srcset)
                if match:
                    first_url = match.group()
                    async with session.get(first_url) as img_response:
                        img = await img_response.read()
                        try:
                            image = Image.open(io.BytesIO(img))
                            resized_image = image.resize((150, 150))
                            # Found, that can crash otherwise
                            if image.mode != 'RGB':
                                resized_image = resized_image.convert('RGB')
                            # Save the image in the specified directory as JPG
                            resized_image.save(f"podcasts_icons/{id}.jpg", 'JPEG')
                            return itunes_id, "OK"
                        except Exception as e:
                            print(f"Error processing image for {itunes_id}: {e}")
                            return itunes_id, "FAIL"
                return itunes_id, "OK"
        except Exception as e:
            print(f"An error occurred for {itunes_id}: {e}")
            return itunes_id, "FAIL"


async def main(urls):
    # Get the current running loop
    loop = asyncio.get_running_loop()

    async with aiohttp.ClientSession() as session:
        tasks = [loop.create_task(fetch(session, id)) for id in urls]
        collector = await asyncio.gather(*tasks)
        print(f"Responses: {collector}")
        return collector


for i in range(0,last_index,10):
    responses = asyncio.run(main(itunes_ids[i:i+10]))
    with open(f'itunes_responses_{12345}.csv', 'a', newline='', encoding='utf-8') as file:
        file.write('iTunesID,status\n')
        for itunes_id, response in responses:
            file.write(f"{itunes_id},{response}\n")


