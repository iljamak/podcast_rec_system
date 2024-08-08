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
