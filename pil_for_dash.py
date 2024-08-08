from PIL import Image
import pandas as pd
import numpy as np


def get_pils(df):
    '''Returns a list of tuplees with PIL.Image and a corresponding title'''
    pils = []
    if df is None:
        pils.append(Image.open(f"podcasts_icons/default.jpg"))
        pils.append(Image.open(f"podcasts_icons/n.jpg"))
        pils.append(Image.open(f"podcasts_icons/o.jpg"))
        pils.append(Image.open(f"podcasts_icons/t.jpg"))
        pils.append(Image.open(f"podcasts_icons/default.jpg"))
        pils.append(Image.open(f"podcasts_icons/f.jpg"))
        pils.append(Image.open(f"podcasts_icons/o.jpg"))
        pils.append(Image.open(f"podcasts_icons/u.jpg"))
        pils.append(Image.open(f"podcasts_icons/n.jpg"))
        pils.append(Image.open(f"podcasts_icons/d.jpg"))
        titles = ['' for _ in range(10)]
        return list(zip(pils,titles))

    itunes_ids = df['itunes_id'][:10]
    titles = df['podcast_name'][:10]
    for itunes_id in itunes_ids:
        try:
            pils.append(Image.open(f"podcasts_icons/{itunes_id}.jpg"))
        except Exception as e:
            print(e)
            pils.append(Image.open(f"podcasts_icons/default.jpg"))
    return list(zip(pils,titles))