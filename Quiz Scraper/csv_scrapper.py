import requests
from bs4 import BeautifulSoup
import random
from csv import DictWriter

url = "http://quotes.toscrape.com/"


def scrape_quotes():
    response = requests.get(url)

    if not response.status_code == 200:
        raise Exception("Something is wrong")
    soup = BeautifulSoup(response.text, "html.parser")
    all_quotes = []
    href = url
    while True:
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            title = quote.find_next().get_text()
            name = quote.find_next(class_="author").get_text()
            bio_link = quote.find_next(class_="author").find_next()["href"]
            all_quotes.append({
                "title": title,
                "name": name,
                "bio-link": bio_link
            })
        next = soup.find(class_="next")
        print(f"Now Scrapping ....{href}")
        if not next:
            break
        href = url+next.find_next()["href"]  # next page link
        response = requests.get(href)
        soup = BeautifulSoup(response.text, "html.parser")
        time.sleep(2)
    return all_quotes


def write_quotes(all_quotes):
    with open("quote_data.csv", "w") as file:
        headers = ["title", "name", "bio-link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        try:
            for quote in all_quotes:
                csv_writer.writerow(quote)
        except :
            pass


quotes = scrape_quotes()
write_quotes(quotes)
