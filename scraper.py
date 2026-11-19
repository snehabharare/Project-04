"""
Project 04: Web Scraper for Headlines & Quotes
----------------------------------------------
Scrapes:
  1. Latest technology headlines from Hacker News
  2. Inspirational quotes from Quotes to Scrape

Saves results as CSV and plain-text files in the output/ folder.

Install:
    pip install -r requirements.txt

Run:
    python scraper.py
    python scraper.py --mode headlines
    python scraper.py --mode quotes
    python scraper.py --mode both --limit 15
"""

import argparse
import csv
import os
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "StudentWebScraper/1.0 (educational project; Python requests)"
}
TIMEOUT = 15
OUTPUT_DIR = "output"


def fetch_page(url):
    """Download a web page and return its HTML."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        raise RuntimeError(f"Could not download {url}: {exc}") from exc


def scrape_headlines(limit=10):
    """Get recent story titles and links from the Hacker News front page."""
    url = "https://news.ycombinator.com/"
    soup = BeautifulSoup(fetch_page(url), "html.parser")
    results = []

    for row in soup.select("tr.athing"):
        title_element = row.select_one("span.titleline > a")
        if not title_element:
            continue

        title = title_element.get_text(" ", strip=True)
        link = title_element.get("href", "")
        if link.startswith("item?id="):
            link = "https://news.ycombinator.com/" + link

        results.append({
            "title": title,
            "link": link,
            "source": "Hacker News"
        })

        if len(results) >= limit:
            break

    if not results:
        raise RuntimeError("No headlines were found. The website layout may have changed.")
    return results


def scrape_quotes(limit=10):
    """Get quotes, authors, and tags from the Quotes to Scrape demo website."""
    url = "https://quotes.toscrape.com/"
    soup = BeautifulSoup(fetch_page(url), "html.parser")
    results = []

    for quote_box in soup.select("div.quote"):
        quote_element = quote_box.select_one("span.text")
        author_element = quote_box.select_one("small.author")
        if not quote_element or not author_element:
            continue

        tag_elements = quote_box.select("div.tags a.tag")
        tags = ", ".join(tag.get_text(strip=True) for tag in tag_elements)

        results.append({
            "quote": quote_element.get_text(strip=True),
            "author": author_element.get_text(strip=True),
            "tags": tags,
            "source": "Quotes to Scrape"
        })

        if len(results) >= limit:
            break

    if not results:
        raise RuntimeError("No quotes were found. The website layout may have changed.")
    return results


def save_results(data, filename, fields):
    """Save scraped records to CSV and readable TXT files."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    csv_path = os.path.join(OUTPUT_DIR, filename + ".csv")
    txt_path = os.path.join(OUTPUT_DIR, filename + ".txt")

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

    with open(txt_path, "w", encoding="utf-8") as txt_file:
        for number, item in enumerate(data, start=1):
            txt_file.write(f"{number}. ")
            if "title" in item:
                txt_file.write(item["title"] + "\n")
                txt_file.write(f"   Link: {item['link']}\n")
                txt_file.write(f"   Source: {item['source']}\n\n")
            else:
                txt_file.write(item["quote"] + "\n")
                txt_file.write(f"   Author: {item['author']}\n")
                txt_file.write(f"   Tags: {item['tags'] or 'None'}\n")
                txt_file.write(f"   Source: {item['source']}\n\n")

    return csv_path, txt_path


def main():
    parser = argparse.ArgumentParser(
        description="Scrape technology headlines and/or quotes into files."
    )
    parser.add_argument(
        "--mode", choices=["headlines", "quotes", "both"], default="both",
        help="Choose what to scrape (default: both)."
    )
    parser.add_argument(
        "--limit", type=int, default=10,
        help="Maximum number of records per category (default: 10)."
    )
    args = parser.parse_args()

    if args.limit < 1:
        parser.error("--limit must be at least 1")

    print("=" * 58)
    print("       WEB SCRAPER FOR HEADLINES & QUOTES")
    print("=" * 58)
    print("Started:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    tasks = []
    if args.mode in ("headlines", "both"):
        tasks.append(("headlines", scrape_headlines, ["title", "link", "source"]))
    if args.mode in ("quotes", "both"):
        tasks.append(("quotes", scrape_quotes, ["quote", "author", "tags", "source"]))

    failures = 0
    for name, scraper, fields in tasks:
        print(f"\nScraping {name}...")
        try:
            records = scraper(args.limit)
            csv_file, txt_file = save_results(records, name, fields)
            print(f"Success: collected {len(records)} {name}.")
            print(f"Saved: {csv_file}")
            print(f"Saved: {txt_file}")
        except RuntimeError as exc:
            failures += 1
            print(f"Error: {exc}", file=sys.stderr)

    print("\nFinished.")
    if failures == len(tasks):
        print("Nothing was saved. Check your internet connection and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
