# Podcast Recommendation Project

## Overview
This project is designed to scrape podcast data, process it, and provide recommendations based on various criteria such as categories, popularity, and embeddings. The project uses a combination of web scraping, data processing, and machine learning techniques to achieve this.

## Features
- Scrape podcast data from various sources.
- Process and clean the data.
- Generate recommendations based on different criteria
- Visualize data using Dash.

## Setup
1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Download vector embeddings:**
    ```bash
    pip install gdown
    gdown --folder https://drive.google.com/drive/folders/1XP_eSoZ2uNW_poyMnsK9TPWHcxpbwvsg
    ```

5. **Run the Dash application:**
    ```bash
    python dash_main.py
    ```

## Dataset collection and data cleaning
### Dataset collection
The dataset was collected using web scraping techniques. The primary sources of data were:
- **Podtail:** Scraped using `podtail_main.py` which collects podcast names, links, and related podcasts with async BFS scraping algorithm
- **Podcast Index** scraped with PodcastIndex API to extract descriptions,RSS feed URLs, language, categories and episode count
- **iTunes** was scraped to extract podcast logos for application and average rating

### Data cleaning
Data were cleaned using primarily pandas and other standard DS libs. Data cleaning is described in jupyter notebooks. Podcasts were divided based on the language and their descriptions were indexed (wiki-embeddings) to accelerate information retrieval. Most commons words were deleted to better capture semantic meaning of each podcast. 

### Recommendation system
Unfortunately, data limitation is the main issue and matrix decomposition cannot be performed, because there is no real data about user preferences. So recommendations were limited based on podcast description semantic meaning and common categories. To adress the question of recommending unpopular podcast, a koefficient based on total episodes, number of reviews and average rating was taken into account. 
SBERT embeddings and cosine similarity prooved to be the best and were used in the final version. 

### Dash application 
A dash application was used to investigate the quality of recommendations. Similar podcasts can be found based by using podcast name or iTunes id.
There are several modes to choose from:
- Most popular (random 10 from 200 most popular)
- Recommendations from SBERT embeddings
- Averaged word embeddings from Wikipedia
- Optimal recommendations
- Recommendations based on user explanations (f.e. "A podcast about scientifical approach to improve health and mood")

#### Examples
| ![Image 1](https://github.com/user-attachments/assets/82843772-1212-4589-9598-ce7abe6ee7b5) | ![Image 2](https://github.com/user-attachments/assets/15edab18-d58b-48fc-91d8-3a39a4fba039) |
|:-:|:-:|
| ![Image 3](https://github.com/user-attachments/assets/f3d14a61-4ba1-4355-9ee3-3dee0a7dbaaf) | ![Image 4](https://github.com/user-attachments/assets/a2e8b082-fad0-44cd-928c-9676e762139b) |
