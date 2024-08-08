import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import re
import os
import sys
import csv
import time
from PIL import Image
from io import BytesIO
'''
A script to collect rating and number of ratings from Itunes.

dataset = pd.read_csv("PodRec/final_podcasts_en_processed.csv")
#https://podcasts.apple.com/podcast/id
itunes_ids = dataset['itunes_id']
itunes_ids[0] = 14215108510515234
'''
df = pd.read_csv('itunes_responses81516.csv')
not_finished = list(df[df['rating']==0].index)
itunes_ids = list(df['iTunesID'].iloc[not_finished])
sem = asyncio.Semaphore(5)
print("Sem")
async def fetch(session, id):
    #print("Fetch")
    async with sem: 
        try:
            itunes_id = "https://podcasts.apple.com/podcast/id" + str(id)
            async with session.get(itunes_id) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                element = soup.find_all(class_='we-rating-count star-rating__count')
                if element:
                    text = element[0].text
                    pattern = r'(\d+(?:\.\d+\w*)?)'
                    numbers = re.findall(pattern, text)
                    print(numbers)
                    return id, numbers
                return id, None
        except Exception as e:
            print(f"An error occurred: {e}")
            return id, None

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for id in urls:
            task = asyncio.create_task(fetch(session, id))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        print(f"Responses: {responses}")
        return responses

responses = asyncio.run(main(itunes_ids))
time = time.time()
time = str(time)
time = time[-5:] # unique_identifier, didnt want my file to be gone, when i accidentally rerun the script
# Writing to a CSV file
with open(f'itunes_responses_not_finished{time[-5:]}.csv', 'w', newline='', encoding='utf-8') as file:
    file.write('iTunesID,rating,number_of_reviews\n')
    
    for itunes_id, response in responses:
        if response is not None:
            file.write(f"{itunes_id},{response[0]},{response[1]}\n")
        else:
            file.write(f"{itunes_id},0,0\n")
