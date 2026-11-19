# Project 04 — Web Scraper for Headlines & Quotes

## Project objective
This Python project uses **Requests** and **BeautifulSoup** to collect recent technology headlines and quotes from public practice websites. It saves the collected information into CSV and TXT files.

## Features
- Scrapes story headlines and links from Hacker News.
- Scrapes quotes, authors, and tags from Quotes to Scrape.
- Saves data in both `.csv` and `.txt` formats.
- Lets the user choose headlines, quotes, or both.
- Handles network errors and creates the output folder automatically.

## Requirements
- Python 3.8 or newer
- Internet connection
- Packages listed in `requirements.txt`

## Installation and execution
1. Extract the project ZIP file.
2. Open a terminal or command prompt in the project folder.
3. Install dependencies:

   `python -m pip install -r requirements.txt`

4. Run the project:

   `python scraper.py`

By default, the program scrapes up to 10 headlines and 10 quotes.

### Optional commands
- `python scraper.py --mode headlines`
- `python scraper.py --mode quotes`
- `python scraper.py --mode both --limit 15`

## Output
The program creates an `output` folder containing:
- `headlines.csv` and `headlines.txt`
- `quotes.csv` and `quotes.txt`

The output files are generated when the program runs successfully.

## Libraries used
- **Requests:** sends HTTP requests and downloads web pages.
- **BeautifulSoup (bs4):** parses HTML and extracts the required elements.
- **csv:** writes structured data to CSV files.
- **argparse:** accepts command-line options.

## Websites used
- Hacker News: https://news.ycombinator.com/
- Quotes to Scrape: https://quotes.toscrape.com/

## Note
This is an educational scraper. Website HTML can change, and scraping requires an internet connection. Use reasonable request rates and follow each website's terms and access rules.
